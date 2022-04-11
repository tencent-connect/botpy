# -*- coding: utf-8 -*-
import json

import requests

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
    ACCEPTED = 202
    NO_CONTENT = 204


def _handle_response(api_url, response):
    if response.status_code in (
        HttpStatus.NO_CONTENT,
        HttpStatus.OK,
        HttpStatus.ACCEPTED,
    ):
        return
    else:
        logger.error(
            "[HTTP]接口请求异常，请求连接: %s, error: %s, 返回内容: %s, trace_id:%s"
            % (
                api_url,
                response.status_code,
                response.content,
                response.headers.get(X_TPS_TRACE_ID),
            )  # trace_id 用于定位接口问题
        )
        error_message_: HttpErrorMessage = json.loads(
            response.content, object_hook=HttpErrorMessage
        )
        error_dict_get = HttpErrorDict.get(response.status_code)
        if error_dict_get is None:
            raise ServerError(error_message_.message)
        raise error_dict_get(msg=error_message_.message)


class Http:
    def __init__(self, time_out, token, type):
        self.timeout = time_out
        self.token = token
        self.scheme = type

    def get(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug("[HTTP]http get headers: %s, api_url: %s" % (headers, api_url))
        response = requests.get(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        )
        _handle_response(api_url, response)
        return response

    def post(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "[HTTP]http post headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        response = requests.post(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        )
        _handle_response(api_url, response)
        return response

    def delete(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug("[HTTP]http delete headers: %s, api_url: %s" % (headers, api_url))
        response = requests.delete(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        )
        _handle_response(api_url, response)
        return response

    def put(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "[HTTP]http put headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        response = requests.put(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        )
        _handle_response(api_url, response)
        return response

    def patch(self, api_url, request=None, params=None):
        headers = {
            "Authorization": self.scheme + " " + self.token,
            "User-Agent": "BotPythonSDK/v0.5.4",
        }
        logger.debug(
            "[HTTP]http patch headers: %s, api_url: %s, request: %s"
            % (headers, api_url, request)
        )
        response = requests.patch(
            url=api_url,
            params=params,
            json=request,
            timeout=self.timeout,
            headers=headers,
        )
        _handle_response(api_url, response)
        return response
