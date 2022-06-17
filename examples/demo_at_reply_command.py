# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


@Commands(name=("你好", "hello"))
async def hello(api: BotAPI, message: Message, params=None):
    _log.info(params)
    # 第一种用reply发送消息
    await message.reply(content=params)
    # 第二种用api.post_message发送消息
    await api.post_message(channel_id=message.channel_id, content=params, msg_id=message.id)
    return True


@Commands("晚安")
async def good_night(api: BotAPI, message: Message, params=None):
    _log.info(params)
    # 第一种用reply发送消息
    await message.reply(content=params)
    # 第二种用api.post_message发送消息
    await api.post_message(channel_id=message.channel_id, content=params, msg_id=message.id)
    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            hello,
            good_night,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return



if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
