# -*- coding: utf-8 -*-
import asyncio
import json
import traceback

import aiohttp
from aiohttp import WSMessage, ClientWebSocketResponse

from qqbot.core.exception.error import WebsocketError
from qqbot.core.network.ws.dto.enum_intents import Intents
from qqbot.core.network.ws.dto.enum_opcode import OpCode
from qqbot.core.network.ws.dto.ws_payload import (
    WSPayload,
    WsIdentifyData,
    WSResumeData,
)
from qqbot.core.network.ws_async.ws_async_handler import parse_and_handle
from qqbot.core.util import logging

logger = logging.getLogger()


class Client:
    def __init__(self, session, session_manager, connected_callback=None):
        self.session = session
        self.ws_conn = None
        self.session_manager = session_manager
        self.connected_callback = connected_callback
        self.can_reconnect = False

    async def on_error(self, exception: BaseException):
        logger.error(
            "on_error: websocket connection: %s, exception : %s"
            % (self.ws_conn, exception)
        )
        traceback.print_exc()

    async def on_close(self, ws, close_status_code, close_msg):
        logger.info(
            "on_close: websocket connection %s" % ws
            + ", code: %s" % close_status_code
            + ", msg: %s" % close_msg
        )
        # 这种不能重新链接
        if (
            close_status_code == WebsocketError.CodeConnCloseErr
            or close_status_code == WebsocketError.CodeInvalidSession
            or self.can_reconnect is False
        ):
            self.session.session_id = ""
            self.session.last_seq = 0
        # 断连后启动一个新的链接并透传当前的session，不使用内部重连的方式，避免死循环
        self.session_manager.session_pool.add(self.session)
        asyncio.ensure_future(self.session_manager.session_pool.run())

    async def on_message(self, ws, message):
        logger.debug("on_message: %s" % message)
        message_event = json.loads(message)
        if await self._is_system_event(message_event, ws):
            return
        if "t" in message_event.keys() and message_event["t"] == "READY":
            event_seq = message_event["s"]
            if event_seq > 0:
                self.session.last_seq = event_seq
            await self._ready_handler(message_event)
            return
        if "t" in message_event.keys():
            await parse_and_handle(message_event, message)

    async def on_connected(self, ws):
        logger.info("ws client connected ok")
        self.ws_conn = ws
        await self.connected_callback(self)
        # 心跳检查
        asyncio.ensure_future(self._send_heartbeat(interval=30))

    async def connect(self):
        """
        websocket向服务器端发起链接，并定时发送心跳
        """

        logger.info("ws client start connect")
        ws_url = self.session.url
        if ws_url == "":
            raise Exception("session url is none")

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.session.url) as ws_conn:
                while True:
                    msg: WSMessage
                    msg = await ws_conn.receive()
                    await self.dispatch(msg, ws_conn)
                    if ws_conn.closed:
                        logger.info("ws is closed, stop circle receive msg")
                        break

    async def dispatch(self, msg, ws_conn):
        """
        ws事件分发
        """
        if msg.type == aiohttp.WSMsgType.TEXT:
            await self.on_message(ws_conn, msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            await self.on_error(ws_conn.exception())
        elif (
            msg.type == aiohttp.WSMsgType.CLOSED or msg.type == aiohttp.WSMsgType.CLOSE
        ):
            await self.on_close(ws_conn, ws_conn.close_code, msg.extra)

    async def identify(self):
        """
        websocket鉴权
        """
        if self.session.intent == 0:
            self.session.intent = Intents.INTENT_GUILDS.value
        logger.info("ws:%s start identify" % self.ws_conn)
        identify_event = json.dumps(
            WSPayload(
                WsIdentifyData(
                    token=self.session.token.get_string(),
                    intents=self.session.intent,
                    shard=[
                        self.session.shards.shard_id,
                        self.session.shards.shard_count,
                    ],
                ).__dict__,
                op=OpCode.WS_IDENTITY.value,
            ).__dict__
        )
        await self.send_msg(identify_event)

    async def send_msg(self, event_json):
        """
        websocket发送消息
        :param event_json:
        """
        send_msg = event_json
        logger.debug("send_msg: %s" % send_msg)
        if isinstance(self.ws_conn, ClientWebSocketResponse):
            if self.ws_conn.closed:
                logger.error("send_msg: websocket connection has closed")
            else:
                await self.ws_conn.send_str(data=send_msg)

    async def reconnect(self):
        """
        websocket重连
        """
        logger.info("ws:%s is reconnected" % self.ws_conn)
        resume_event = json.dumps(
            WSPayload(
                WSResumeData(
                    token=self.session.token.get_string(),
                    session_id=self.session.session_id,
                    seq=self.session.last_seq,
                ).__dict__,
                op=OpCode.WS_RESUME.value,
            ).__dict__
        )
        await self.send_msg(resume_event)

    async def _ready_handler(self, message_event):
        data = message_event["d"]
        self.version = data["version"]
        self.session.session_id = data["session_id"]
        self.session.shards.shard_id = data["shard"][0]
        self.session.shards.shard_count = data["shard"][1]
        self.user = data["user"]

    async def _is_system_event(self, message_event, ws):
        """
        系统事件
        :param message_event:消息
        :param ws:websocket
        :return:
        """
        event_op = message_event["op"]
        if event_op == OpCode.WS_HELLO.value:
            await self.on_connected(ws)
            return True
        if event_op == OpCode.WS_HEARTBEAT_ACK.value:
            return True
        if event_op == OpCode.WS_RECONNECT.value:
            self.can_reconnect = True
            return True
        if event_op == OpCode.WS_INVALID_SESSION.value:
            self.can_reconnect = False
            return True
        return False

    async def _send_heartbeat(self, interval):
        """
        心跳包
        :param interval: 间隔时间
        """
        logger.info("start send heartbeat")
        while True:
            heartbeat_event = json.dumps(
                WSPayload(
                    op=OpCode.WS_HEARTBEAT.value, d=self.session.last_seq
                ).__dict__
            )
            if self.ws_conn is None:
                logger.error("ws is None")
                return
            else:
                if self.ws_conn.closed:
                    logger.info("ws is closed, stop circle heartbeat")
                    return
                else:
                    await asyncio.sleep(interval)
                    await self.send_msg(heartbeat_event)
