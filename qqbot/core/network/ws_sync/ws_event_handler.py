# -*- coding: utf-8 -*-

import json

from qqbot.core.network.ws.ws_event import WsEvent
from qqbot.core.network.ws.ws_handler import DefaultHandler
from qqbot.core.util import logging
from qqbot.model.audio import AudioAction
from qqbot.model.channel import Channel
from qqbot.model.guild import Guild
from qqbot.model.guild_member import GuildMember
from qqbot.model.message import Message, DeletedMessageInfo
from qqbot.model.reaction import Reaction
from qqbot.model.interaction import Interaction
from qqbot.model.ws_context import WsContext

logger = logging.getLogger()


def parse_and_handle(ws_event, data):
    event_id = ws_event["id"]
    event_type = ws_event["t"]
    context = WsContext(event_type, event_id)
    call_handler = event_handler_dict.get(event_type)

    if call_handler is None:
        if DefaultHandler.plain is not None:
            plain = DefaultHandler.plain
            plain(context, data)
        else:
            return
    else:
        call_handler(context, data)


def _handle_event_guild(context, data):
    callback = DefaultHandler.guild
    if callback is None:
        return
    guild: Guild = json.loads(_parse_data(data), object_hook=Guild)
    callback(context, guild)


def _handle_event_channel(context, data):
    callback = DefaultHandler.channel
    if callback is None:
        return
    channel: Channel = json.loads(_parse_data(data), object_hook=Channel)
    callback(context, channel)


def _handle_event_guild_member(context, data):
    callback = DefaultHandler.guild_member
    if callback is None:
        return
    guild_member: GuildMember = json.loads(_parse_data(data), object_hook=GuildMember)
    callback(context, guild_member)


def _handle_event_at_message_create(context, data):
    callback = DefaultHandler.at_message
    if callback is None:
        return
    at_message: Message = json.loads(_parse_data(data), object_hook=Message)
    callback(context, at_message)


def _handle_event_public_message_delete(context, data):
    callback = DefaultHandler.public_message_delete
    if callback is None:
        return
    message_deletion_info: DeletedMessageInfo = json.loads(_parse_data(data), object_hook=DeletedMessageInfo)
    callback(context, message_deletion_info)


def _handle_event_message_create(context, data):
    callback = DefaultHandler.message_create
    if callback is None:
        return
    msg: Message = json.loads(_parse_data(data), object_hook=Message)
    callback(context, msg)


def _handle_event_message_delete(context, data):
    callback = DefaultHandler.message_delete
    if callback is None:
        return
    message_deletion_info: DeletedMessageInfo = json.loads(_parse_data(data), object_hook=DeletedMessageInfo)
    callback(context, message_deletion_info)


def _handle_event_direct_message_create(context, data):
    callback = DefaultHandler.direct_message_create
    if callback is None:
        return
    msg: Message = json.loads(_parse_data(data), object_hook=Message)
    callback(context, msg)


def _handle_event_direct_message_delete(context, data):
    callback = DefaultHandler.direct_message_delete
    if callback is None:
        return
    message_deletion_info: DeletedMessageInfo = json.loads(_parse_data(data), object_hook=DeletedMessageInfo)
    callback(context, message_deletion_info)


def _handle_event_audio(context, data):
    callback = DefaultHandler.audio
    if callback is None:
        return
    audio_action: AudioAction = json.loads(_parse_data(data), object_hook=AudioAction)
    callback(context, audio_action)


def _handle_event_message_reaction(context, data):
    callback = DefaultHandler.message_reaction
    if callback is None:
        return
    reaction: Reaction = json.loads(_parse_data(data), object_hook=Reaction)
    callback(context, reaction)


def _handle_event_interaction_create(context, data):
    callback = DefaultHandler.interaction_create
    if callback is None:
        return
    interaction: Interaction = json.loads(_parse_data(data), object_hook=Interaction)
    callback(context, interaction)


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
    WsEvent.EventPublicMessageDelete: _handle_event_public_message_delete,
    WsEvent.EventMessageCreate: _handle_event_message_create,
    WsEvent.EventMessageDelete: _handle_event_message_delete,
    WsEvent.EventDirectMessageCreate: _handle_event_direct_message_create,
    WsEvent.EventDirectMessageDelete: _handle_event_direct_message_delete,
    WsEvent.EventAudioStart: _handle_event_audio,
    WsEvent.EventAudioFinish: _handle_event_audio,
    WsEvent.EventAudioOnMic: _handle_event_audio,
    WsEvent.EventAudioOffMic: _handle_event_audio,
    WsEvent.EventMessageReactionAdd: _handle_event_message_reaction,
    WsEvent.EventMessageReactionRemove: _handle_event_message_reaction,
    WsEvent.EventInteractionCreate: _handle_event_interaction_create,
}


def _parse_data(message):
    json_obj = json.loads(message)
    if "d" in json_obj.keys():
        data = json_obj["d"]
        return json.dumps(data)
