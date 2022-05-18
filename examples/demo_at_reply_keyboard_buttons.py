#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.inline_keyboard import RenderData, Action, Permission, Button, InlineKeyboardRow, InlineKeyboard
from qqbot.model.message import MessageMarkdown, MessageKeyboard
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(context: WsContext, message: qqbot.Message):
    """
    发送带消息按钮的 markdown 消息。(消息按钮只能和 markdown 一起使用)

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    await send_template_keyboard(message.channel_id, message.id)
    await send_self_defined_keyboard(message.channel_id, message.id)


async def send_template_keyboard(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown(content="# 123 \n 今天是个好天气")
    keyword: MessageKeyboard = MessageKeyboard(id='62')
    send = qqbot.MessageSendRequest(markdown=markdown, msg_id=msg_id, keyboard=keyword)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


async def send_self_defined_keyboard(channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    markdown = MessageMarkdown(content="# 标题 \n## 简介 \n内容")
    keyboard: MessageKeyboard = build_a_demo_keyboard()
    send = qqbot.MessageSendRequest(markdown=markdown, msg_id=msg_id, keyboard=keyboard)
    # 通过api发送回复消息
    await msg_api.post_message(channel_id, send)


def build_a_demo_keyboard() -> MessageKeyboard:
    """
    创建一个只有一行且该行只有一个 button 的键盘
    """
    button1 = Button(
        '1',
        RenderData(
            "button",
            "BUTTON",
            0
        ),
        Action(
            2,
            Permission(2, specify_role_ids=["1"]),
            10,
            "/搜索",
            True
        )
    )
    row1 = InlineKeyboardRow([button1])
    inline_keyboard = InlineKeyboard([row1])
    return MessageKeyboard(content=inline_keyboard)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
