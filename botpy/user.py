from .api import BotAPI
from .types import user, gateway


class Member:
    __slots__ = (
        "_api",
        "_ctx",
        "user",
        "nick",
        "roles",
        "joined_at",
        "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: user.GuildMemberPayload):
        self._api = api

        self.user = data.get("user")
        self.nick = data.get("nick")
        self.roles = data.get("roles")
        self.joined_at = data.get("joined_at")
        self.event_id = ctx.get("id")
