#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _recall_handler(context: WsContext, message: qqbot.Message):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    send = qqbot.MessageSendRequest("async recall")
    # 通过api发送回复消息
    await msg_api.post_message(message.channel_id, send)
    await msg_api.recall_message(message.channel_id, message.id)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _recall_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
