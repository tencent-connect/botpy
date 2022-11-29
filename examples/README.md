# examples

该目录用于存放基于 botpy 开发的机器人的完整示例。

```
examples/
.
├── README.md
├── config.example.yaml          # 示例配置文件（需要修改为config.yaml）
├── demo_announce.py             # 机器人公告API使用示例
├── demo_api_permission.py       # 机器人授权查询API使用示例
├── demo_at_reply.py             # 机器人at被动回复async示例
├── demo_at_reply_ark.py         # 机器人at被动回复ark消息示例
├── demo_at_reply_embed.py       # 机器人at被动回复embed消息示例
├── demo_at_reply_command.py     # 机器人at被动使用Command指令装饰器回复消息示例
├── demo_at_reply_file_data.py   # 机器人at被动回复本地图片消息示例
├── demo_at_reply_keyboard.py    # 机器人at被动回复md带内嵌键盘的示例
├── demo_at_reply_markdown.py    # 机器人at被动回复md消息示例
├── demo_at_reply_reference.py   # 机器人at被动回复消息引用示例
├── demo_dms_reply.py            # 机器人私信被动回复示例
├── demo_get_reaction_users.py   # 机器人获取表情表态成员列表示例
├── demo_guild_member_event.py   # 机器人频道成员变化事件示例
├── demo_interaction.py          # 机器人互动事件示例（未启用）
├── demo_pins_message.py         # 机器人消息置顶示例
├── demo_recall.py               # 机器人消息撤回示例
├── demo_schedule.py             # 机器人日程相关示例
├── demo_recall.py               # 机器人消息撤回示例
├── demo_audio_or_live_channel_member.py   # 音视频/直播子频道成员进出事件
├── demo_open_forum_event.py   # 开放论坛事件对象
```

## 环境安装

``` bash
pip install qq-botpy
```

## 使用方法

1. 拷贝 config.example.yaml 为 config.yaml ：

    ``` bash
    cp config.example.yaml config.yaml
    ```

2. 修改 config.yaml ，填入自己的 BotAppID 和  Bot token 。
3. 运行机器人。例如：

    ``` bash
    python3 demo_at_reply.py
    ```
