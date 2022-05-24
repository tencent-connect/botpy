#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy.utils import YamlUtil
from botpy.types.message import MessageReference
from botpy.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(context: WsContext, message: botpy.Message):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = botpy.BotMessageAPI(t_token, False)
    # 打印返回信息
    botpy._log.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    # 构造消息发送请求数据对象
    message_reference = MessageReference()
    message_reference.message_id = message.id
    send = botpy.MessageSendRequest(content="<emoji:4>这是一条引用消息", msg_id=message.id, message_reference=message_reference)
    # 通过api发送回复消息
    await msg_api.post_message(message.channel_id, send)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = botpy.Handler(botpy.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    botpy.async_listen_events(t_token, False, qqbot_handler)
