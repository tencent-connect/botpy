from .api import BotAPI
from .types import guild, gateway


class Guild:
    __slots__ = (
        "_api",
        "_ctx",
        "id",
        "name",
        "icon",
        "owner_id",
        "is_owner",
        "member_count",
        "max_members",
        "description",
        "joined_at",
    )

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: guild.GuildPayload):
        self._api = api
        self._ctx = ctx

        self.id = data.get("id")
        self.name = data.get("name")
        self.icon = data.get("icon")
        self.owner_id = data.get("owner_id")
        self.is_owner = data.get("owner", False)
        self.member_count = data.get("member_count")
        self.max_members = data.get("max_members")
        self.description = data.get("description")
        self.joined_at = data.get("joined_at")
