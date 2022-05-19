from botpy.types.gateway import UserPayload


class Robot:
    def __init__(self, data: UserPayload):
        self._update(data)

    def _update(self, data: UserPayload) -> None:
        self.name = data.get("username")
        self.id = int(data["id"])
        self.bot = data.get("bot", False)
        self.status = data.get("status")
