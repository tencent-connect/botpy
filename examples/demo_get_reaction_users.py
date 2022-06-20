# -*- coding: utf-8 -*-
import os
from typing import List

import botpy

from botpy.message import Message
from botpy.types import reaction
from botpy.types.user import User
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        users: List[User] = []
        cookie = ""
        while True:
            reactionUsers: reaction.ReactionUsers = await self.api.get_reaction_users(
                "2568610",
                "088de19cbeb883e7e97110a2e39c0138d80d48acfc879406",
                1,
                "4",
                cookie=cookie,
            )

            if not reactionUsers:
                break

            users.extend(reactionUsers["users"])

            if reactionUsers["is_end"]:
                break
            else:
                cookie = reactionUsers["cookie"]

        print(len(users))
        for user in users:
            print(user["username"])


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
