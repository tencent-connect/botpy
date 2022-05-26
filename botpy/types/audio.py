# -*- coding: utf-8 -*-
from typing import TypedDict, Literal


"""
START = 0
PAUSE = 1
RESUME = 2
STOP = 3
"""
AudioStatus = Literal[0, 1, 2, 3]


class AudioControl(TypedDict):
    audio_url: str
    text: str
    status: AudioStatus


class AudioAction(TypedDict):
    guild_id: str
    channel_id: str
    audio_url: str
    text: str
