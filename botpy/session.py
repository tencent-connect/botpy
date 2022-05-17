import asyncio
from typing import List, Callable

from .core.network.ws.ws_session import Session
from .core.util import logging

_log = logging.getLogger()


class ConnectionSession:
    """Client的ws连接池

    SessionPool主要支持session的重连,可以根据session的状态动态设置是否需要进行重连操作
    这里通过设置session_id=""空则任务session需要重连
    """

    def __init__(self, max_async, _connect: Callable, _dispatch: Callable, loop=None):
        self.dispatch = _dispatch

        self._connect = _connect
        self._max_async = max_async
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        # session链接同时最大并发数
        self._session_list: List[Session] = []

    async def run(self, session_interval=5):
        loop = self._loop

        # 根据并发数同时建立多个future
        index = 0
        session_list = self._session_list
        # 需要执行的链接列表，通过time_interval控制启动时间
        tasks = []

        while len(session_list) > 0:
            _log.debug("session list circle run")
            time_interval = session_interval * (index + 1)
            _log.info("[连接池]最大并发连接数: %s, 启动会话数: %s" % (self._max_async, len(session_list)))
            for i in range(self._max_async):
                if len(session_list) == 0:
                    break
                tasks.append(asyncio.ensure_future(self._runner(session_list.pop(i), time_interval), loop=loop))
            index += self._max_async

        await asyncio.wait(tasks)

    async def _runner(self, session, time_interval):
        await self._connect(session)
        # 后台有频率限制，根据间隔时间发起链接请求
        await asyncio.sleep(time_interval)

    def add(self, session):
        self._session_list.append(session)
