# -*- coding: utf-8 -*-
import json
import threading
import traceback

import websocket

from qqbot.core.exception.error import WebsocketError
from qqbot.core.network.ws.dto.enum_intents import Intents
from qqbot.core.network.ws.dto.enum_opcode import OpCode
from qqbot.core.network.ws.dto.ws_payload import (
    WSPayload,
    WsIdentifyData,
    WSResumeData,
)
from qqbot.core.network.ws_sync.ws_event_handler import parse_and_handle
from qqbot.core.util import logging

logger = logging.getLogger()


def _loop_exception_handler(loop, context):
    # first, handle with default handler
    loop.default_exception_handler(context)

    exception = context.get("exception")
    if isinstance(exception, ZeroDivisionError):
        print(context)
        loop.stop()


class Client:
    def __init__(self, session, session_manager):
        self.session = session
        self.ws_conn = None
        self.heartbeat_thread = None
        self.session_manager = session_manager
        self.can_reconnect = False

    def connect(self, connected_callback):
        """
        websocket向服务器端发起链接，并定时发送心跳
        :param connected_callback:链接成功后的回调
        """
        ws_url = self.session.url
        if ws_url == "":
            raise Exception("session url is none")

        def on_close(ws, close_status_code, close_msg):
            logger.info(
                "[ws连接]关闭, 返回码: %s" % close_status_code + ", 返回信息:%s" % close_msg
            )
            # 关闭心跳包线程
            self.ws_conn = None
            # 这种不能重新链接
            if (
                close_status_code == WebsocketError.CodeConnCloseErr
                or close_status_code == WebsocketError.CodeInvalidSession
                or self.can_reconnect is False
            ):
                self.session.session_id = ""
                self.session.last_seq = 0
            # 断连后启动一个新的链接并透传当前的session，不使用内部重连的方式，避免死循环
            self.session_manager.session_pool.add_task(self.session)
            self.session_manager.start_session()

        def on_message(ws, message):
            logger.debug("on_message: %s" % message)
            message_event = json.loads(message)
            if self._is_system_event(message_event, ws, connected_callback):
                return
            if "t" in message_event.keys() and message_event["t"] == "READY":
                logger.info("[ws连接]鉴权成功")
                event_seq = message_event["s"]
                if event_seq > 0:
                    self.session.last_seq = event_seq
                self._ready_handler(message_event)
                logger.info("[ws连接]程序启动成功！")
                return
            if "t" in message_event.keys():
                parse_and_handle(message_event, message)

        def on_error(ws, exception=Exception):
            traceback.print_exc()

        def on_open(ws):
            logger.debug("on_open: %s" % ws)

        ws_app = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
        )

        self.heartbeat_thread = threading.Thread(
            target=self._send_heartbeat, args=(30, (threading.Event()))
        )
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()

        ws_app.run_forever()

    def identify(self):
        """
        websocket鉴权
        """
        if self.session.intent == 0:
            self.session.intent = Intents.INTENT_GUILDS.value
        logger.info("[ws连接]鉴权中...")
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
        self.send_msg(identify_event)

    def send_msg(self, event_json):
        """
        websocket发送消息
        :param event_json:
        """
        send_msg = event_json
        logger.debug("send_msg: %s" % send_msg)
        self.ws_conn.send(data=send_msg)

    def reconnect(self):
        """
        websocket重连
        """
        logger.info("[ws连接]重连启动中...")
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
        self.send_msg(resume_event)

    def _ready_handler(self, message_event):
        data = message_event["d"]
        self.version = data["version"]
        self.session.session_id = data["session_id"]
        self.session.shards.shard_id = data["shard"][0]
        self.session.shards.shard_count = data["shard"][1]
        self.user = data["user"]

    def _is_system_event(self, message_event, ws, connected_callback):
        """
        系统事件
        :param message_event:消息
        :param ws:websocket
        :param connected_callback:回调
        :return:
        """
        event_op = message_event["op"]
        if event_op == OpCode.WS_HELLO.value:
            self.ws_conn = ws
            connected_callback(self)
            return True
        if event_op == OpCode.WS_HEARTBEAT.value:
            return True
        if event_op == OpCode.WS_RECONNECT.value:
            self.can_reconnect = True
            return True
        if event_op == OpCode.WS_INVALID_SESSION.value:
            self.can_reconnect = False
            return True
        return False

    def _send_heartbeat(self, interval, thread_event):
        """
        心跳包
        :param interval: 间隔时间
        :param thread_event: 线程
        """
        while not thread_event.wait(interval):
            heartbeat_event = json.dumps(
                WSPayload(
                    op=OpCode.WS_HEARTBEAT.value, d=self.session.last_seq
                ).__dict__
            )
            if self.ws_conn is None:
                self.heartbeat_thread.stopped = True
            else:
                self.send_msg(heartbeat_event)
