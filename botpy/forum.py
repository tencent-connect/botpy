from json import loads

from .api import BotAPI
from .types import gateway, forum


class _Text:
    def __init__(self, data):
        self.text = data.get("text", None)


class _Image:
    def __init__(self, data):
        self.plat_image = self._PlatImage(data.get("plat_image", {}))

    class _PlatImage:
        def __init__(self, data):
            self.url = data.get("url", None)
            self.width = data.get("width", None)
            self.height = data.get("height", None)
            self.image_id = data.get("image_id", None)


class _Video:
    def __init__(self, data):
        self.plat_video = self._PlatVideo(data.get("plat_video", {}))

    class _PlatVideo:
        def __init__(self, data):
            self.url = data.get("url", None)
            self.width = data.get("width", None)
            self.height = data.get("height", None)
            self.video_id = data.get("video_id", None)
            self.cover = data.get("cover", {})

        class _Cover:
            def __init__(self, data):
                self.url = data.get("url", None)
                self.width = data.get("width", None)
                self.height = data.get("height", None)


class _Url:
    def __init__(self, data):
        self.url = data.get("url", None)
        self.desc = data.get("desc", None)


class Thread:
    __slots__ = (
        "_api",
        "_ctx",
        "thread_info",
        "channel_id",
        "guild_id",
        "author_id",
        "event_id")

    def __init__(self, api: BotAPI, ctx: gateway.WsContext, data: forum.Thread):
        self._api = api

        self.author_id = data.get("author_id")
        self.channel_id = data.get("channel_id")
        self.guild_id = data.get("guild_id")
        self.thread_info = self._ThreadInfo(data.get("thread_info"))
        self.event_id = ctx.get("id")

    class _ThreadInfo:
        def __init__(self, data):
            self.title = self._Title(loads(data.get("title")))
            self.content = self._Content(loads(data.get("content")))
            self.thread_id = data.get("thread_id")
            self.date_time = data.get("date_time")

        class _Title:
            def __init__(self, data):
                self.paragraphs = [self._Paragraphs(items) for items in data.get("paragraphs")]

            class _Paragraphs:
                def __init__(self, data):
                    self.elems = [self._Elems(items) for items in data.get("elems")]
                    self.props = data.get("props")

                class _Elems:
                    def __init__(self, data):
                        self.type = data.get("type")
                        self.text = _Text(data.get("text", {}))

        class _Content:
            def __init__(self, data):
                self.paragraphs = [self._Paragraphs(items) for items in data.get("paragraphs")]

            class _Paragraphs:
                def __init__(self, data):
                    self.elems = [self._Elems(items) for items in data.get("elems")]
                    self.props = data.get("props")

                class _Elems:
                    def __init__(self, data):
                        self.type = data.get("type")
                        if self.type == 1:
                            self.text = _Text(data.get("text", {}))
                        elif self.type == 2:
                            self.image = _Image(data.get("image", {}))
                        elif self.type == 3:
                            self.video = _Video(data.get("video", {}))
                        elif self.type == 4:
                            self.url = _Url(data.get("url", {}))
