from typing import TypedDict, Literal

from botpy.types.emoji import Emoji


# 0: 消息 1: 帖子 2: 评论 3: 回复
ReactionTargetType = Literal[0, 1, 2, 3]


class ReactionTarget(TypedDict):
    id: str
    type: ReactionTargetType


class Reaction(TypedDict):
    user_id: str
    guild_id: str
    channel_id: str
    target: ReactionTarget
    emoji: Emoji
