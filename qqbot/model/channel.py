# -*- coding: utf-8 -*-


class ChannelType:
    TEXT_CHANNEL = 0  # 文字子频道
    # x_CHANNEL = 1    # 保留，不可用
    VOICE_CHANNEL = 2  # 语音子频道
    # x_CHANNEL = 3    # 保留，不可用
    GROUP_CHANNEL = 4  # 子频道分组
    LIVE_CHANNEL = 10005  # 直播子频道
    APP_CHANNEL = 10006  # 应用子频道
    DISCUSSION_CHANNEL = 10007  # 论坛子频道


class ChannelSubType:
    TALK = 0  # 闲聊
    POST = 1  # 公告
    CHEAT = 2  # 攻略
    BLACK = 3  # 开黑


class Channel:
    def __init__(self, data=None):
        self.id: str = ""
        self.guild_id: str = ""
        self.name: str = ""
        self.type: int = 0
        self.sub_type: int = 0
        self.position: int = 0
        self.parent_id: str = ""
        self.owner_id: str = ""
        if data is not None:
            self.__dict__ = data


class CreateChannelRequest:
    def __init__(
        self,
        name: str,
        channel_type: ChannelType,
        sub_type: ChannelSubType,
        position: int = 0,
        parent_id: str = "",
    ):
        self.parent_id = parent_id
        self.position = position
        self.sub_type = sub_type
        self.name = name
        self.type = channel_type


class PatchChannelRequest:
    def __init__(
        self, name: str, channel_type: ChannelType, position: int, parent_id: str
    ):
        self.parent_id = parent_id
        self.channel_type = channel_type
        self.position = position
        self.name = name


class ChannelResponse:
    def __init__(self, data=None):
        self.id: str = ""
        self.guild_id: str = ""
        self.name: str = ""
        self.type: int = 0
        self.sub_type: int = 0
        self.position: int = 0
        self.parent_id: str = ""
        self.owner_id: str = ""
        if data is not None:
            self.__dict__ = data
