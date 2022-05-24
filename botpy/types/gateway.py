from typing import TypedDict, List

from .user import Member


class UserPayload(TypedDict):
    id: str
    username: str
    bot: bool
    status: int


class WsUrlPayload(TypedDict):
    url: str


class MessagePayload(TypedDict):
    author: UserPayload
    channel_id: str
    content: str
    guild_id: str
    id: str
    member: Member
    mentions: List[UserPayload]
    seq: int
    seq_in_channel: str
    timestamp: str


class ReadyEvent(TypedDict):
    version: int
    session_id: str
    user: UserPayload
    shard: List[int]
