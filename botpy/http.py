# -*- coding: utf-8 -*-
import asyncio
from json.decoder import JSONDecodeError
from typing import Any, Optional, ClassVar, Union, Dict

import aiohttp
from aiohttp import ClientResponse, FormData, ClientTimeout, TCPConnector
from ssl import SSLContext

from . import logging
from .errors import HttpErrorDict, ServerError
from .robot import Token
from .types import robot

X_TPS_TRACE_ID = "X-Tps-trace-Id"

_log = logging.get_logger()

# 请求成功的返回码
HTTP_OK_STATUS = [200, 202, 204]


async def _handle_response(url, response: ClientResponse) -> Union[Dict[str, Any], str]:
    try:
        condition = response.headers["content-type"] == "application/json"
        # note that when content-type is application/json, aiohttp will directly auto-sub encoding to be utf-8
        data = await response.json() if condition else await response.text()
    except (KeyError, JSONDecodeError):
        data = None
    if response.status in HTTP_OK_STATUS:
        _log.debug(f"[botpy] 请求成功, 请求连接: {url}, 返回内容: {data}, trace_id:{response.headers.get(X_TPS_TRACE_ID)}")
        return data
    else:
        _log.error(
            f"[botpy] 接口请求异常，请求连接: {url}, "
            f"错误代码: {response.status}, 返回内容: {data}, trace_id:{response.headers.get(X_TPS_TRACE_ID)}"
            # trace_id 用于定位接口问题
        )
        error_dict_get = HttpErrorDict.get(response.status)
        # type of data should be dict or str or None, so there should be a condition to check and prevent bug
        message = data["message"] if isinstance(data, dict) else str(data)
        if not error_dict_get:
            raise ServerError(message)
        raise error_dict_get(msg=message)


class Route:
    DOMAIN: ClassVar[str] = "api.sgroup.qq.com"
    SANDBOX_DOMAIN: ClassVar[str] = "sandbox.api.sgroup.qq.com"
    SCHEME: ClassVar[str] = "https"

    def __init__(self, method: str, path: str, is_sandbox: str = False, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.is_sandbox = is_sandbox
        self.parameters = parameters

    @property
    def url(self):
        if self.is_sandbox:
            d = self.SANDBOX_DOMAIN
        else:
            d = self.DOMAIN
        _url = "{}://{}{}".format(self.SCHEME, d, self.path)

        # path的参数:
        if self.parameters:
            _url = _url.format_map(self.parameters)
        return _url


class BotHttp:
    """
    TODO 增加请求重试功能 @veehou
    TODO 增加并发请求的锁控制 @veehou
    """

    def __init__(self, timeout: int, is_sandbox: bool = False, app_id: str = None, token: str = None):
        self.timeout = timeout
        self.is_sandbox = is_sandbox

        self._token: Optional[Token] = None if not app_id else Token(app_id=app_id, access_token=token)
        self._session: Optional[aiohttp.ClientSession] = None
        self._global_over: Optional[asyncio.Event] = None
        self._headers: Optional[dict] = None

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def check_session(self):
        if not self._headers:
            self._headers = {
                "Authorization": f"{self._token.get_type()} {self._token.get_string()}",
                "User-Agent": "botpy/v1",
            }

        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self._headers,
                timeout=ClientTimeout(self.timeout),
                connector=TCPConnector(limit=500, ssl=SSLContext()),
            )

    async def request(self, route: Route, **kwargs: Any):
        # some checking if it's a JSON request
        if "json" in kwargs:
            json_ = kwargs["json"]
            json__get = json_.get("file_image")
            if json__get and isinstance(json__get, bytes):
                kwargs["data"] = FormData()
                for k, v in kwargs.pop("json").items():
                    if v:
                        kwargs["data"].add_field(k, v)

        await self.check_session()
        route.is_sandbox = self.is_sandbox
        _log.debug(f"[botpy] 请求头部: {self._headers}, 请求方式: {route.method}, 请求url: {route.url}")

        async with self._session.request(method=route.method, url=route.url, **kwargs) as response:
            return await _handle_response(route.url, response)

    async def login(self, token: Token) -> robot.Robot:
        """login后保存token和session"""

        self._token = token
        await self.check_session()
        self._global_over = asyncio.Event()
        self._global_over.set()

        data = await self.request(Route("GET", "/users/@me"))
        # TODO 检查机器人token错误的raise exception @veehou

        return data
