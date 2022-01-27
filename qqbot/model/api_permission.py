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
    def __init__(self, data=None):
        self.guild_id: str
        self.channel_id: str
        self.api_identify: APIPermissionDemandIdentify
        self.title: str
        self.desc: str
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
