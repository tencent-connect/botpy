from qqbot.model.emoji import Emoji


class Reaction:
    def __init__(self, data=None):
        self.user_id: str = ""
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.target: ReactionTarget = ReactionTarget()
        self.emoji: Emoji = Emoji()
        if data:
            self.__dict__ = data


class ReactionTarget:
    def __init__(self, data=None):
        self.id: str = ""
        self.type: int = 0
        if data:
            self.__dict__ = data


class ReactionTargetType:
    message = 0
    feed = 1
    comment = 2
    reply = 3
