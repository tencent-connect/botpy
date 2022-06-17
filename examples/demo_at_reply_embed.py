# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.types.message import Embed, EmbedField
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        # 构造消息发送请求数据对象
        embed = Embed(
            title="embed消息",
            prompt="消息透传显示",
            fields=[
                EmbedField(name="<@!1234>hello world"),
                EmbedField(name="<@!1234>hello world"),
            ],
        )

        # embed = {
        #     "title": "embed消息",
        #     "prompt": "消息透传显示",
        #     "fields": [
        #         {"name": "<@!1234>hello world"},
        #         {"name": "<@!1234>hello world"},
        #     ],
        # }

        await self.api.post_message(channel_id=message.channel_id, embed=embed)
        # await message.reply(embed=embed) # 这样也可以


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
