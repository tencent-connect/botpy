from enum import Enum
from typing import TypedDict


class InteractionData:
    type: int
    resolved: object


class InteractionPayload(TypedDict):
    id: str
    application_id: int
    type: int
    data: InteractionData
    guild_id: int
    channel_id: int
    version: int


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    HTTP_PROXY = 10
    INLINE_KEYBOARD = 11

    def __int__(self) -> int:
        return self.value


class InteractionDataType(Enum):
    CHAT_INPUT_SEARCH = 9
    HTTP_PROXY = 10
    INLINE_KEYBOARD_BUTTON_CLICK = 11

    def __int__(self) -> int:
        return self.value
