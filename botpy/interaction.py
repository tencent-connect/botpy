from .api import BotAPI
from .types import interaction, gateway


class Interaction:
    __slots__ = ("_api", "_ctx", "id", "application_id", "type")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: interaction.InteractionPayload):
        self._api = api
        self._ctx = ctx
        self.id = data["id"]
        self.type = data["type"]
        self.application_id = data["application_id"]
