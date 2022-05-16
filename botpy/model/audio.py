# -*- coding: utf-8 -*-


class STATUS:
    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3


class AudioControl:
    def __init__(self, audio_url: str, text: str, status: STATUS):
        self.audio_url = audio_url
        self.text = text
        self.status = status


class AudioAction:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.audio_url: str = ""
        self.text: str = ""
        if data is not None:
            self.__dict__ = data
