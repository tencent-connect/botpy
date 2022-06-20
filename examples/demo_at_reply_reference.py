# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.types.message import Reference
from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        # 构造消息发送请求数据对象
        message_reference = Reference(message_id=message.id)
        # 通过api发送回复消息
        await self.api.post_message(
            channel_id=message.channel_id,
            content="<emoji:4>这是一条引用消息",
            msg_id=message.id,
            message_reference=message_reference,
        )


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
