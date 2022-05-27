import os

import botpy
from botpy import logging
from botpy.channel import Channel
from botpy.message import Message
from botpy.utils import YamlUtil

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_channel_create(self, channel: Channel):
        _log.info(f"create channel name:{channel.name}")
        await channel.reply(f"机器人 {self.robot.name} 发现你创建频道了！")

    async def on_at_message_create(self, message: Message):
        _log.info(f"robot 「{self.robot.name}」 is on at, message: {message.content}")
        await message.reply(f"机器人收到你的@消息了: {message.content}")


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(guilds=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
