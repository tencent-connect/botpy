# -*- coding: utf-8 -*-
from functools import wraps
from typing import Union

from botpy import BotAPI
from botpy.message import Message


class Commands:
    """
    指令装饰器

    Args:
      name (Union[tuple, str]): 字符串元组或单个字符串。
    """

    def __init__(self, name: Union[tuple, str]):
        self.commands = name

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            api: BotAPI = kwargs["api"]
            message: Message = kwargs["message"]
            if isinstance(self.commands, tuple):
                for command in self.commands:
                    if command in message.content:
                        # 分割指令后面的指令参数
                        params = message.content.split(command)[1].strip()
                        return await func(api=api, message=message, params=params)
            elif self.commands in message.content:
                # 分割指令后面的指令参数
                params = message.content.split(self.commands)[1].strip()
                return await func(api=api, message=message, params=params)
            else:
                return False

        return decorated

