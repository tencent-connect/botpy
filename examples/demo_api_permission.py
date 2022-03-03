#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.api_permission import (
    APIPermissionDemandIdentify,
    PermissionDemandToCreate,
)

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _api_permission_handler(event, message: qqbot.Message):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    api_permission_api = qqbot.AsyncAPIPermissionAPI(t_token, False)

    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)

    # 先发送消息告知用户
    message_to_send = qqbot.MessageSendRequest("command received: %s" % message.content)
    await msg_api.post_message(message.channel_id, message_to_send)

    # 输入/xxx后的处理
    if "/权限列表" in message.content:
        apis = await api_permission_api.get_permissions(message.guild_id)
        for api in apis:
            qqbot.logger.info("api: %s" % api.desc + ", status: %d" % api.auth_status)

    if "/请求权限" in message.content:
        demand_identity = APIPermissionDemandIdentify(
            "/guilds/{guild_id}/members/{user_id}", "GET"
        )
        permission_demand_to_create = PermissionDemandToCreate(
            message.channel_id, demand_identity
        )
        demand = await api_permission_api.post_permission_demand(
            message.guild_id, permission_demand_to_create
        )
        qqbot.logger.info("api title: %s" % demand.title + ", desc: %s" % demand.desc)


if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _api_permission_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)
