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
    event_id = ws_event["id"] if "id" in ws_event.keys() else ""
    event_type = ws_event["t"]
    context = WsContext(event_type, event_id)
    callback = DefaultHandler.get_handler_by_type(event_type)

    if callback is None:
        if DefaultHandler.plain is not None:
            plain = DefaultHandler.plain
            plain(context, data)
        else:
            return
    else:
        object_type = event_object_dict.get(event_type)
        resolved = json.loads(_parse_data(data), object_hook=object_type)
        callback(context, resolved)


event_object_dict = {
    WsEvent.EventGuildCreate: Guild,
    WsEvent.EventGuildUpdate: Guild,
    WsEvent.EventGuildDelete: Guild,
    WsEvent.EventChannelCreate: Channel,
    WsEvent.EventChannelUpdate: Channel,
    WsEvent.EventChannelDelete: Channel,
    WsEvent.EventGuildMemberAdd: GuildMember,
    WsEvent.EventGuildMemberUpdate: GuildMember,
    WsEvent.EventGuildMemberRemove: GuildMember,
    WsEvent.EventAtMessageCreate: Message,
    WsEvent.EventPublicMessageDelete: DeletedMessageInfo,
    WsEvent.EventMessageCreate: Message,
    WsEvent.EventMessageDelete: DeletedMessageInfo,
    WsEvent.EventDirectMessageCreate: Message,
    WsEvent.EventDirectMessageDelete: DeletedMessageInfo,
    WsEvent.EventAudioStart: AudioAction,
    WsEvent.EventAudioFinish: AudioAction,
    WsEvent.EventAudioOnMic: AudioAction,
    WsEvent.EventAudioOffMic: AudioAction,
    WsEvent.EventMessageReactionAdd: Reaction,
    WsEvent.EventMessageReactionRemove: Reaction,
    WsEvent.EventInteractionCreate: Interaction,
}


def _parse_data(data_dict):
    json_obj = json.loads(data_dict)
    if "d" in json_obj.keys():
        data = json_obj["d"]
        return json.dumps(data)
