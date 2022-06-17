from .api import BotAPI
from .types import gateway, reaction


class Reaction:
    __slots__ = (
        "_api",
        "_ctx",
        "user_id",
        "channel_id",
        "guild_id",
        "emoji",
        "target",
        "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: reaction.Reaction):
        self._api = api

        self.user_id = data.get("user_id")
        self.channel_id = data.get("channel_id")
        self.guild_id = data.get("guild_id")
        self.emoji = self._Emoji(data.get("emoji"))
        self.target = self._Target(data.get("target"))
        self.event_id = ctx.get("id")

    class _Emoji:
        def __init__(self, data):
            self.id = data.get("id")
            self.type = data.get("type")

    class _Target:
        def __init__(self, data):
            self.id = data.get("id")
            self.type = data.get("type")   # 0: 消息 1: 帖子 2: 评论 3: 回复
