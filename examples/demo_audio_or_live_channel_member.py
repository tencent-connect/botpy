# -*- coding: utf-8 -*-
import botpy
from botpy import logging
from botpy.audio import PublicAudio

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_audio_or_live_channel_member_enter(self, Public_Audio: PublicAudio):
        if Public_Audio.channel_type == 2:
            _log.info("%s 加入了音视频子频道" % Public_Audio.user_id)
        elif Public_Audio.channel_type == 5:
            _log.info("%s 加入了直播子频道" % Public_Audio.user_id)

    async def on_audio_or_live_channel_member_exit(self, Public_Audio: PublicAudio):
        if Public_Audio.channel_type == 2:
            _log.info("%s 退出了音视频子频道" % Public_Audio.user_id)
        elif Public_Audio.channel_type == 5:
            _log.info("%s 退出了直播子频道" % Public_Audio.user_id)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(audio_or_live_channel_member=True)
    client = MyClient(intents=intents)
    client.run(appid="appid", token="token")
