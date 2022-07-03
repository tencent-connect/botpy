from .api import BotAPI
from .types import audio


class Audio:
    __slots__ = (
        "_api",
        "_ctx",
        "channel_id",
        "guild_id",
        "audio_url",
        "text",
        "event_id")

    def __init__(self, api: BotAPI, event_id, data: audio.AudioAction):
        self._api = api

        self.channel_id = data.get("channel_id", None)
        self.guild_id = data.get("guild_id", None)
        self.audio_url = data.get("audio_url", None)
        self.text = data.get("text", None)
        self.event_id = event_id

    def __repr__(self):
        return str({items: str(getattr(self, items)) for items in self.__slots__ if not items.startswith('_')})
