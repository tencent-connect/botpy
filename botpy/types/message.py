# -*- coding: utf-8 -*-
from typing import List, TypedDict

from .gateway import MessagePayload


class Attachment(TypedDict):
    url: str


class Thumbnail(TypedDict):
    url: str  # 图片地址


class EmbedField(TypedDict):
    name: str
    value: str


class Embed(TypedDict):
    title: str  # 标题
    prompt: str  # 消息弹窗内容
    thumbnail: Thumbnail  # 缩略图
    fields: List[EmbedField]  # 消息创建时间


class ArkObjKv(TypedDict):
    key: str
    value: str


class ArkObj(TypedDict):
    obj_kv: List[ArkObjKv]


class ArkKv(TypedDict):
    key: str
    value: str
    obj: List[ArkObj]


class Ark(TypedDict):
    template_id: int
    kv: List[ArkKv]


class Reference(TypedDict):
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


class MessageMarkdownParams(TypedDict):
    key: str
    values: List[str]


class Markdown(TypedDict):
    template_id: int
    params: MessageMarkdownParams
    content: str


class DirectMessageGuild(TypedDict):
    guild_id: str
    channel_id: str
    creat_time: str


class CreateDirectMessageRequest(TypedDict):
    """机器人发送私信时所传的数据对象

    :param source_guild_id: 创建的私信频道ID
    :param user_id: 私信接收人用户ID
    """

    recipient_id: str
    source_guild_id: str


class DeletedMessageOriginalAuthor(TypedDict):
    id: str
    username: str
    bot: bool


class DeletedMessage(TypedDict):
    guild_id: str
    channel_id: str
    id: str
    author: DeletedMessageOriginalAuthor


class DeletionOperator(TypedDict):
    id: str


class DeletedMessageInfo(TypedDict):
    message: DeletedMessage
    op_user: DeletionOperator
