# -*- coding: utf-8 -*-
import asyncio

from qqbot.core.util import logging

logger = logging.getLogger()


class SessionPool:
    """
    SessionPool主要支持session的重连，可以根据session的状态动态设置是否需要进行重连操作
    这里通过设置session_id=""空则任务session需要重连
    """

    def __init__(self, max_async, session_manager, loop=None):
        self.max_async = max_async
        self.session_manager = session_manager
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        # session链接同时最大并发数
        self.session_list = []

    async def run(self, session_interval=5):
        loop = self.loop

        # 根据并发数同时建立多个future
        index = 0
        session_list = self.session_list
        # 需要执行的链接列表，通过time_interval控制启动时间
        tasks = []

        while len(session_list) > 0:
            logger.debug("session list circle run")
            time_interval = session_interval * (index + 1)
            logger.info("[连接池]最大并发连接数: %s, 启动会话数: %s" % (self.max_async, len(session_list)))
            for i in range(self.max_async):
                if len(session_list) == 0:
                    break
                tasks.append(asyncio.ensure_future(self._runner(session_list.pop(i), time_interval), loop=loop))
            index += self.max_async

        await asyncio.wait(tasks)

    async def _runner(self, session, time_interval):
        await self.session_manager.new_connect(session)
        # 后台有频率限制，根据间隔时间发起链接请求
        await asyncio.sleep(time_interval)

    def add(self, session):
        self.session_list.append(session)

    def close(self):
        self.loop.close()
