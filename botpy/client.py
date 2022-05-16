import asyncio
import sys
import traceback
from types import TracebackType
from typing import Any, Callable, Coroutine, Dict, List, Tuple, Optional, Type

from .api import WebsocketAPI
from .core.network.ws.ws_session import Session, ShardConfig
from .core.util import logging
from .flags import Intents
from .gateway import BotWebSocket
from .model import Token
from .runtime import SessionPool

_log = logging.getLogger()


class _LoopSentinel:
    __slots__ = ()

    def __getattr__(self, attr: str) -> None:
        msg = (
            "loop attribute cannot be accessed in non-async contexts. "
            "Consider using either an asynchronous main function and passing it to asyncio.run or "
            "using asynchronous initialisation hooks such as Client.setup_hook"
        )
        raise AttributeError(msg)


_loop: Any = _LoopSentinel()


def _loop_exception_handler(loop, context):
    # first, handle with default handler
    loop.default_exception_handler(context)

    exception = context.get("exception")
    if isinstance(exception, ZeroDivisionError):
        print(context)
        loop.stop()


async def _on_connected(ws_client):
    if ws_client.ws_conn is None:
        raise Exception("websocket connection failed ")
    if ws_client.session.session_id != "":
        await ws_client.reconnect()
    else:
        await ws_client.identify()


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

    def __init__(self, ret_coro=False):
        # 是否返回协程对象
        self.ret_coro = ret_coro

    async def start(self, websocket_ap, token: Type[Token], intent: int):
        _log.info("[连接管理]程序启动...")
        # 每个机器人创建的连接数不能超过remaining剩余连接数
        if _check_session_limit(websocket_ap):
            raise Exception("session limit exceeded")
        # 根据session限制建立链接
        session_interval = _cal_interval(websocket_ap["session_start_limit"]["max_concurrency"])
        shards_count = websocket_ap["shards"]
        _log.debug("session_interval: %s, shards: %s" % (session_interval, shards_count))
        # 根据限制建立分片的并发链接数
        return await self.init_session_pool(intent, shards_count, token, websocket_ap, session_interval)

    async def init_session_pool(self, intent, shards_count, token, websocket_ap, session_interval):

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
            self.session_pool.add(session)
        return await self.start_session(session_interval)

    async def start_session(self, session_interval=5):
        pool = self.session_pool
        loop = pool.loop
        loop.set_exception_handler(_loop_exception_handler)
        try:
            # 返回协程对象，交由开发者自行调控
            if self.ret_coro:
                return pool.run(session_interval)
            else:
                await pool.run(session_interval)
        except KeyboardInterrupt:
            _log.info("[连接管理]服务强行停止!")
            # cancel all tasks lingering

    async def new_connect(self, session):
        """
        newConnect 启动一个新的连接，如果连接在监听过程中报错了，或者被远端关闭了链接，需要识别关闭的原因，能否继续 resume
        如果能够 resume，则往 sessionChan 中放入带有 sessionID 的 session
        如果不能，则清理掉 sessionID，将 session 放入 sessionChan 中
        session 的启动，交给 start 中的 for 循环执行，session 不自己递归进行重连，避免递归深度过深

        param session: session对象
        """
        _log.info("[连接管理]新会话启动中...")

        client = BotWebSocket(session, self, _on_connected)
        try:
            await client.connect()
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            await client.on_error(e)


class Client:
    """botpy的机器人客户端"""

    def __init__(self, intents: Intents):
        self._closed: bool = False
        self.intents: int = intents.value
        self._connection = None
        self.http = None
        self.loop = None
        self._listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        self._ws_ap: Dict = {}

    async def __aenter__(self):
        print("__aenter__")
        await self._async_setup_hook()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        print("__aexit__")

        if not self.is_closed():
            await self.close()

    async def close(self) -> None:
        """关闭client相关的连接"""

        if self._closed:
            return

        self._closed = True

    def is_closed(self) -> bool:
        """:class:`bool`: Indicates if the websocket connection is closed."""
        return self._closed

    async def _async_setup_hook(self) -> None:
        # Called whenever the client needs to initialise asyncio objects with a running loop
        loop = asyncio.get_running_loop()
        self.loop = loop
        self._ready = asyncio.Event()

    def run(self, *args: Any, **kwargs: Any) -> None:
        """机器人服务开始执行
        注意: 这里会阻塞后面的执行代码

        如果想获取协程对象，可以使用`start`方法执行服务, 如:
        ```
        async with Client as c:
            c.start()
        ```
        """

        async def runner():
            async with self:
                await self.start(*args, **kwargs)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            # nothing to do here
            # `asyncio.run` handles the loop cleanup
            # and `self.start` closes all sockets and the HTTPClient instance.
            return

    async def start(self, appid: str, token: str, ret_coro: bool = False) -> Optional[Coroutine]:
        """机器人开始执行

         参数
        ------------
        appid: :class:`str`
            机器人 appid
        token: :class:`str`
            机器人 token
        ret_coro: :class:`bool
            是否需要返回协程对象
        """
        # login后再进行后面的操作
        token = Token(appid, token)
        await self.login(token)

        # 实例一个session_manager
        manager = SessionManager(ret_coro=ret_coro)
        return await manager.start(self._ws_ap, token.bot_token(), self.intents)

    async def login(self, token: Token) -> None:
        _log.info("[连接管理]登录机器人账号中...")

        if self.loop is _loop:
            await self._async_setup_hook()

        # 通过api获取websocket链接
        ws_api = WebsocketAPI(token)
        self._ws_ap = ws_api.ws()

    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

    def dispatch(self, event: str, *args: Any, **kwargs: Any) -> None:
        _log.debug("Dispatching event %s", event)
        method = "on_" + event

        listeners = self._listeners.get(event)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as exc:
                    future.set_exception(exc)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)

            if len(removed) == len(listeners):
                self._listeners.pop(event)
            else:
                for idx in reversed(removed):
                    del listeners[idx]

        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._schedule_event(coro, method, *args, **kwargs)

    def _schedule_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
        wrapped = self._run_event(coro, event_name, *args, **kwargs)
        # Schedules the task
        return self.loop.create_task(wrapped, name=f"botpy: {event_name}")

    async def _run_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass
