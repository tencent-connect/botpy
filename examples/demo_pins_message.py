# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
        if "/获取精华列表" in message.content:
            pins_message = await self.api.get_pins(message.channel_id)
            _log.info(pins_message)

        if "/创建精华消息" in message.content:
            pins_message = await self.api.put_pin(message.channel_id, message.id)
            _log.info(pins_message)

        if "/删除精华消息" in message.content:
            result = await self.api.delete_pin(message.channel_id, message.id)
            _log.info(result)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
