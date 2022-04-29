#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageMarkdown, MessageMarkdownParams
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(context: WsContext, message: qqbot.Message):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    await handle_send_markdown_by_template(message.channel_id, message.id)

    await handle_send_markdown_by_content(message.channel_id, message.id)


async def handle_send_markdown_by_template(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown()
    markdown.template_id = 65
    markdown.params = [
        MessageMarkdownParams(key="title", values=["标题"]),
        MessageMarkdownParams(key="content", values=["为了成为一名合格的巫师，请务必阅读频道公告", "藏馆黑色魔法书"]),
    ]

    send = qqbot.MessageSendRequest(content="", markdown=markdown, msg_id=msg_id)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


async def handle_send_markdown_by_content(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown()
    markdown.content = "# 标题 \n## 简介很开心 \n内容"

    send = qqbot.MessageSendRequest(content="", markdown=markdown, msg_id=msg_id)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
