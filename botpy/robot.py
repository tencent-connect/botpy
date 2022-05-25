from botpy.types import robot


class Robot:
    def __init__(self, data: robot.Robot):
        self._update(data)

    def _update(self, data: robot.Robot) -> None:
        self.name = data.get("username")
        self.id = int(data["id"])
        self.avatar = data.get("avatar")


class Token:
    TYPE_BOT = "Bot"
    TYPE_NORMAL = "Bearer"

    def __init__(self, app_id: str, access_token: str):
        """
        :param app_id:
            机器人appid
        :param access_token:
            机器人token
        """
        self.app_id = app_id
        self.access_token = access_token
        self.Type = self.TYPE_BOT

    # BotToken 机器人身份的 token
    def bot_token(self):
        return self

    # GetString 获取授权头字符串
    def get_string(self):
        if self.Type == self.TYPE_NORMAL:
            return self.access_token
        return "{}.{}".format(self.app_id, self.access_token)

    def get_type(self):
        return self.Type
