# -*- coding: utf-8 -*-


class WebsocketError:
    CodeInvalidSession = 9001
    CodeConnCloseErr = 9005


class AuthenticationFailedError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs


class NotFoundError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs


class MethodNotAllowedError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs


class SequenceNumberError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs


class ServerError(RuntimeError):
    def __init__(self, msg):
        self.msgs = msg

    def __str__(self):
        return self.msgs
