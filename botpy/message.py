from .api import BotAPI
from .types import gateway


class Message:
    __slots__ = ("_api", "content", "channel_id", "message_id", "guild_id")

    def __init__(self, api: BotAPI, data: gateway.MessagePayload):
        self._api = api
        # TODO 创建一些实体类的数据缓存 @veehou
        self.channel_id = data["channel_id"]
        self.message_id = data["id"]
        self.content = data["content"]
        self.guild_id = data["guild_id"]

    async def reply(self, **kwargs):
        await self._api.post_message(channel_id=self.channel_id, msg_id=self.message_id, **kwargs)
