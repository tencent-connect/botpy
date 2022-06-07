from typing import TypedDict, List

from .user import Member


class WsContext(TypedDict):
    id: str  # 被动事件里携带的上下文信息，目前仅有部分事件支持


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


class MessageAuditPayload(TypedDict):
    audit_id: str
    message_id: str
    guild_id: str
    channel_id: str
    audit_time: str
    create_time: str
    seq_in_channel: str
