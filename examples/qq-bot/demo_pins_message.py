#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy.core.util.yaml_util import YamlUtil
from botpy.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _pins_handler(context: WsContext, message: botpy.Message):
    pins_api = botpy.BotPinsAPI(t_token, False)
    botpy._log.info("event_type %s" % context.event_type + ",receive message %s" % message.content)

    if "/获取精华列表" in message.content:
        pins_message = await pins_api.get_pins(message.channel_id)
        botpy._log.info(pins_message)

    if "/创建精华消息" in message.content:
        pins_message = await pins_api.put_pin(message.channel_id, message.id)
        botpy._log.info(pins_message)

    if "/删除精华消息" in message.content:
        result = await pins_api.delete_pin(message.channel_id, message.id)
        botpy._log.info(result)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = botpy.Handler(botpy.HandlerType.AT_MESSAGE_EVENT_HANDLER, _pins_handler)
    botpy.async_listen_events(t_token, False, qqbot_handler)
