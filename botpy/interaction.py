from .api import BotAPI
from .types import interaction


class Interaction:
    __slots__ = (
        "_api",
        "_ctx",
        "id",
        "application_id",
        "type",
        "chat_type",
        "event_id",
        "data",
        "guild_id",
        "channel_id",
        "group_open_id",
        "timestamp",
        "version",
    )

    def __init__(self, api: BotAPI, event_id, data: interaction.InteractionPayload):
        self._api = api

        self.id = data.get("id", None)
        self.type = data.get("type", None)
        self.chat_type = data.get("chat_type", None)
        self.application_id = data.get("application_id", None)
        self.event_id = event_id
        self.data = self._Data(data.get("data", {}))
        self.guild_id = data.get("guild_id", None)
        self.channel_id = data.get("channel_id", None)
        self.group_open_id = data.get("group_open_id", None)
        self.timestamp = data.get("timestamp", None)
        self.version = data.get("version", None)

    def __repr__(self):
        return str({items: str(getattr(self, items)) for items in self.__slots__ if not items.startswith("_")})

    class _Data:
        def __init__(self, data):
            self.type = data.get("type", None)
            self.resolved = Interaction._Resolved(data.get("resolved", None))

        def __repr__(self):
            return str(self.__dict__)

    class _Resolved:
        def __init__(self, data):
            self.button_id = data.get("button_id", None)
            self.button_data = data.get("button_data", None)
            self.message_id = data.get("message_id", None)
            self.user_id = data.get("user_id", None)

        def __repr__(self):
            return str(self.__dict__)
