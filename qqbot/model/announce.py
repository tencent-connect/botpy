# -*- coding: utf-8 -*-
from typing import List


class Announce:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.message_id: str = ""
        self.announces_type: int = 0
        self.recommend_channels: List[RecommendChannel] = []
        if data:
            self.__dict__ = data


class RecommendChannel:
    def __init__(self, channel_id: str, introduce: str):
        self.channel_id = channel_id
        self.introduce = introduce


class CreateAnnounceRequest:
    def __init__(self, channel_id: str, message_id: str):
        self.channel_id = channel_id
        self.message_id = message_id


class CreateChannelAnnounceRequest:
    def __init__(self, message_id: str):
        self.message_id = message_id


class RecommendChannelRequest:
    def __init__(self, announces_type: int, recommend_channels: List[RecommendChannel]):
        self.announces_type = announces_type
        self.recommend_channels = recommend_channels
