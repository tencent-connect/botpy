from .api import BotAPI
from .types import gateway, audio


class Audio:
    __slots__ = (
        "_api",
        "_ctx",
        "channel_id",
        "guild_id",
        "audio_url",
        "text",
        "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: audio.AudioAction):
        self._api = api

        self.channel_id = data.get("channel_id")
        self.guild_id = data.get("guild_id")
        self.audio_url = data.get("audio_url")
        self.text = data.get("text")
        self.event_id = ctx.get("id")
