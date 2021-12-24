# -*- coding: utf-8 -*-

from enum import Enum


class Intents(Enum):
    INTENT_GUILDS = 1 << 0
    # - GUILD_CREATE // 当机器人加入新guild时
    # - GUILD_UPDATE // 当guild资料发生变更时
    # - GUILD_DELETE // 当机器人退出guild时
    # - CHANNEL_CREATE // 当channel被创建时
    # - CHANNEL_UPDATE // 当channel被更新时
    # - CHANNEL_DELETE // 当channel被删除时

    INTENT_GUILD_MEMBERS = 1 << 1
    # - GUILD_MEMBER_ADD // 当成员加入时
    # - GUILD_MEMBER_UPDATE // 当成员资料变更时
    # - GUILD_MEMBER_REMOVE // 当成员被移除时

    INTENT_GUILD_MESSAGES = 1 << 9

    INTENT_DIRECT_MESSAGE = 1 << 12
    # - DIRECT_MESSAGE_CREATE // 当收到用户发给机器人的私信消息时

    INTENT_AUDIO = 1 << 29
    # - AUDIO_START           // 音频开始播放时
    # - AUDIO_FINISH          // 音频播放结束时
    # - AUDIO_ON_MIC          // 上麦时
    # - AUDIO_OFF_MIC         // 下麦时

    INTENT_GUILD_AT_MESSAGE = 1 << 30
    # - AT_MESSAGE_CREATE // 当收到 @ 机器人的消息时
