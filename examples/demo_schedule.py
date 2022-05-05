#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import time

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

CHANNEL_SCHEDULE_ID = "12333"  # 修改为自己频道的日程子频道ID


async def _schedule_handler(context: WsContext, message: qqbot.Message):
    schedule_id: str = ""  # 日程ID，可以填写或者发送/创建日程 命令后获取

    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    schedule_api = qqbot.AsyncScheduleAPI(t_token, False)

    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)

    # 先发送消息告知用户
    message_to_send = qqbot.MessageSendRequest("command received: %s" % message.content)
    await msg_api.post_message(message.channel_id, message_to_send)

    delay = 1000 * 60
    start_time = int(round(time.time() * 1000)) + delay
    end_time = start_time + delay

    # 判断用户@后输出的指令
    if "/创建日程" in message.content:
        schedule = await schedule_api.create_schedule(
            CHANNEL_SCHEDULE_ID,
            qqbot.ScheduleToCreate(
                name="test",
                start_timestamp=str(start_time),
                end_timestamp=str(end_time),
                remind_type="0",
            ),
        )
        schedule_id = schedule.id

    elif "/查询日程" in message.content:
        schedule = await schedule_api.get_schedule(CHANNEL_SCHEDULE_ID, schedule_id)
        qqbot.logger.info(schedule)

    elif "/更新日程" in message.content:
        await schedule_api.update_schedule(
            CHANNEL_SCHEDULE_ID,
            schedule_id,
            qqbot.ScheduleToPatch(
                name="update",
                start_timestamp=str(start_time),
                end_timestamp=str(end_time),
                remind_type="0",
            ),
        )
    elif "/删除日程" in message.content:
        await schedule_api.delete_schedule(CHANNEL_SCHEDULE_ID, schedule_id)


if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _schedule_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
