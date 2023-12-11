# -*- coding: utf-8 -*-
import os

import botpy
from botpy import BotAPI

from botpy.message import Message
from botpy.types.inline import Keyboard, Button, RenderData, Action, Permission, KeyboardRow
from botpy.types.message import MarkdownPayload, KeyboardPayload
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await send_template_keyboard(self.api, message)
        await send_self_defined_keyboard(self.api, message)


async def send_template_keyboard(api: BotAPI, message: Message):
    markdown = MarkdownPayload(content="# 123 \n 今天是个好天气")
    keyboard = KeyboardPayload(id="62")
    await api.post_keyboard_message(message.channel_id, markdown=markdown, keyboard=keyboard)


async def send_self_defined_keyboard(api: BotAPI, message: Message):
    markdown = MarkdownPayload(content="# 标题 \n## 简介 \n内容")
    keyboard = KeyboardPayload(content=build_a_demo_keyboard())
    await api.post_keyboard_message(message.channel_id, markdown=markdown, keyboard=keyboard)


def build_a_demo_keyboard() -> Keyboard:
    """
    创建一个只有一行且该行只有一个 button 的键盘
    """
    button1 = Button(
        id="1",
        render_data=RenderData(label="button", visited_label="BUTTON", style=0),
        action=Action(
            type=2,
            permission=Permission(type=2, specify_role_ids=["1"], specify_user_ids=["1"]),
            click_limit=10,
            data="/搜索",
            at_bot_show_channel_list=True,
        ),
    )

    row1 = KeyboardRow(buttons=[button1])
    return Keyboard(rows=[row1])


if __name__ == "__main__":
    # async的异步接口的使用示例
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
