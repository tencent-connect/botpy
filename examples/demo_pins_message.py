#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _pins_handler(context: WsContext, message: qqbot.Message):
    pins_api = qqbot.AsyncPinsAPI(t_token, False)
    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)

    if "/获取精华列表" in message.content:
        pins_message = await pins_api.get_pins(message.channel_id)
        qqbot.logger.info(pins_message)

    if "/创建精华消息" in message.content:
        pins_message = await pins_api.put_pin(message.channel_id, message.id)
        qqbot.logger.info(pins_message)

    if "/删除精华消息" in message.content:
        result = await pins_api.delete_pin(message.channel_id, message.id)
        qqbot.logger.info(result)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _pins_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
