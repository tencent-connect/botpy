from qqbot.core.network.ws.ws_event import WsEvent


class DefaultHandler:
    """
    持有handler的实例
    """

    plain = None
    guild = None
    guild_member = None
    channel = None
    message_create = None
    message_delete = None
    at_message = None
    public_message_delete = None
    direct_message_create = None
    direct_message_delete = None
    audio = None
    message_reaction = None
    interaction_create = None

    @classmethod
    def get_handler_by_type(cls, event_type: str):
        if event_type in (
                WsEvent.EventGuildCreate,
                WsEvent.EventGuildUpdate,
                WsEvent.EventGuildDelete
        ):
            return cls.guild
        elif event_type in (
                WsEvent.EventChannelCreate,
                WsEvent.EventChannelUpdate,
                WsEvent.EventChannelDelete
        ):
            return cls.channel
        elif event_type in (
            WsEvent.EventGuildMemberAdd,
            WsEvent.EventGuildMemberUpdate,
            WsEvent.EventGuildMemberRemove,
        ):
            return cls.guild_member
        elif event_type == WsEvent.EventAtMessageCreate:
            return cls.at_message
        elif event_type == WsEvent.EventPublicMessageDelete:
            return cls.public_message_delete
        elif event_type == WsEvent.EventMessageCreate:
            return cls.message_create
        elif event_type == WsEvent.EventMessageDelete:
            return cls.message_delete
        elif event_type == WsEvent.EventDirectMessageCreate:
            return cls.direct_message_create
        elif event_type == WsEvent.EventDirectMessageDelete:
            return cls.direct_message_delete
        elif event_type in (
            WsEvent.EventAudioStart,
            WsEvent.EventAudioFinish,
            WsEvent.EventAudioOnMic,
            WsEvent.EventAudioOffMic,
        ):
            return cls.audio
        elif event_type in (
                WsEvent.EventMessageReactionAdd,
                WsEvent.EventMessageReactionRemove
        ):
            return cls.message_reaction
        elif event_type == WsEvent.EventInteractionCreate:
            return cls.interaction_create
