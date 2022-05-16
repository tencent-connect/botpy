# -*- coding: utf-8 -*-
from typing import List


class PinsMessage:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.message_ids: List[str] = []
        if data:
            self.__dict__ = data
