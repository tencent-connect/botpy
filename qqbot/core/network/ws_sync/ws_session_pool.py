# -*- coding: utf-8 -*-
import asyncio
import threading
import time

from qqbot.core.util import logging

logger = logging.getLogger()


class SessionPool:
    """
    SessionPool主要支持session的重连，可以根据session的状态动态设置是否需要进行重连操作
    这里通过设置session_id=""空则任务session需要重连
    """

    def __init__(self, max_async, session_manager, loop=None, session_count=1):
        self.max_async = max_async
        self.session_manager = session_manager
        self.loop = loop or asyncio.get_event_loop()
        self._queue = asyncio.Queue(maxsize=session_count, loop=self.loop)
        self.lock = threading.Lock()
        # session链接同时最大并发数
        self.work_list = []

    async def run(self, session_interval=5):
        works = [
            asyncio.ensure_future(self._work(session_interval), loop=self.loop)
            for _ in range(self.max_async)
        ]
        self.work_list.extend(works)
        await self._queue.join()
        logger.info("all tasks done")

    async def _work(self, session_interval):

        try:
            while True:
                # 后台有限制，一定时间后发起链接
                time.sleep(session_interval)
                session = await self._queue.get()
                logger.info("get session: %s" % session)
                # 这里开启线程添加websocket链接，不用等待
                thread = threading.Thread(
                    target=self.session_manager.new_connect, args=(session,)
                )
                thread.start()
                self._queue.task_done()
                if self._queue.empty():
                    break

        except asyncio.CancelledError:
            logger.error(asyncio.CancelledError)

    def add_task(self, item):
        with self.lock:
            self._queue.put_nowait(item)

    @property
    def count(self):
        return self._queue.qsize()

    def print_status(self):
        for w in self.work_list:
            logger.info(w.done())
