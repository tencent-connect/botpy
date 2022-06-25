from .api import BotAPI
from .types import user, gateway


class Member:
    __slots__ = ("_api", "_ctx", "user", "nick", "roles", "joined_at", "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: user.GuildMemberPayload):
        self._api = api

        self.user = self._User(data.get("user"))
        self.nick = data.get("nick")
        self.roles = data.get("roles")
        self.joined_at = data.get("joined_at")
        self.event_id = ctx.get("id")

    class _User:
        def __init__(self, data):
            self.id = data.get("id")
            self.username = data.get("username")
            self.avatar = data.get("avatar")
            self.bot = data.get("bot")
            self.union_openid = data.get("union_openid", None)
            self.union_user_account = data.get("union_user_account", None)
