# -*- coding: utf-8 -*-
from typing import List

from qqbot.model.guild_role import Role
from qqbot.model.member import User


class GuildMember:
    def __init__(self, data=None):
        self.user: [User] = None
        self.nick: str = ""
        self.roles: List[Role] = []
        self.joined_at: str = ""
        if data is not None:
            self.__dict__ = data


class QueryParams:
    def __init__(self, after: str, limit: int):
        self.after: str = after
        self.limit: int = limit
