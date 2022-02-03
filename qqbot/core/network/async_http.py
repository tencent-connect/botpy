# -*- coding: utf-8 -*-
import json

from aiohttp import ClientResponse

from qqbot.core.exception.error import (
    AuthenticationFailedError,
    NotFoundError,
    MethodNotAllowedError,
    SequenceNumberError,
    ServerError,
)
from qqbot.core.util import logging

X_TPS_TRACE_ID = "X-Tps-trace-Id"

logger = logging.getLogger()

HttpErrorDict = {
    401: AuthenticationFailedError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    429: SequenceNumberError,
    500: ServerError,
    504: ServerError,
}


class HttpErrorMessage:
    def __init__(self, data=None):
        self.message = ""
        self.code = 0
        if data is not None:
            self.__dict__ = data


class HttpStatus:
    OK = 200
    ACCEPTED = 200
    NO_CONTENT = 204


def _handle_response(api_url, response: ClientResponse, content: str):
    if response.status in (HttpStatus.NO_CONTENT, HttpStatus.OK, HttpStatus.ACCEPTED):
        return
    else:
        logger.error(
            "http request error with api_url:%s, error: %s, content: %s, trace_id:%s"
            % (
                api_url,
                response.status,
                content,
                response.headers.get(X_TPS_TRACE_ID),
            )  # trace_id 用于定位接口问题
        )
        error_message_: HttpErrorMessage = json.loads(
            content, object_hook=HttpErrorMessage
        )
        error_dict_get = HttpErrorDict.get(response.status)
        if error_dict_get is None:
            raise ServerError(error_message_.message)
        raise error_dict_get(msg=error_message_.message)


class AsyncHttp:
    def __init__(self, session, time_out, token, type):
        self.timeout = time_out
        self.token = token
        self.scheme = type
        self.session = session

    async def get(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug("http get headers: %s, api_url: %s" % (headers, api_url))
        async with self.session.get(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        ) as resp:
            content = await resp.text()
            _handle_response(api_url, resp, content)
            return content

    async def post(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "http post headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        async with self.session.post(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        ) as resp:
            content = await resp.text()
            _handle_response(api_url, resp, content)
            return content

    async def delete(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug("http delete headers: %s, api_url: %s" % (headers, api_url))
        async with self.session.delete(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        ) as resp:
            content = await resp.text()
            _handle_response(api_url, resp, content)
            return content

    async def put(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "http put headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        async with self.session.put(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        ) as resp:
            content = await resp.text()
            _handle_response(api_url, resp, content)
            return content

    async def patch(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "http patch headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        async with self.session.patch(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        ) as resp:
            content = await resp.text()
            _handle_response(api_url, resp, content)
            return content
