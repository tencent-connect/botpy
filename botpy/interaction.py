from .api import BotAPI
from .types import interaction,gateway


class Interaction:
    __slots__ = ("_api", "_ctx", "id", "application_id", "type")
    
    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: interaction.InteractionPayload):
        self._api = api
        self._ctx = ctx
        self.id = data["id"]
        self.type = data["type"]
    
    async def reply(self, content: str, **kwargs):
        await self._api.post_message(content=content, channel_id=self.id, msg_id=self._ctx["id"], **kwargs)
