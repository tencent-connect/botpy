#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy.core.util.yaml_util import YamlUtil
from botpy.types.emoji import EmojiType
from botpy.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _reaction_handler(context: WsContext, message: botpy.Message):
    reaction_api = botpy.BotReactionAPI(t_token, False)
    botpy._log.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    await reaction_api.put_reaction(message.channel_id, message.id, EmojiType.system, "4")


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = botpy.Handler(botpy.HandlerType.AT_MESSAGE_EVENT_HANDLER, _reaction_handler)
    botpy.async_listen_events(t_token, False, qqbot_handler)
