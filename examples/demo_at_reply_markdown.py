#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageMarkdown, MessageMarkdownParams

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    await handle_send_markdown_by_template(message.channel_id, message.id)

    await handle_send_markdown_by_content(message.channel_id, message.id)


async def handle_send_markdown_by_template(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown()
    markdown.template_id = 57
    markdown.params = [
        MessageMarkdownParams(key="title", values=["内嵌键盘"]),
        MessageMarkdownParams(key="slice", values=["请前往<#1146349>认领你的巫1111师身份", "为了成为一名合格的巫师，请务必阅读频道公告<#1146349>", "藏馆黑色魔法书"]),
        MessageMarkdownParams(key="image", values=["https://img1.baidu.com/it/u=4065681780,1569034563&fm=253&fmt=auto&app=120&f=JPEG?w=1422&h=800"]),
        MessageMarkdownParams(key="link", values=["https://www.qq.com"]),
        MessageMarkdownParams(key="desc", values=["这是个什么东东"])
    ]

    send = qqbot.MessageSendRequest(content="", markdown=markdown, msg_id=msg_id)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


async def handle_send_markdown_by_content(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown()
    markdown.content = "# 标题 \n## 简介很开心 \n内容[🔗腾讯](https://www.qq.com)"

    send = qqbot.MessageSendRequest(content="", markdown=markdown, msg_id=msg_id)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)
