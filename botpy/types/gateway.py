from typing import TypedDict, List


class UserPayload(TypedDict):
    id: str
    username: str
    bot: bool
    status: int


class ReadyEvent(TypedDict):
    version: int
    session_id: str
    user: UserPayload
    shard: List[int]


class WsUrlPayload(TypedDict):
    url: str
