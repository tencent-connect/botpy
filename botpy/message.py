from .api import BotAPI
from .types import gateway


class Message:
    __slots__ = ("_api", "content", "channel_id", "message_id")

    def __init__(self, api: BotAPI, data: gateway.MessagePayload):
        self._api = api
        # TODO 创建一些实体类的数据缓存
        self.channel_id = data["channel_id"]
        self.message_id = data["id"]
        self.content = data["content"]

    async def reply(self, content: str):
        await self._api.post_message(content=content, channel_id=self.channel_id, msg_id=self.message_id)
