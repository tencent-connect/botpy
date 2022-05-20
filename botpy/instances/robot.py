from botpy.types import robot


class Robot:
    def __init__(self, data: robot.BaseInfo):
        self._update(data)

    def _update(self, data: robot.BaseInfo) -> None:
        self.name = data.get("username")
        self.id = int(data["id"])
        self.avatar = data.get("avatar")
