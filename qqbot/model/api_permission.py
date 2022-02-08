# -*- coding: utf-8 -*-
from typing import List


class APIPermission:
    def __init__(self, data=None):
        self.path: str = ""
        self.method: str = ""
        self.desc: str = ""
        self.auth_status: int
        if data:
            self.__dict__ = data


class APIPermissionDemandIdentify:
    def __init__(self, path: str, method: str):
        self.path = path
        self.method = method


class APIPermissionDemand:
    def __init__(
        self,
        data=None,
        guild_id: str = None,
        channel_id: str = None,
        api_identify: APIPermissionDemandIdentify = None,
        title: str = None,
        desc: str = None,
    ):
        if guild_id:
            self.guild_id = guild_id
        if channel_id:
            self.channel_id = channel_id
        if api_identify:
            self.api_identify = api_identify
        if title:
            self.title = title
        if desc:
            self.desc = desc
        if data:
            self.__dict__ = data


class PermissionDemandToCreate:
    def __init__(
        self, channel_id: str, api_identify: APIPermissionDemandIdentify, desc: str = ""
    ):
        self.channel_id = channel_id
        self.api_identify = api_identify
        self.desc = desc


class APIs:
    def __init__(self, data=None):
        self.apis: List[APIPermission]
        if data:
            self.__dict__ = data
