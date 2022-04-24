# -*- coding: utf-8 -*-

import asyncio

from qqbot.core.network.ws_sync.ws_client import Client
from qqbot.core.network.ws_sync.ws_session_pool import SessionPool
from qqbot.core.network.ws.dto.enum_intents import Intents
from qqbot.core.network.ws.ws_session import Session, ShardConfig
from qqbot.core.util import logging
from qqbot.model.token import Token

logger = logging.getLogger()


def _loop_exception_handler(loop, context):
    # first, handle with default handler
    loop.default_exception_handler(context)

    exception = context.get("exception")
    if isinstance(exception, ZeroDivisionError):
        print(context)
        loop.stop()


def _on_connected(ws_client):
    if ws_client.ws_conn is None:
        raise Exception("websocket connection failed ")
    if ws_client.session.session_id != "":
        ws_client.reconnect()
    else:
        ws_client.identify()


def _check_session_limit(websocket_ap):
    return websocket_ap["shards"] > websocket_ap["session_start_limit"]["remaining"]


def _cal_interval(max_concurrency):
    """
    :param max_concurrency:每5s可以创建的session数
    :return: 链接间隔时间
    """
    return round(5 / max_concurrency)


class SessionManager:
    session_pool: SessionPool

    def start(self, websocket_ap, token=Token, intent=Intents):
        logger.info("[连接管理]程序启动中...")
        # 每个机器人创建的连接数不能超过remaining剩余连接数
        if _check_session_limit(websocket_ap):
            raise Exception("session limit exceeded")
        # 根据session限制建立链接
        session_interval = _cal_interval(websocket_ap["session_start_limit"]["max_concurrency"])
        shards_count = websocket_ap["shards"]
        logger.debug("session_interval: %s" % session_interval, "shards: %s" % shards_count)
        # 根据限制建立分片的并发链接数
        self.init_session_pool(intent, shards_count, token, websocket_ap, session_interval)

    def init_session_pool(self, intent, shards_count, token, websocket_ap, session_interval):

        # 实例一个session_pool
        self.session_pool = SessionPool(
            max_async=websocket_ap["session_start_limit"]["max_concurrency"],
            session_manager=self,
            loop=asyncio.get_event_loop(),
        )
        for i in range(shards_count):
            session = Session(
                session_id="",
                url=websocket_ap["url"],
                intent=intent,
                last_seq=0,
                token=token,
                shards=ShardConfig(i, shards_count),
            )
            self.session_pool.add_task(session)

        self.start_session(session_interval)

    def start_session(self, session_interval=5):
        self.session_pool.loop.set_exception_handler(_loop_exception_handler)
        self.session_pool.loop.run_until_complete(self.session_pool.run(session_interval))

    def new_connect(self, session):
        """
        newConnect 启动一个新的连接，如果连接在监听过程中报错了，或者被远端关闭了链接，需要识别关闭的原因，能否继续 resume
        如果能够 resume，则往 sessionChan 中放入带有 sessionID 的 session
        如果不能，则清理掉 sessionID，将 session 放入 sessionChan 中
        session 的启动，交给 start 中的 for 循环执行，session 不自己递归进行重连，避免递归深度过深

        param session: session对象
        """
        logger.info("[连接管理]会话启动中...")

        client = Client(session, self)
        client.connect(_on_connected)
