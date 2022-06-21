from .api import BotAPI
from .types import interaction, gateway


class Interaction:
    __slots__ = ("_api", "_ctx", "id", "application_id", "type", "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: interaction.InteractionPayload):
        self._api = api

        self.id = data.get("id")
        self.type = data.get("type")
        self.application_id = data.get("application_id")
        self.event_id = ctx.get("id")
