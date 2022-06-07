from .api import BotAPI
from .types import channel, gateway


class Channel:
    __slots__ = (
        "_api",
        "_ctx",
        "guild_id",
        "id",
        "name",
        "type",
        "sub_type",
        "position",
        "owner_id",
        "private_type",
        "speak_permission",
        "application_id",
        "permissions",
    )

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: channel.ChannelPayload):
        self._api = api
        self._ctx = ctx

        self.id = data.get("id")
        self.name = data.get("name", "default_channel")
        self.type = data.get("type")
        self.sub_type = data.get("sub_type")
        self.position = data.get("position")
        self.owner_id = data.get("owner_id")
        self.private_type = data.get("private_type")
        self.speak_permission = data.get("speak_permission")
        self.application_id = data.get("application_id", "")
        self.permissions = data.get("permissions")

    async def reply(self, content: str, **kwargs):
        await self._api.post_message(content=content, channel_id=self.id, msg_id=self._ctx["id"], **kwargs)
