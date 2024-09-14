# -*- coding: utf-8 -*-
import re
from functools import wraps
from typing import Tuple

class Commands:
    """
    指令装饰器

    Args:
      args (tuple): 字符串元组。
    """

    def __init__(self, *args):
        self.commands = args
        # 构建正则表达式模式
        self.pattern = re.compile(rf"({'|'.join(self.commands)})(?:\s+(.*))?")

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            message: BaseMessage = kwargs["message"]
            match = self.pattern.match(message.content)
            if match:
                command, params = match.groups()
                if params:
                    kwargs["params"] = params.strip()
                return await func(*args, **kwargs)
            return False

        return decorated
