# -*- coding: utf-8 -*-
from typing import List

from .gateway import MessagePayload


class Attachment:
    url: str


class Thumbnail:
    url: str  # 图片地址


class EmbedField:
    name: str
    value: str


class Embed:
    title: str  # 标题
    prompt: str  # 消息弹窗内容
    thumbnail: Thumbnail  # 缩略图
    fields: List[EmbedField]  # 消息创建时间


class ArkObjKv:
    key: str
    value: str


class ArkObj:
    obj_kv: List[ArkObjKv]


class ArkKv:
    key: str
    value: str
    obj: List[ArkObj]


class Ark:
    template_id: int
    kv: List[ArkKv]


class Reference:
    message_id: str
    ignore_get_message_error: bool


class Message(MessagePayload):
    edited_timestamp: str
    mention_everyone: str
    attachments: List[Attachment]
    embeds: List[Embed]
    ark: Ark
    message_reference: Reference


class TypesEnum:
    around = "around"
    before = "before"
    after = "after"
    latest = ""


class MessagesPager:
    def __init__(self, type: TypesEnum, id: str, limit: str):
        type = type
        id = id
        limit = limit


class MessageMarkdownParams:
    key: str
    values: List[str]


class Markdown:
    template_id: int
    params = None
    content: str


class DirectMessageGuild:
    guild_id: str
    channel_id: str
    creat_time: str


class CreateDirectMessageRequest:
    """机器人发送私信时所传的数据对象

    :param source_guild_id: 创建的私信频道ID
    :param user_id: 私信接收人用户ID
    """

    recipient_id: str
    source_guild_id: str


class DeletedMessageOriginalAuthor:
    id: str
    username: str
    bot: bool


class DeletedMessage:
    guild_id: str
    channel_id: str
    id: str
    author: DeletedMessageOriginalAuthor


class DeletionOperator:
    id: str


class DeletedMessageInfo:
    message: DeletedMessage
    op_user: DeletionOperator
