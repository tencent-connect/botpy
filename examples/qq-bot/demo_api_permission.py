#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy.utils import YamlUtil
from botpy.types.permission import (
    APIPermissionDemandIdentify,
    PermissionDemandToCreate,
)
from botpy.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _api_permission_handler(context: WsContext, message: botpy.Message):
    msg_api = botpy.BotMessageAPI(t_token, False)
    api_permission_api = botpy.BotAPIPermissionAPI(t_token, False)

    botpy._log.info("event_type %s" % context.event_type + ",receive message %s" % message.content)

    # 先发送消息告知用户
    message_to_send = botpy.MessageSendRequest("command received: %s" % message.content)
    await msg_api.post_message(message.channel_id, message_to_send)

    # 输入/xxx后的处理
    if "/权限列表" in message.content:
        apis = await api_permission_api.get_permissions(message.guild_id)
        for api in apis:
            botpy._log.info("api: %s" % api.desc + ", status: %d" % api.auth_status)

    if "/请求权限" in message.content:
        demand_identity = APIPermissionDemandIdentify("/guilds/{guild_id}/members/{user_id}", "GET")
        permission_demand_to_create = PermissionDemandToCreate(message.channel_id, demand_identity)
        demand = await api_permission_api.post_permission_demand(message.guild_id, permission_demand_to_create)
        botpy._log.info("api title: %s" % demand.title + ", desc: %s" % demand.desc)


if __name__ == "__main__":
    t_token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = botpy.Handler(botpy.HandlerType.AT_MESSAGE_EVENT_HANDLER, _api_permission_handler)
    botpy.async_listen_events(t_token, False, qqbot_handler)
