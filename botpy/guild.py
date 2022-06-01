from .api import BotAPI
from .types import guild, gateway


class Guild:
    __slots__ = ("_api", "_ctx", "guild_id", "id", "name")
    
    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: guild.GuildPayload):
        self._api = api
        self._ctx = ctx
        self.id = data["id"]
        self.name = data["name"]
        
    async def reply(self, content: str, **kwargs):
        await self._api.post_message(content=content, guild_id=self.id, msg_id=self._ctx["id"], **kwargs)
