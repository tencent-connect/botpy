class WsContext:
    """
    被动事件里携带的上下文信息，目前仅有部分事件支持
    """

    def __init__(self, event_type: str, event_id: str):
        self.event_type = str(event_type or "")
        self.event_id = str(event_id or "")
