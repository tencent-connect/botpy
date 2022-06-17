# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.types.announce import AnnouncesType
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        _log.info(f"{self.robot.name}receive message {message.content}")

        # 先发送消息告知用户
        await self.api.post_message(message.channel_id, content="command received: %s" % message.content)

        # 输入/xxx后的处理
        message_id = "088de19cbeb883e7e97110a2e39c0138d401"
        if "/建公告" in message.content:
            await self.api.create_announce(message.guild_id, message.channel_id, message_id)

        elif "/删公告" in message.content:
            await self.api.delete_announce(message.guild_id, message_id)

        elif "/设置推荐子频道" in message.content:
            channel_list = [{"channel_id": message.channel_id, "introduce": "introduce"}]
            await self.api.create_recommend_announce(message.guild_id, AnnouncesType.MEMBER, channel_list)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
