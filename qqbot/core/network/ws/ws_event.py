# -*- coding: utf-8 -*-

from qqbot.core.network.ws.dto.enum_intents import Intents


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
    EventMessageDelete = "MESSAGE_DELETE"

    EventAtMessageCreate = "AT_MESSAGE_CREATE"
    EventPublicMessageDelete = "PUBLIC_MESSAGE_DELETE"

    EventDirectMessageCreate = "DIRECT_MESSAGE_CREATE"
    EventDirectMessageDelete = "DIRECT_MESSAGE_DELETE"

    EventAudioStart = "AUDIO_START"
    EventAudioFinish = "AUDIO_FINISH"
    EventAudioOnMic = "AUDIO_ON_MIC"
    EventAudioOffMic = "AUDIO_OFF_MIC"

    EventInteractionCreate = "INTERACTION_CREATE"

    EventMessageReactionAdd = "MESSAGE_REACTION_ADD"
    EventMessageReactionRemove = "MESSAGE_REACTION_REMOVE"

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
        EventMessageDelete: Intents.INTENT_GUILD_MESSAGES,
        EventAtMessageCreate: Intents.INTENT_PUBLIC_GUILD_MESSAGES,
        EventPublicMessageDelete: Intents.INTENT_PUBLIC_GUILD_MESSAGES,
        EventDirectMessageCreate: Intents.INTENT_DIRECT_MESSAGE,
        EventDirectMessageDelete: Intents.INTENT_DIRECT_MESSAGE,
        EventAudioStart: Intents.INTENT_AUDIO,
        EventAudioFinish: Intents.INTENT_AUDIO,
        EventAudioOnMic: Intents.INTENT_AUDIO,
        EventAudioOffMic: Intents.INTENT_AUDIO,
        EventInteractionCreate: Intents.INTERACTION,
        EventMessageReactionAdd: Intents.INTENT_MESSAGE_REACTION,
        EventMessageReactionRemove: Intents.INTENT_MESSAGE_REACTION,
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
