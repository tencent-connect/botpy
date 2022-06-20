# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging

from botpy.user import Member
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_guild_member_add(self, member: Member):
        _log.info("%s 加入频道" % member.nick)

    async def on_guild_member_update(self, member: Member):
        _log.info("%s 更新了资料" % member.nick)

    async def on_guild_member_remove(self, member: Member):
        _log.info("%s 退出了频道" % member.nick)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(guild_members=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
