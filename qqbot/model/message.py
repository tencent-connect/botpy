# -*- coding: utf-8 -*-
from typing import List

from qqbot.model.inline_keyboard import InlineKeyboard
from qqbot.model.member import User, Member


class MessageGet:
    def __init__(self, data=None):
        self.message: Message = Message()
        if data:
            self.__dict__ = data


class Message:
    def __init__(self, data=None):
        self.id: str = ""
        self.channel_id: str = ""
        self.guild_id: str = ""
        self.content: str = ""
        self.timestamp: str = ""
        self.edited_timestamp: str = ""
        self.mention_everyone: str = ""
        self.author: User = User()
        self.attachments: List[MessageAttachment] = [MessageAttachment()]
        self.embeds: List[MessageEmbed] = [MessageEmbed()]
        self.mentions: List[User] = [User()]
        self.member: Member = Member()
        self.ark: MessageArk = MessageArk()
        self.seq: int = 0
        self.seq_in_channel = ""
        self.message_reference = MessageReference()
        self.src_guild_id = ""
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
    def __init__(self, url: str = "", data=None):
        self.url = url
        if data:
            self.__dict__ = data


class MessageEmbedThumbnail:
    def __init__(self, url: str = "", data=None):
        # 图片地址
        self.url = url
        if data is not None:
            self.__dict__ = data


class MessageEmbedField:
    def __init__(self, data=None, name: str = None, value: str = None):
        self.name = name
        self.value = value
        if data:
            self.__dict__ = data


class MessageEmbed:
    def __init__(
        self,
        title: str = "",
        prompt: str = "",
        thumbnail: MessageEmbedThumbnail = MessageEmbedThumbnail(),
        fields: List[MessageEmbedField] = [MessageEmbedField()],
        data=None,
    ):
        # 标题
        self.title = title
        # 消息弹窗内容
        self.prompt = prompt
        # 缩略图
        self.thumbnail = thumbnail
        # 消息创建时间
        self.fields = fields
        if data:
            self.__dict__ = data


class MessageArkObjKv:
    def __init__(self, data=None, key: str = None, value: str = None):
        self.key = key
        self.value = value
        if data:
            self.__dict__ = data


class MessageArkObj:
    def __init__(self, data=None, obj_kv: List[MessageArkObjKv] = None):
        self.obj_kv = obj_kv
        if data:
            self.__dict__ = data


class MessageArkKv:
    def __init__(
        self,
        data=None,
        key: str = None,
        value: str = None,
        obj: List[MessageArkObj] = None,
    ):
        self.key = key
        self.value = value
        self.obj = obj
        if data:
            self.__dict__ = data


class MessageArk:
    def __init__(
        self,
        template_id: int = 0,
        kv: List[MessageArkKv] = [MessageArkKv()],
        data=None,
    ):
        self.template_id = template_id
        self.kv = kv
        if data:
            self.__dict__ = data


class MessageMarkdownParams:
    def __init__(self, data=None, key="", values: List[str] = None):
        self.key = key
        self.values = values
        if data:
            self.__dict__ = data


class MessageMarkdown:
    def __init__(self, data=None, template_id: int = 0, params=None, content: str = ""):
        self.template_id = template_id
        self.params = params
        self.content = content
        if data:
            self.__dict__ = data


class MessageReference:
    def __init__(self, data=None, message_id: str = "", ignore_get_message_error: bool = False):
        self.message_id = message_id
        self.ignore_get_message_error = ignore_get_message_error
        if data:
            self.__dict__ = data


class MessageKeyboard:
    """
    id 和 content 两个参数互斥，都传值将返回错误
    """
    def __init__(self, id: str = None, content: InlineKeyboard = None):
        if id:
            self.id = id
        if content:
            self.content = content


class MessageSendRequest:
    def __init__(
        self,
        content: str = "",
        msg_id: str = None,
        embed: MessageEmbed = None,
        ark: MessageArk = None,
        image: str = "",
        message_reference: MessageReference = None,
        markdown: MessageMarkdown = None,
        keyboard: MessageKeyboard = None
    ):
        """
        机器人发送消息时所传的数据对象

        :param content: 消息内容，文本内容，支持内嵌格式
        :param msg_id: 要回复的消息id(Message.id), 在 AT_CREATE_MESSAGE 事件中获取。带了 msg_id 视为被动回复消息，否则视为主动推送消息
        :param embed: embed 消息，一种特殊的 ark
        :param ark: ark 消息
        :param image: 图片url地址
        :param message_reference: 引用消息
        :param markdown: markdown 消息
        :param keyboard: markdown 消息内的按钮
        """

        self.content = content
        self.embed = embed
        self.ark = ark
        self.image = image
        self.msg_id = msg_id
        self.message_reference = message_reference
        self.markdown = markdown
        self.keyboard = keyboard


class DirectMessageGuild:
    def __init__(self, data=None, guild_id: str = "", channel_id: str = "", creat_time: str = ""):
        self.guild_id =  guild_id
        self.channel_id =  channel_id
        self.creat_time =  creat_time
        if data is not None:
            self.__dict__ = data


class CreateDirectMessageRequest:
    def __init__(self, source_guild_id: str, user_id: str):
        """
        机器人发送私信时所传的数据对象

        :param source_guild_id: 创建的私信频道ID
        :param user_id: 私信接收人用户ID
        """
        self.recipient_id = user_id
        self.source_guild_id = source_guild_id


class DeletedMessageOriginalAuthor:
    def __init__(self, data=None):
        self.id = ""
        self.username = ""
        self.bot = False
        if data:
            self.__dict__ = data


class DeletedMessage:
    def __init__(self, data=None):
        self.guild_id = ""
        self.src_guild_id = ""
        self.channel_id = ""
        self.id = ""
        self.author = DeletedMessageOriginalAuthor()
        if data:
            self.__dict__ = data


class DeletionOperator:
    def __init__(self, data=None):
        self.id = ""
        if data:
            self.__dict__ = data


class DeletedMessageInfo:
    def __init__(self, data=None):
        self.message = DeletedMessage()
        self.op_user = DeletionOperator()
        if data:
            self.__dict__ = data
