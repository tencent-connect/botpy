import os

import botpy
from botpy.core.util.yaml_util import YamlUtil

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_robot_at(self, message):
        print(f"message: {message}")
        print(f"------user: {self.user}")

    async def on_message_delete(self, message):
        print(f"message: {message}")
        print(f"------user: {self.user}")


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
