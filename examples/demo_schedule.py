# -*- coding: utf-8 -*-
import os
import time

import botpy
from botpy import logging

from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

CHANNEL_SCHEDULE_ID = "12333"  # 修改为自己频道的日程子频道ID


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        schedule_id: str = ""  # 日程ID，可以填写或者发送/创建日程 命令后获取
        _log.info("receive message %s" % message.content)
        # 先发送消息告知用户
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")

        delay = 1000 * 60
        start_time = int(round(time.time() * 1000)) + delay
        end_time = start_time + delay

        # 判断用户@后输出的指令
        if "/创建日程" in message.content:
            schedule = await self.api.create_schedule(
                CHANNEL_SCHEDULE_ID,
                name="test",
                start_timestamp=str(start_time),
                end_timestamp=str(end_time),
                jump_channel_id=CHANNEL_SCHEDULE_ID,
                remind_type="0",
            )
            schedule_id = schedule.id

        elif "/查询日程" in message.content:
            schedule = await self.api.get_schedule(CHANNEL_SCHEDULE_ID, schedule_id)
            _log.info(schedule)

        elif "/更新日程" in message.content:
            await self.api.update_schedule(
                CHANNEL_SCHEDULE_ID,
                schedule_id,
                name="update",
                start_timestamp=str(start_time),
                end_timestamp=str(end_time),
                jump_channel_id=CHANNEL_SCHEDULE_ID,
                remind_type="0",
            )
        elif "/删除日程" in message.content:
            await self.api.delete_schedule(CHANNEL_SCHEDULE_ID, schedule_id)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
