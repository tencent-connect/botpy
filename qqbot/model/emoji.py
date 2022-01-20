# -*- coding: utf-8 -*-


class Emoji:
    def __init__(self, data=None):
        self.id: str = ""
        self.type: EmojiType = EmojiType()
        if data:
            self.__dict__ = data


class EmojiType:
    system = 1
    emoji = 2
