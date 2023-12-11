# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.types.message import MarkdownPayload, MessageMarkdownParams
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def handle_send_markdown_by_template(self, channel_id, msg_id):
        params = [
            MessageMarkdownParams(key="title", values=["标题"]),
            MessageMarkdownParams(key="content", values=["为了成为一名合格的巫师，请务必阅读频道公告", "藏馆黑色魔法书"]),
        ]
        markdown = MarkdownPayload(custom_template_id="65", params=params)

        # 通过api发送回复消息
        await self.api.post_message(channel_id, markdown=markdown, msg_id=msg_id)

    async def handle_send_markdown_by_content(self, channel_id, msg_id):
        markdown = MarkdownPayload(content="# 标题 \n## 简介很开心 \n内容")
        # 通过api发送回复消息
        await self.api.post_message(channel_id, markdown=markdown, msg_id=msg_id)

    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
        await self.handle_send_markdown_by_template(message.channel_id, message.id)
        await self.handle_send_markdown_by_content(message.channel_id, message.id)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
