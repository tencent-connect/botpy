#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot import GuildMember
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _member_event_handler(context: WsContext, guild_member: GuildMember):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param guild_member: 成员事件对象
    """
    qqbot.logger.info("event_type %s" % context.event_type + ", event_id %s" % context.event_id)

    msg_api = qqbot.AsyncMessageAPI(t_token, False)

    # 这里将 WsContext.event_id 作为回复消息的 msg_id，可以使回复消息被识别为被动消息。
    send = qqbot.MessageSendRequest(content="收到了成员事件", msg_id=context.event_id)
    await msg_api.post_message(channel_id="1234567", message_send=send)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.GUILD_MEMBER_EVENT_HANDLER, _member_event_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
