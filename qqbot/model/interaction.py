class Interaction:
    def __init__(self, data=None):
        self.id: str = ""
        self.application_id: int = 0
        self.type: int = 0
        self.data: InteractionData = None
        self.guild_id: int = 0
        self.channel_id: int = 0
        self.version: int = 1
        if data:
            self.__dict__ = data


class InteractionData:
    def __init__(
            self,
            type: int = 0,
            resolved: object = None,
            data=None
    ):
        self.type = type
        self.resolved = resolved
        if data:
            self.__dict__ = data


class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2
    HTTP_PROXY = 10
    INLINE_KEYBOARD = 11


class InteractionDataType:
    CHAT_INPUT_SEARCH = 9
    HTTP_PROXY = 10
    INLINE_KEYBOARD_BUTTON_CLICK = 11
