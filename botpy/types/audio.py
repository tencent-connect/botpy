# -*- coding: utf-8 -*-


class STATUS:
    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3


class AudioControl:
    audio_url: str
    text: str
    status: STATUS


class AudioAction:
    guild_id: str
    channel_id: str
    audio_url: str
    text: str
