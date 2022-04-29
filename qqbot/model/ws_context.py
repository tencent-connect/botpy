class WsContext:
    """
    被动事件里携带的上下文信息，目前支持的回调类型有：

    GUILD_MEMBER_ADD
    GUILD_MEMBER_UPDATE
    GUILD_MEMBER_REMOVE
    MESSAGE_REACTION_ADD
    MESSAGE_REACTION_REMOVE
    FORUM_THREAD_CREATE
    FORUM_THREAD_UPDATE
    FORUM_THREAD_DELETE
    FORUM_POST_CREATE
    FORUM_POST_DELETE
    FORUM_REPLY_CREATE
    FORUM_REPLY_DELETE
    """

    def __init__(self, event_type: str, event_id: str):
        self.event_type = str(event_type or "")
        self.event_id = str(event_id or "")
