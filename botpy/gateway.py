# -*- coding: utf-8 -*-
import asyncio
import json
import traceback
from typing import Optional

import aiohttp
from aiohttp import WSMessage, ClientWebSocketResponse

from . import logging
from .error import WebsocketError
from .session import ConnectionSession
from .types.gateway import ReadyEvent
from .types.session import Session
from .utils import JsonUtil

_log = logging.getLogger()


class BotWebSocket:
    """Bot的Websocket实现

    CODE	名称	客户端操作	描述
    0	Dispatch	Receive	服务端进行消息推送
    1	Heartbeat	Send/Receive	客户端或服务端发送心跳
    2	Identify	Send	客户端发送鉴权
    6	Resume	Send	客户端恢复连接
    7	Reconnect	Receive	服务端通知客户端重新连接
    9	Invalid Session	Receive	当identify或resume的时候，如果参数有错，服务端会返回该消息
    10	Hello	Receive	当客户端与网关建立ws连接之后，网关下发的第一条消息
    11	Heartbeat ACK	Receive	当发送心跳成功之后，就会收到该消息
    """

    WS_DISPATCH_EVENT = 0
    WS_HEARTBEAT = 1
    WS_IDENTITY = 2
    WS_RESUME = 6
    WS_RECONNECT = 7
    WS_INVALID_SESSION = 9
    WS_HELLO = 10
    WS_HEARTBEAT_ACK = 11

    def __init__(self, session: Session, _connection: ConnectionSession):
        self._conn: Optional[ClientWebSocketResponse] = None
        self._session = session
        self._connection = _connection
        self._parser = _connection.parser
        self._can_reconnect = False

    async def on_error(self, exception: BaseException):
        _log.error("on_error: websocket connection: %s, exception : %s" % (self._conn, exception))
        traceback.print_exc()

    async def on_close(self, close_status_code, close_msg):
        _log.info("[ws连接]关闭, 返回码: %s" % close_status_code + ", 返回信息:%s" % close_msg)
        # 这种不能重新链接
        if (
            close_status_code == WebsocketError.CodeConnCloseErr
            or close_status_code == WebsocketError.CodeInvalidSession
            or self._can_reconnect is False
        ):
            self._session["session_id"] = ""
            self._session["last_seq"] = 0
        # 断连后启动一个新的链接并透传当前的session，不使用内部重连的方式，避免死循环
        self._connection.add(self._session)
        asyncio.ensure_future(self._connection.run())

    async def on_message(self, ws, message):
        msg = json.loads(message)
        if await self._is_system_event(msg, ws):
            return

        if "t" in msg.keys() and msg["t"] == "READY":
            _log.info("[ws连接]鉴权成功")
            event_seq = msg["s"]
            if event_seq > 0:
                self._session["last_seq"] = event_seq
            ready = await self._ready_handler(msg)
            _log.info(f"[ws连接] 机器人「 {ready['user']['username']} 」 启动成功！")

        if "t" in msg.keys():
            event = msg["t"].lower()
            _log.debug("[ws连接]接收消息: %s" % message)

            try:
                func = self._parser[event]
            except KeyError:
                _log.debug("unknown event %s.", event)
            else:
                func(msg.get("d"))

    async def on_connected(self, ws: ClientWebSocketResponse):
        self._conn = ws
        if self._conn is None:
            raise Exception("websocket connection failed ")
        if self._session["session_id"] != "":
            await self.connect()
        else:
            await self.identify()
        # 心跳检查
        asyncio.ensure_future(self._send_heartbeat(interval=30))

    async def connect(self):
        """
        websocket向服务器端发起链接，并定时发送心跳
        """

        _log.info("[ws连接]启动中...")
        ws_url = self._session["url"]
        if ws_url == "":
            raise Exception("session url is none")

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self._session["url"]) as ws_conn:
                while True:
                    msg: WSMessage
                    msg = await ws_conn.receive()
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await self.on_message(ws_conn, msg.data)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        await self.on_error(ws_conn.exception())
                    elif msg.type == aiohttp.WSMsgType.CLOSED or msg.type == aiohttp.WSMsgType.CLOSE:
                        await self.on_close(ws_conn.close_code, msg.extra)
                    if ws_conn.closed:
                        _log.debug("ws is closed, stop circle receive msg")
                        break

    async def identify(self):
        """websocket鉴权"""
        if self._session["intent"] == 0:
            self._session["intent"] = 1

        _log.info("[ws连接]鉴权中...")

        payload = {
            "op": self.WS_IDENTITY,
            "d": {
                "shard": [
                    self._session["shards"]["shard_id"],
                    self._session["shards"]["shard_count"],
                ],
                "token": self._session["token"].get_string(),
                "intents": self._session["intent"],
            },
        }

        await self.send_msg(JsonUtil.dict2json(payload))

    async def send_msg(self, event_json):
        """
        websocket发送消息
        :param event_json:
        """
        send_msg = event_json
        _log.debug("[ws连接]发送消息: %s" % send_msg)
        if isinstance(self._conn, ClientWebSocketResponse):
            if self._conn.closed:
                _log.debug("[ws连接]ws连接已关闭! ws对象: %s" % self._conn)
            else:
                await self._conn.send_str(data=send_msg)

    async def resume(self):
        """
        websocket重连
        """
        _log.info("[ws连接]重连启动...")

        payload = {
            "op": self.WS_RESUME,
            "d": {
                "token": self._session["token"].get_string(),
                "session_id": self._session["session_id"],
                "seq": self._session["last_seq"],
            },
        }

        await self.send_msg(JsonUtil.dict2json(payload))

    async def _ready_handler(self, message_event) -> ReadyEvent:
        data = message_event["d"]
        self.version = data["version"]
        self._session["session_id"] = data["session_id"]
        self._session["shards"]["shard_id"] = data["shard"][0]
        self._session["shards"]["shard_count"] = data["shard"][1]
        self.user = data["user"]
        return data

    async def _is_system_event(self, message_event, ws):
        """
        系统事件
        :param message_event:消息
        :param ws:websocket
        :return:
        """
        event_op = message_event["op"]
        if event_op == self.WS_HELLO:
            await self.on_connected(ws)
            return True
        if event_op == self.WS_HEARTBEAT_ACK:
            return True
        if event_op == self.WS_RECONNECT:
            self._can_reconnect = True
            return True
        if event_op == self.WS_INVALID_SESSION:
            self._can_reconnect = False
            return True
        return False

    async def _send_heartbeat(self, interval):
        """
        心跳包
        :param interval: 间隔时间
        """
        _log.info("[ws连接]心跳检测启动...")
        while True:
            payload = {
                "op": self.WS_HEARTBEAT,
                "d": self._session["last_seq"],
            }

            if self._conn is None:
                _log.debug("[ws连接]连接已关闭!")
                return
            else:
                if self._conn.closed:
                    _log.debug("[ws连接]ws连接已关闭, 心跳检测停止，ws对象: %s" % self._conn)
                    return
                else:
                    await asyncio.sleep(interval)
                    await self.send_msg(JsonUtil.dict2json(payload))
