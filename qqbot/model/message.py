# -*- coding: utf-8 -*-
from typing import List

from qqbot.model.member import User, Member


class Message:
    def __init__(self, data=None):
        self.id: str = ""
        self.channel_id: str = ""
        self.guild_id: str = ""
        self.content: str = ""
        self.timestamp: str = ""
        self.edited_timestamp: str = ""
        self.author: User = User()
        self.attachments: List[MessageAttachment] = [MessageAttachment()]
        self.embeds: List[MessageEmbed] = [MessageEmbed()]
        self.mentions: List[User] = [User()]
        self.member: Member = Member()
        self.ark: MessageArk = MessageArk()
        if data:
            self.__dict__ = data


class TypesEnum:
    around = "around"
    before = "before"
    after = "after"
    latest = ""


class MessagesPager:
    def __init__(self, type: TypesEnum, id: str, limit: str):
        self.type = type
        self.id = id
        self.limit = limit


class MessageAttachment:
    def __init__(self, data=None):
        self.url: str = ""
        if data:
            self.__dict__ = data


class MessageEmbed:
    def __init__(self, data=None):
        # 标题
        self.title: str = ""
        # 消息弹窗内容
        self.prompt: str = ""
        # 缩略图
        self.thumbnail: MessageEmbedThumbnail = MessageEmbedThumbnail()
        # 消息创建时间
        self.fields: List[MessageEmbedField] = [MessageEmbedField()]
        if data:
            self.__dict__ = data


class MessageEmbedThumbnail:
    def __init__(self, data=None):
        # 图片地址
        self.url: str = ""
        if data is not None:
            self.__dict__ = data


class MessageEmbedField:
    def __init__(self, data=None):
        self.key: str = ""
        self.value: str = ""
        if data:
            self.__dict__ = data


class MessageArk:
    def __init__(self, data=None):
        self.template_id = 0
        self.kv: List[MessageArkKv] = [MessageArkKv()]
        if data:
            self.__dict__ = data


class MessageArkKv:
    def __init__(self, data=None):
        self.key: str = ""
        self.value: str = ""
        self.obj: List[MessageArkObj] = [MessageArkObj()]
        if data:
            self.__dict__ = data


class MessageArkObj:
    def __init__(self, data=None):
        self.obj_kv: List[MessageArkObjKv] = [MessageArkObjKv()]
        if data:
            self.__dict__ = data


class MessageArkObjKv:
    def __init__(self, data=None):
        self.key: str = ""
        self.value: str = ""
        if data:
            self.__dict__ = data


class MessageSendRequest:
    def __init__(
        self,
        content: str,
        msg_id: str = None,
        embed: MessageEmbed = None,
        ark: MessageArk = None,
        image: str = "",
    ):
        """

        :param content:消息内容，文本内容，支持内嵌格式
        :param msg_id:要回复的消息id(Message.id), 在 AT_CREATE_MESSAGE 事件中获取。带了 msg_id 视为被动回复消息，否则视为主动推送消息
        :param embed:embed 消息，一种特殊的 ark
        :param ark:ark 消息
        :param image:图片url地址
        """

        self.content = content
        self.embed = embed
        self.ark = ark
        self.image = image
        self.msg_id = msg_id


class DirectMessageGuild:
    def __init__(self, data=None):
        self.guild_id: str = ""
        self.channel_id: str = ""
        self.creat_time: str = ""
        if data is not None:
            self.__dict__ = data


class CreateDirectMessageRequest:
    def __init__(self, source_guild_id: str, user_id: str):
        """
        :param source_guild_id: 创建的私信频道ID
        :param user_id: 私信接收人用户ID
        """
        self.recipient_id = user_id
        self.source_guild_id = source_guild_id
