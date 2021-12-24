# -*- coding: utf-8 -*-

import json

from qqbot.core.network.websocket.ws_event import WsEvent
from qqbot.core.util import logging
from qqbot.model.audio import AudioAction
from qqbot.model.channel import Channel
from qqbot.model.guild import Guild
from qqbot.model.guild_member import GuildMember
from qqbot.model.message import Message

logger = logging.getLogger(__name__)


class DefaultHandler:
    """
    持有handler的实例
    """

    plain = None
    guild = None
    guild_member = None
    channel = None
    message = None
    at_message = None
    direct_message = None
    audio = None


def parse_and_handle(message_event, message):
    event_type = message_event["t"]
    call_handler = event_handler_dict.get(event_type)

    if call_handler is None:
        if DefaultHandler.plain is not None:
            plain = DefaultHandler.plain
            plain(event_type, message)
        else:
            return
    else:
        call_handler(event_type, message)


def _handle_event_guild(message_event, message):
    callback = DefaultHandler.guild
    if callback is None:
        return
    guild: Guild = json.loads(_parse_data(message), object_hook=Guild)
    callback(message_event, guild)


def _handle_event_channel(message_event, message):
    callback = DefaultHandler.channel
    if callback is None:
        return
    channel: Channel = json.loads(_parse_data(message), object_hook=Channel)
    callback(message_event, channel)


def _handle_event_guild_member(message_event, message):
    callback = DefaultHandler.guild_member
    if callback is None:
        return
    guild_member: GuildMember = json.loads(
        _parse_data(message), object_hook=GuildMember
    )
    callback(message_event, guild_member)


def _handle_event_at_message_create(message_event, message):
    callback = DefaultHandler.at_message
    if callback is None:
        return
    at_message: Message = json.loads(_parse_data(message), object_hook=Message)
    callback(message_event, at_message)


def _handle_event_message_create(message_event, message):
    callback = DefaultHandler.message
    if callback is None:
        return
    msg: Message = json.loads(_parse_data(message), object_hook=Message)
    callback(message_event, msg)


def _handle_event_direct_message_create(message_event, message):
    callback = DefaultHandler.direct_message
    if callback is None:
        return
    msg: Message = json.loads(_parse_data(message), object_hook=Message)
    callback(message_event, msg)


def _handle_event_audio(message_event, message):
    callback = DefaultHandler.audio
    if callback is None:
        return
    audio_action: AudioAction = json.loads(
        _parse_data(message), object_hook=AudioAction
    )
    callback(message_event, audio_action)


event_handler_dict = {
    WsEvent.EventGuildCreate: _handle_event_guild,
    WsEvent.EventGuildUpdate: _handle_event_guild,
    WsEvent.EventGuildDelete: _handle_event_guild,
    WsEvent.EventChannelCreate: _handle_event_channel,
    WsEvent.EventChannelUpdate: _handle_event_channel,
    WsEvent.EventChannelDelete: _handle_event_channel,
    WsEvent.EventGuildMemberAdd: _handle_event_guild_member,
    WsEvent.EventGuildMemberUpdate: _handle_event_guild_member,
    WsEvent.EventGuildMemberRemove: _handle_event_guild_member,
    WsEvent.EventAtMessageCreate: _handle_event_at_message_create,
    WsEvent.EventMessageCreate: _handle_event_message_create,
    WsEvent.EventDirectMessageCreate: _handle_event_direct_message_create,
    WsEvent.EventAudioStart: _handle_event_audio,
    WsEvent.EventAudioFinish: _handle_event_audio,
    WsEvent.EventAudioOnMic: _handle_event_audio,
    WsEvent.EventAudioOffMic: _handle_event_audio,
}


def _parse_data(message):
    json_obj = json.loads(message)
    if "d" in json_obj.keys():
        data = json_obj["d"]
        return json.dumps(data)
