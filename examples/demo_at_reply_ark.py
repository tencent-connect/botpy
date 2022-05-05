#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageArk, MessageArkKv
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _message_handler(context: WsContext, message: qqbot.Message):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    await handle_send_ark(1, message.channel_id, message.id)


async def handle_send_ark(time, channel_id, msg_id):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    for i in range(time):
        await asyncio.sleep(1)
        # 构造消息发送请求数据对象
        ark = MessageArk()
        ark.template_id = 37

        ark.kv = [
            MessageArkKv(key="#PROMPT#", value="通知提醒"),
            MessageArkKv(key="#METATITLE#", value="标题"),
            MessageArkKv(key="#METASUBTITLE#", value="子标题"),
            MessageArkKv(
                key="#METACOVER#",
                value="https://vfiles.gtimg.cn/vupload/20211029/bf0ed01635493790634.jpg",
            ),
        ]

        send = qqbot.MessageSendRequest(content="", ark=ark, msg_id=msg_id)
        # 通过api发送回复消息
        qqbot.logger.info("send text message : %s" % i)
        await msg_api.post_message(channel_id, send)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
