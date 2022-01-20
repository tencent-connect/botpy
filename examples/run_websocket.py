#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.MessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
    # 构造消息发送请求数据对象
    send = qqbot.MessageSendRequest("收到你的消息: %s" % message.content, message.id)
    # 通过api发送回复消息
    msg_api.post_message(message.channel_id, send)


def _direct_message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.MessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
    # 构造消息发送请求数据对象
    send = qqbot.MessageSendRequest("收到你的私信消息了：%s" % message.content, message.id)
    # 通过api发送回复消息
    msg_api.post_direct_message(message.guild_id, send)


if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.listen_events(t_token, False, qqbot_handler)

    # # 多事件监听
    # qqbot_dms_handler = qqbot.Handler(
    #     qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler
    # )
    # qqbot.listen_events(t_token, False, qqbot_handler, qqbot_dms_handler)
