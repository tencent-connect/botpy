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
    # - MESSAGE_CREATE         // 发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。内容与 AT_MESSAGE_CREATE 相同
    # - MESSAGE_DELETE         // 删除（撤回）消息事件

    INTENT_MESSAGE_REACTION = 1 << 10
    # - MESSAGE_REACTION_ADD    // 为消息添加表情表态
    # - MESSAGE_REACTION_REMOVE // 为消息删除表情表态

    INTENT_DIRECT_MESSAGE = 1 << 12
    # - DIRECT_MESSAGE_CREATE // 当收到用户发给机器人的私信消息时
    # - DIRECT_MESSAGE_DELETE   // 删除（撤回）消息事件

    INTERACTION = 1 << 26
    # - INTERACTION_CREATE // 互动事件创建时

    INTENT_AUDIO = 1 << 29
    # - AUDIO_START           // 音频开始播放时
    # - AUDIO_FINISH          // 音频播放结束时
    # - AUDIO_ON_MIC          // 上麦时
    # - AUDIO_OFF_MIC         // 下麦时

    INTENT_PUBLIC_GUILD_MESSAGES = 1 << 30
    # - AT_MESSAGE_CREATE // 当收到 @ 机器人的消息时
    # - PUBLIC_MESSAGE_DELETE   // 当频道的消息被删除时
