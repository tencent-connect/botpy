# -*- coding: utf-8 -*-
from typing import List


class Role:
    def __init__(self, data=None):
        self.id: str = ""
        self.name: str = ""
        self.color: int = 0
        self.hoist: int = 0
        self.number: int = 0
        self.number_limit: int = 0
        if data is not None:
            self.__dict__ = data


class GuildRoles:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.roles: List[Role] = [Role()]
        self.role_num_limit: str = ""
        if data is not None:
            self.__dict__ = data


class RoleUpdateRequest:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.filter: [RoleUpdateFilter] = None
        self.info: [RoleUpdateInfo] = None
        if data is not None:
            self.__dict__ = data


class RoleUpdateFilter:
    def __init__(self, name: int, color: int, hoist: int):
        self.name = name
        self.color = color
        self.hoist = hoist


class RoleUpdateInfo:
    def __init__(self, name: str, color: int, hoist: int):
        """
        身份组更新的信息

        :param name:名称
        :param color:ARGB的HEX十六进制颜色值转换后的十进制数值
        :param hoist:在成员列表中单独展示: 0-否, 1-是
        """
        self.name = name
        self.color = color
        self.hoist = hoist


class RoleUpdateResult:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.role_id: str = ""
        self.role: Role = Role()
        if data is not None:
            self.__dict__ = data
