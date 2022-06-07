# -*- coding: utf-8 -*-
from functools import wraps

from botpy import logger
from botpy.message import Message


class Command:
    """
    指令装饰器
    """

    def __init__(self, command: tuple or str):
        self.command = command

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            message: Message = kwargs["message"]
            if isinstance(self.command, tuple):
                for command in self.command:
                    if self.command in message.content:
                        # 分割指令后面的指令参数
                        params = message.content.split(self.command)[1].strip()
                        return await func(message=message, params=params)
            elif isinstance(self.command, str):
                # 分割指令后面的指令参数
                params = message.content.split(self.command)[1].strip()
                return await func(message=message, params=params)
            else:
                return False

        return decorated
