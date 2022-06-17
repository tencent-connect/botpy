from .api import BotAPI
from .types import gateway


class Message:
    __slots__ = (
        "_api",
        "author",
        "content",
        "channel_id",
        "id",
        "guild_id",
        "member",
        "message_reference",
        "mentions",
        "seq",
        "seq_in_channel",
        "timestamp",
        "event_id"
    )

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: gateway.MessagePayload):
        # TODO 创建一些实体类的数据缓存 @veehou
        self._api = api

        self.author = self._User(data.get("author"))
        self.channel_id = data.get("channel_id")
        self.id = data.get("id")
        self.content = data.get("content")
        self.guild_id = data.get("guild_id")
        self.member = self._Member(data.get("member"))
        self.message_reference = self._MessageRef(data.get("message_reference", {}))
        self.mentions = [self._User(items) for items in data.get("mentions", {})]
        self.seq = data.get("seq")  # 全局消息序号
        self.seq_in_channel = data.get("seq_in_channel")  # 子频道消息序号
        self.timestamp = data.get("timestamp")
        self.event_id = ctx.get("id")

    class _User:
        def __init__(self, data):
            self.id = data.get("id")
            self.username = data.get("username")
            self.bot = data.get("bot")
            self.avatar = data.get("avatar")

    class _Member:
        def __init__(self, data):
            self.nick = data.get("nick", None)
            self.roles = data.get("roles", None)
            self.joined_at = data.get("joined_at", None)

    class _MessageRef:
        def __init__(self, data):
            self.message_id = data.get("message_id", None)

    async def reply(self, **kwargs):
        return await self._api.post_message(channel_id=self.channel_id, msg_id=self.id, **kwargs)


class DirectMessage:
    __slots__ = (
        "_api",
        "author",
        "content",
        "direct_message",
        "channel_id",
        "id",
        "guild_id",
        "member",
        "message_reference",
        "seq",
        "seq_in_channel",
        "src_guild_id",
        "timestamp",
        "event_id"
    )

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: gateway.DirectMessagePayload):
        self._api = api

        self.author = self._User(data.get("author"))
        self.channel_id = data.get("channel_id")
        self.id = data.get("id")
        self.content = data.get("content")
        self.direct_message = data.get("direct_message")
        self.guild_id = data.get("guild_id")
        self.member = self._Member(data.get("member"))
        self.message_reference = self._MessageRef(data.get("message_reference", {}))
        self.seq = data.get("seq")  # 全局消息序号
        self.seq_in_channel = data.get("seq_in_channel")  # 子频道消息序号
        self.src_guild_id = data.get("src_guild_id")
        self.timestamp = data.get("timestamp")
        self.event_id = ctx.get("id")

    class _User:
        def __init__(self, data):
            self.id = data.get("id")
            self.username = data.get("username")
            self.avatar = data.get("avatar")

    class _Member:
        def __init__(self, data):
            self.joined_at = data.get("joined_at", None)

    class _MessageRef:
        def __init__(self, data):
            self.message_id = data.get("message_id", None)

    async def reply(self, **kwargs):
        return await self._api.post_message(channel_id=self.channel_id, msg_id=self.id, **kwargs)


class MessageAudit:
    __slots__ = (
        "_api",
        "audit_id",
        "message_id",
        "channel_id",
        "guild_id",
        "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: gateway.MessageAuditPayload):
        self._api = api
        self.audit_id = data.get("audit_id")
        self.channel_id = data.get("channel_id")
        self.message_id = data.get("message_id")
        self.guild_id = data.get("guild_id")
        self.event_id = ctx.get("id")
