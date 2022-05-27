#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import botpy
from botpy import InteractionData, InteractionDataType
from botpy.core.util.yaml_util import YamlUtil
from botpy.types.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _interaction_handler(context: WsContext, interaction: botpy.Interaction):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param interaction: 事件对象（如监听消息是Message对象）
    """
    # 发送回复消息通知
    msg_api = botpy.BotMessageAPI(t_token, False)
    send = botpy.MessageSendRequest(content="收到了 markdown 交互事件，data_type: %d" % interaction.data.type)
    await msg_api.post_message(interaction.channel_id, send)

    # 异步更新交互数据
    interaction_api = botpy.BotInteractionAPI(t_token, False)
    data = InteractionData(type=InteractionDataType.INLINE_KEYBOARD_BUTTON_CLICK, resolved="Test")
    await interaction_api.put_interaction(interaction.id, data)


if __name__ == "__main__":
    # async的异步接口的使用示例
    t_token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = botpy.Handler(botpy.HandlerType.INTERACTION_CREATE_HANDLER, _interaction_handler)
    botpy.async_listen_events(t_token, False, qqbot_handler)
