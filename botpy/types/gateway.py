from typing import TypedDict, List


class RobotInfo(TypedDict):
    id: str
    username: str
    bot: bool
    status: int


class ReadyEvent(TypedDict):
    version: int
    session_id: str
    user: RobotInfo
    shard: List[int]
