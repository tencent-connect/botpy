from .api import BotAPI
from .types import user


class Member:
    __slots__ = ("_api", "_ctx", "user", "nick", "roles", "joined_at", "event_id")

    def __init__(self, api: BotAPI, event_id, data: user.GuildMemberPayload):
        self._api = api

        self.user = self._User(data.get("user", {}))
        self.nick = data.get("nick", None)
        self.roles = data.get("roles", None)
        self.joined_at = data.get("joined_at", None)
        self.event_id = event_id

    class _User:
        def __init__(self, data):
            self.id = data.get("id", None)
            self.username = data.get("username", None)
            self.avatar = data.get("avatar", None)
            self.bot = data.get("bot", None)
            self.union_openid = data.get("union_openid", None)
            self.union_user_account = data.get("union_user_account", None)
