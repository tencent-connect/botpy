# -*- coding: utf-8 -*-
from .audio import AudioControl, STATUS
from .message import (
    Message,
    TypesEnum,
    MessagesPager,
    MessageAttachment,
    MessageEmbedThumbnail,
    MessageEmbedField,
    MessageEmbed,
    MessageArkObjKv,
    MessageArkObj,
    MessageArkKv,
    MessageArk,
    MessageMarkdownParams,
    MessageMarkdown,
    MessageReference,
    MessageSendRequest,
    DirectMessageGuild,
    CreateDirectMessageRequest,
    DeletedMessageOriginalAuthor,
    DeletedMessage,
    DeletionOperator,
    MessageSendRequest,
    DeletedMessageInfo,
)
from .mute import MuteOption, MultiMuteOption
from .schedule import ScheduleToCreate, ScheduleToPatch
from .user import ReqOption
from .reaction import *
from .interaction import *

"""
这里放用户层直接使用的数据抽象类
提供一些抽象类的方法提高机器人开发使用效率
"""
