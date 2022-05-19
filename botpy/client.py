import asyncio
import sys
import traceback
from types import TracebackType
from typing import Any, Callable, Coroutine, Dict, List, Tuple, Optional, Type

from . import logging
from .api import AsyncWebsocketAPI
from .flags import Intents
from .gateway import BotWebSocket
from .model import Token
from .connection import ConnectionSession

_log = logging.getLogger()


class _LoopSentinel:
    __slots__ = ()

    def __getattr__(self, attr: str) -> None:
        raise AttributeError("无法在非异步上下文中访问循环属性")


_loop: Any = _LoopSentinel()


def _loop_exception_handler(loop, context):
    # first, handle with default handler
    loop.default_exception_handler(context)

    exception = context.get("exception")
    if isinstance(exception, ZeroDivisionError):
        print(context)
        loop.stop()


class Client:
    """botpy的机器人客户端"""

    def __init__(self, intents: Intents):
        self.intents: int = intents.value
        self.ret_coro: bool = False
        self.http = None
        self.loop = None

        self._connection: Optional[ConnectionSession] = None
        self._closed: bool = False
        self._listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        self._ws_ap: Dict = {}

    async def __aenter__(self):
        _log.debug("__aenter__")
        await self._async_setup_hook()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        _log.debug("__aexit__")

        if not self.is_closed():
            await self.close()

    @property
    def robot(self):
        return self._connection.connect_state.robot

    async def close(self) -> None:
        """关闭client相关的连接"""

        if self._closed:
            return

        self._closed = True

    def is_closed(self) -> bool:
        """:class:`bool`: Indicates if the websocket connection is closed."""
        return self._closed

    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

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
        ret_coro: :class:`bool`
            是否需要返回协程对象
        """
        # login后再进行后面的操作
        token = Token(appid, token)
        self.ret_coro = ret_coro

        await self._login(token)
        return await self._init(token)

    async def _login(self, token: Token) -> None:
        _log.info("[连接管理]登录机器人账号中...")

        if self.loop is _loop:
            await self._async_setup_hook()

        # 通过api获取websocket链接
        ws_api = AsyncWebsocketAPI(token)
        self._ws_ap = await ws_api.ws()

    async def _init(self, token):
        _log.info("[连接管理]程序启动...")
        # 每个机器人创建的连接数不能超过remaining剩余连接数
        if self._ws_ap["shards"] > self._ws_ap["session_start_limit"]["remaining"]:
            raise Exception("session limit exceeded")

        # 根据session限制建立链接
        concurrency = self._ws_ap["session_start_limit"]["max_concurrency"]
        session_interval = round(5 / concurrency)

        # 根据限制建立分片的并发链接数
        _log.debug(f'session_interval: {session_interval}, shards: {self._ws_ap["shards"]}, intents: {self.intents}')
        return await self._pool_init(token.bot_token(), session_interval)

    async def _pool_init(self, token, session_interval):
        # 实例一个session_pool
        self._connection = ConnectionSession(
            max_async=self._ws_ap["session_start_limit"]["max_concurrency"],
            connect=self.connect,
            dispatch=self.dispatch,
            loop=asyncio.get_event_loop(),
        )
        for i in range(self._ws_ap["shards"]):
            session = {
                "session_id": "",
                "last_seq": 0,
                "intent": self.intents,
                "token": token,
                "url": self._ws_ap["url"],
                "shards": {"shard_id": i, "shard_count": self._ws_ap["shards"]},
            }
            self._connection.add(session)

        loop = self._connection._loop
        loop.set_exception_handler(_loop_exception_handler)

        try:
            # 返回协程对象，交由开发者自行调控
            if self.ret_coro:
                return self._connection.run(session_interval)
            else:
                await self._connection.run(session_interval)
        except KeyboardInterrupt:
            _log.info("[连接管理]服务强行停止!")
            # cancel all tasks lingering

    async def connect(self, session):
        """
        newConnect 启动一个新的连接，如果连接在监听过程中报错了，或者被远端关闭了链接，需要识别关闭的原因，能否继续 resume
        如果能够 resume，则往 sessionChan 中放入带有 sessionID 的 session
        如果不能，则清理掉 sessionID，将 session 放入 sessionChan 中
        session 的启动，交给 start 中的 for 循环执行，session 不自己递归进行重连，避免递归深度过深

        param session: session对象
        """
        _log.info("[连接管理]新会话启动中...")

        client = BotWebSocket(session, self._connection)
        try:
            await client.connect()
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            await client.on_error(e)

    def dispatch(self, event: str, *args: Any, **kwargs: Any) -> None:
        """分发ws的下行事件

        解析client类的on_event事件，进行对应的事件回调
        """
        _log.debug("dispatching event %s", event)
        method = "on_" + event

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
