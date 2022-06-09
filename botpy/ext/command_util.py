# -*- coding: utf-8 -*-
from functools import wraps

from botpy.message import Message


class Commands:
    """
    指令装饰器
    """

    def __init__(self, commands: tuple or str):
        self.commands = commands

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            message: Message = kwargs["message"]
            if isinstance(self.commands, tuple):
                for command in self.commands:
                    if self.commands in message.content:
                        # 分割指令后面的指令参数
                        params = message.content.split(self.commands)[1].strip()
                        return await func(message=message, params=params)
            elif isinstance(self.commands, str):
                # 分割指令后面的指令参数
                params = message.content.split(self.command)[1].strip()
                return await func(message=message, params=params)
            else:
                return False

        return decorated

