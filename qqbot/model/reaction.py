from typing import List

from qqbot.model.member import User

from qqbot.model.emoji import Emoji


class Reaction:
    def __init__(self, data=None):
        self.user_id: str = ""
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.target: ReactionTarget = ReactionTarget()
        self.emoji: Emoji = Emoji()
        if data:
            self.__dict__ = data


class ReactionTarget:
    def __init__(self, data=None):
        self.id: str = ""
        self.type: int = 0
        if data:
            self.__dict__ = data


class ReactionUsers:
    def __init__(
            self,
            data=None,
            users: List[User] = None,
            cookie: str = None,
            is_end: bool = None
    ):
        if users:
            self.users = users
        if cookie:
            self.cookie = cookie
        if is_end:
            self.is_end = is_end
        if data:
            self.__dict__ = data


class ReactionUsersPager:
    def __init__(self, cookie: str = "", limit: int = 20):
        self.cookie = cookie
        self.limit = limit


class ReactionTargetType:
    message = 0
    feed = 1
    comment = 2
    reply = 3
