"""
对子频道转跳进行操作(#name)
注意:
1、无法识别真假转跳
2、当子频道重名时无法准确识别
3、当提供子频道转跳字段时请弃用本模块
"""

__all__ = [
    "get_channel_jump",
    "get_channel_jump_strict",
    "escape_channel_jump"
]

import re
from typing import List, Union, Match

from botpy import BotAPI
from botpy.message import Message

CHANNEL_JUMP_RE = re.compile(r"#(.{1,12}?)(?= )")


def get_channel_jump(text: str = None, message: Message = None) -> List[str]:
    """
    识别文本中的子频道转跳
    :param message: 消息对象
    :param text: 文本，为空则message.content
    :return: 子频道名称列表(不带#)
    """
    return CHANNEL_JUMP_RE.findall(message.content if text is None else text)


async def get_channel_jump_strict(api: BotAPI, message: Message = None, text: str = None,
                                  guild_id: str = None) -> List[str]:
    """
    识别文本中的子频道转跳，并过滤不存在的子频道
    :param api: BotAPI
    :param message: 消息对象
    :param text: 文本，为空则message.content
    :param guild_id: 频道id，为空则message.guild_id
    :return: 子频道名称列表(不带#)
    """
    channels = [channel["name"] for channel in await api.get_channels(guild_id or message.guild_id)]
    return [jump for jump in CHANNEL_JUMP_RE.findall(message.content if text is None else text) if jump in channels]


async def escape_channel_jump(api: BotAPI, message: Message = None, text: str = None, guild_id: str = None,
                              strict: bool = False) -> Union[str, bool]:
    """
    转义子频道转跳 (#name -> #<#id>)
    :param api: BotAPI
    :param message: 消息对象
    :param text: 文本，为空则message.content
    :param guild_id: 频道id，为空则message.guild_id
    :param strict: 是否严格模式(无不存在的子频道 返回false)
    :return: 转义后的文本
    """
    channels = await api.get_channels(guild_id or message.guild_id)

    def _escape(match: Match):
        for channel in channels:
            if channel["name"] == match.group(1):
                return "<#%s>" % channel["id"]
        else:
            if strict:
                raise ValueError
            else:
                return match.group(0)

    try:
        return CHANNEL_JUMP_RE.sub(_escape, message.content if text is None else text)
    except ValueError:
        return False
