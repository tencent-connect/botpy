# -*- coding: utf-8 -*-
from functools import wraps
from botpy.message import BaseMessage


class Commands:
    """
    指令装饰器

    Args:
      args (tuple): 字符串元组。
    """

    def __init__(self, *args):
        self.commands = args

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            message: BaseMessage = kwargs["message"]
            for command in self.commands:
                if command in message.content:
                    # 剔除消息文本中@机器人的字符串
                    content = message.content.replace(f"<@!{(await message.api.me())['id']}>", "")
                    content_split = content.lstrip().split(command)
                    # 当指令出现在消息文本（已剔除@机器人的信息）的开头执行指令
                    if len(content_split[0]) == 0:
                        # 分割指令后面的指令参数
                        kwargs["params"] = content_split[1].strip()
                        return await func(*args, **kwargs)
            return False

        return decorated

