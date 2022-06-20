# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.message import Message
from botpy.types.message import Ark, ArkKv
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        # 两种方式构造消息发送请求数据对象
        payload: Ark = Ark(
            template_id=37,
            kv=[
                ArkKv(key="#METATITLE#", value="通知提醒"),
                ArkKv(key="#PROMPT#", value="标题"),
                ArkKv(key="#TITLE#", value="标题"),
                ArkKv(key="#METACOVER#", value="https://vfiles.gtimg.cn/vupload/20211029/bf0ed01635493790634.jpg"),
            ],
        )
        # payload = {
        #     "template_id": 37,
        #     "kv": [
        #         {"key": "#METATITLE#", "value": "通知提醒"},
        #         {"key": "#PROMPT#", "value": "标题"},
        #         {"key": "#TITLE#", "value": "标题"},
        #         {"key": "#METACOVER#", "value": "https://vfiles.gtimg.cn/vupload/20211029/bf0ed01635493790634.jpg"},
        #     ],
        # }

        await self.api.post_message(channel_id=message.channel_id, ark=payload)
        # await message.reply(ark=payload) # 这样也可以


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
