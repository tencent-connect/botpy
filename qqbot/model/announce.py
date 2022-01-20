# -*- coding: utf-8 -*-


class Announce:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.message_id: str = ""
        if data:
            self.__dict__ = data


class CreateAnnounceRequest:
    def __init__(self, channel_id: str, message_id: str):
        self.channel_id = channel_id
        self.message_id = message_id


class CreateChannelAnnounceRequest:
    def __init__(self, message_id: str):
        self.message_id = message_id
