# -*- coding: utf-8 -*-

from qqbot.core.network.websocket.dto.enum_intents import Intents


class WsEvent:
    EventGuildCreate = "GUILD_CREATE"
    EventGuildUpdate = "GUILD_UPDATE"
    EventGuildDelete = "GUILD_DELETE"
    EventChannelCreate = "CHANNEL_CREATE"
    EventChannelUpdate = "CHANNEL_UPDATE"
    EventChannelDelete = "CHANNEL_DELETE"

    EventGuildMemberAdd = "GUILD_MEMBER_ADD"
    EventGuildMemberUpdate = "GUILD_MEMBER_UPDATE"
    EventGuildMemberRemove = "GUILD_MEMBER_REMOVE"

    EventMessageCreate = "MESSAGE_CREATE"
    EventAtMessageCreate = "AT_MESSAGE_CREATE"
    EventDirectMessageCreate = "DIRECT_MESSAGE_CREATE"

    EventAudioStart = "AUDIO_START"
    EventAudioFinish = "AUDIO_FINISH"
    EventAudioOnMic = "AUDIO_ON_MIC"
    EventAudioOffMic = "AUDIO_OFF_MIC"

    # 事件map
    event_dirt = {
        EventGuildCreate: Intents.INTENT_GUILDS,
        EventGuildUpdate: Intents.INTENT_GUILDS,
        EventGuildDelete: Intents.INTENT_GUILDS,
        EventChannelCreate: Intents.INTENT_GUILDS,
        EventChannelUpdate: Intents.INTENT_GUILDS,
        EventChannelDelete: Intents.INTENT_GUILDS,
        EventGuildMemberAdd: Intents.INTENT_GUILD_MEMBERS,
        EventGuildMemberUpdate: Intents.INTENT_GUILD_MEMBERS,
        EventGuildMemberRemove: Intents.INTENT_GUILD_MEMBERS,
        EventMessageCreate: Intents.INTENT_GUILD_MESSAGES,
        EventAtMessageCreate: Intents.INTENT_GUILD_AT_MESSAGE,
        EventDirectMessageCreate: Intents.INTENT_DIRECT_MESSAGE,
        EventAudioStart: Intents.INTENT_AUDIO,
        EventAudioFinish: Intents.INTENT_AUDIO,
        EventAudioOnMic: Intents.INTENT_AUDIO,
        EventAudioOffMic: Intents.INTENT_AUDIO,
    }

    @staticmethod
    def event_to_intent(*events):
        intent = 0
        for event in events:
            intent = intent | WsEvent.event_dirt[event].value
        return intent

    @staticmethod
    def intent_to_event(intent_event_map):
        pass
