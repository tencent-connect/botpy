# -*- coding: utf-8 -*-
import asyncio
import json
from typing import Any, Optional, ClassVar, Union, Dict
from urllib.parse import quote

import aiohttp
from aiohttp import ClientResponse

from .utils import JsonUtil
from .errors import HttpErrorDict, ServerError
from .robot import Token
from .logging import logging
from .types import robot

X_TPS_TRACE_ID = "X-Tps-trace-Id"

logger = logging.getLogger()


class HttpErrorMessage:
    def __init__(self, data=None):
        self.message = ""
        self.code = 0
        if data is not None:
            self.__dict__ = data


class HttpStatus:
    OK = 200
    ACCEPTED = 202
    NO_CONTENT = 204


async def _handle_response(url, response: ClientResponse) -> Union[Dict[str, Any], str]:
    data = await _json_or_text(response)
    if response.status in (HttpStatus.NO_CONTENT, HttpStatus.OK, HttpStatus.ACCEPTED):
        logger.debug(f"[HTTP]请求成功, 请求连接: {url}, 返回内容: {data}")
        return data
    else:
        logger.error(
            f"[HTTP]接口请求异常，请求连接: {url},"
            f" error code: {response.status}, 返回内容: {data}, trace_id:{response.headers.get(X_TPS_TRACE_ID)}"
            # trace_id 用于定位接口问题
        )
        error_dict_get = HttpErrorDict.get(response.status)
        if error_dict_get is None:
            raise ServerError(data["message"])
        raise error_dict_get(msg=data["message"])


async def _json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json" and text:
            return json.loads(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text


class Route:
    DOMAIN: ClassVar[str] = "api.sgroup.qq.com"
    SANDBOX_DOMAIN: ClassVar[str] = "sandbox.api.sgroup.qq.com"
    SCHEME: ClassVar[str] = "https"

    def __init__(self, method: str, path: str, is_sandbox: str = False, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.is_sandbox = is_sandbox

        if self.is_sandbox:
            d = self.SANDBOX_DOMAIN
        else:
            d = self.DOMAIN
        self._url = "{}://{}{}".format(self.SCHEME, d, self.path)

        # path的参数:
        if parameters:
            self._url = self._url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})

    @property
    def url(self):
        return self._url


class BotHttp:
    """
    TODO 增加请求重试功能
    TODO 增加并发请求的锁控制
    """

    def __init__(
        self,
        timeout: int,
        is_sandbox: str = False,
    ):
        self.timeout = timeout
        self.is_sandbox = is_sandbox

        self._token: Optional[Token] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._global_over: Optional[asyncio.Event] = None

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def request(self, route: Route, **kwargs: Any):
        headers = {
            "Authorization": f"{self._token.get_type()} {self._token.get_string()}",
            "User-Agent": "botpy/v1",
        }
        # some checking if it's a JSON request
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = JsonUtil.dict2json(kwargs.pop("json"))

        kwargs["headers"] = headers

        logger.debug(f"[HTTP] request headers: {headers}, method: {route.method}, api_url: {route.url}")
        async with self._session.request(method=route.method, url=route.url, **kwargs) as response:
            return await _handle_response(route.url, response)

    async def login(self, token: Token) -> robot.Robot:
        """login后保存token和session"""

        self._session = aiohttp.ClientSession()
        self._global_over = asyncio.Event()
        self._global_over.set()

        self._token = token

        data = await self.request(Route("GET", "/users/@me"))
        # TODO 检查机器人token错误的raise exception

        return data