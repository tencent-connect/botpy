#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy import logging

from botpy.interaction import Interaction
from botpy.ext.yaml_util import YamlUtil

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "qq-bot/config.yaml"))


_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_interaction_create(self, interaction: Interaction):
        # 暂时未开放互动事件
        pass


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(interaction=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
