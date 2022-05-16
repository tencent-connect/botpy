# -*- coding: utf-8 -*-


class Type:
    typeBot = "Bot"
    typeNormal = "Bearer"


class Token:
    def __init__(self, app_id: str, access_token: str):
        """
        :param app_id: 机器人appid
        :param access_token: 机器人token
        """
        self.app_id = app_id
        self.access_token = access_token
        self.Type = Type.typeBot

    # BotToken 机器人身份的 token
    def bot_token(self):
        return self

    # GetString 获取授权头字符串
    def get_string(self):
        if self.Type == Type.typeNormal:
            return self.access_token
        return "{}.{}".format(self.app_id, self.access_token)

    def get_type(self):
        return self.Type
