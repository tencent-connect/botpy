# -*- coding: utf-8 -*-


class User:
    def __init__(self, data=None):
        self.id: str = ""
        self.username: str = ""
        self.avatar: str = ""
        self.bot: bool = False
        self.union_openid: str = ""
        self.union_user_account: str = ""
        if data is not None:
            self.__dict__ = data


class Member:
    def __init__(self, data=None):
        self.user: User = User()
        self.nick: str = ""
        self.roles = [""]
        self.joined_at: str = ""
        if data is not None:
            self.__dict__ = data


class MemberWithGuildID:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.user: User = User()
        self.nick: str = ""
        self.roles: [str] = [""]
        self.joined_at: str = ""
        if data is not None:
            self.__dict__ = data
