#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path
from typing import List

import qqbot
from qqbot import ReactionUsersPager, ReactionUsers
from qqbot.model.emoji import EmojiType
from qqbot.model.member import User
from qqbot.core.util.yaml_util import YamlUtil


test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    reaction_api = qqbot.AsyncReactionAPI(t_token, False)
    loop = asyncio.get_event_loop()

    pager = ReactionUsersPager()
    users: List[User] = []
    while True:
        reactionUsers: ReactionUsers = loop.run_until_complete(
            reaction_api.get_reaction_users('2568610', '088de19cbeb883e7e97110a2e39c0138d80d48acfc879406', EmojiType.system, "4", pager)
        )

        if not reactionUsers:
            break

        users.extend(reactionUsers.users)

        if reactionUsers.is_end:
            break
        else:
            pager.cookie = reactionUsers.cookie

    print(len(users))
    for user in users:
        print(user.username)
