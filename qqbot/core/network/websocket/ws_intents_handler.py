# -*- coding: utf-8 -*-

from enum import Enum

from qqbot.core.network.websocket.ws_event import WsEvent
from qqbot.core.network.websocket.ws_event_handler import DefaultHandler


class Handler:
    def __init__(self, handler_type, callback):
        self.type = handler_type
        self.callback = callback


def register_handlers(handlers):
    """
    RegisterHandlers 注册事件回调，并返回 intent 用于 websocket 的鉴权
    """
    intent = 0

    for handler in handlers:
        call_handler = intent_handler_dict.get(handler.type.value)
        intent = intent | call_handler(handler.callback, intent)

    return intent


def plain_event_handler(callback, intent):
    DefaultHandler.plain = callback
    return intent


def guild_event_handler(callback, intent):
    DefaultHandler.guild = callback
    intent = intent | WsEvent.event_to_intent(
        WsEvent.EventGuildCreate, WsEvent.EventGuildDelete, WsEvent.EventGuildUpdate
    )
    return intent


def guild_member_event_handler(callback, intent):
    DefaultHandler.guild_member = callback
    intent = intent | WsEvent.event_to_intent(
        WsEvent.EventGuildMemberAdd,
        WsEvent.EventGuildMemberRemove,
        WsEvent.EventGuildMemberUpdate,
    )
    return intent


def audio_event_handler(callback, intent):
    DefaultHandler.audio = callback
    intent = intent | WsEvent.event_to_intent(
        WsEvent.EventAudioStart,
        WsEvent.EventAudioFinish,
        WsEvent.EventAudioOnMic,
        WsEvent.EventAudioOffMic,
    )
    return intent


def channel_event_handler(callback, intent):
    DefaultHandler.channel = callback
    intent = intent | WsEvent.event_to_intent(
        WsEvent.EventChannelCreate,
        WsEvent.EventChannelDelete,
        WsEvent.EventChannelUpdate,
    )
    return intent


def message_event_handler(callback, intent):
    DefaultHandler.message = callback
    intent = intent | WsEvent.event_to_intent(WsEvent.EventMessageCreate)
    return intent


def at_message_event_handler(callback, intent):
    DefaultHandler.at_message = callback
    intent = intent | WsEvent.event_to_intent(WsEvent.EventAtMessageCreate)
    return intent


def direct_message_event_handler(callback, intent):
    DefaultHandler.direct_message = callback
    intent = intent | WsEvent.event_to_intent(WsEvent.EventDirectMessageCreate)
    return intent


class HandlerType(Enum):
    PLAIN_EVENT_HANDLER = 0
    GUILD_EVENT_HANDLER = 1
    GUILD_MEMBER_EVENT_HANDLER = 2
    CHANNEL_EVENT_HANDLER = 3
    MESSAGE_EVENT_HANDLER = 4
    AT_MESSAGE_EVENT_HANDLER = 5
    DIRECT_MESSAGE_EVENT_HANDLER = 6
    AUDIO_EVENT_HANDLER = 7


intent_handler_dict = {
    HandlerType.PLAIN_EVENT_HANDLER.value: plain_event_handler,
    HandlerType.GUILD_EVENT_HANDLER.value: guild_event_handler,
    HandlerType.GUILD_MEMBER_EVENT_HANDLER.value: guild_member_event_handler,
    HandlerType.CHANNEL_EVENT_HANDLER.value: channel_event_handler,
    HandlerType.MESSAGE_EVENT_HANDLER.value: message_event_handler,
    HandlerType.AT_MESSAGE_EVENT_HANDLER.value: at_message_event_handler,
    HandlerType.DIRECT_MESSAGE_EVENT_HANDLER.value: direct_message_event_handler,
    HandlerType.AUDIO_EVENT_HANDLER.value: audio_event_handler,
}
