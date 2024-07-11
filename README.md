<div align="center">

![botpy](https://socialify.git.ci/tencent-connect/botpy/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&language=1&logo=https%3A%2F%2Fgithub.com%2Ftencent-connect%2Fbot-docs%2Fblob%2Fmain%2Fdocs%2F.vuepress%2Fpublic%2Ffavicon-64px.png%3Fraw%3Dtrue&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light)

[![Language](https://img.shields.io/badge/language-python-green.svg?style=plastic)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=plastic)](https://github.com/tencent-connect/botpy/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![PyPI](https://img.shields.io/pypi/v/qq-botpy)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-713959939bdc4adca0eea2d4420eef4b/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](https://devops.woa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-713959939bdc4adca0eea2d4420eef4b/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)

_✨ 基于 [机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的机器人框架 ✨_

_✨ 为开发者提供一个易使用、开发效率高的开发框架 ✨_

[文档](https://bot.q.qq.com/wiki/develop/pythonsdk/)
·
[下载](https://github.com/tencent-connect/botpy/tags)
·
[安装](https://bot.q.qq.com/wiki/develop/pythonsdk/#sdk-安装)

</div>

## 准备工作

### 安装

```bash
pip install qq-botpy
```

更新包的话需要添加 `--upgrade` `兼容版本：python3.8+`

### 使用

需要使用的地方`import botpy`

```python
import botpy
```

### 兼容提示

> 原机器人的老版本`qq-bot`仍然可以使用，但新接口的支持上会逐渐暂停，此次升级不会影响线上使用的机器人 

## 版本更新说明
### v1.1.5
1. 更新鉴权方式。 新版本通过AppID + AppSecret进行鉴权，需要使用者进行适配。AppSecret见[QQ机器人开发设置页](https://q.qq.com/qqbot/#/developer/developer-setting)中的AppSecret字段。具体适配方式见示例  [鉴权配置示例](./examples/config.example.yaml) [鉴权传参接口变更示例](./examples/demo_at_reply.py)
2. 增加群和好友内发消息能力。可参考[群内发消息示例](./examples/demo_group_reply_text.py) [好友内发消息示例](./examples/demo_c2c_reply_text.py)
3. 增加群和好友内发送富媒体消息能力，目前支持图片、视频、语音类型。可参考  [群内发富媒体消息示例](./examples/demo_group_reply_file.py)   [好友内发富媒体消息示例](./examples/demo_c2c_reply_file.py)

## 使用方式

### 快速入门

#### 步骤1

通过继承实现`bot.Client`, 实现自己的机器人Client 

#### 步骤2

实现机器人相关事件的处理方法,如 `on_at_message_create`， 详细的事件监听列表，请参考 [事件监听.md](./docs/事件监听.md)

如下，是定义机器人被@的后自动回复:

```python
import botpy
from botpy.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
```

``注意:每个事件会下发具体的数据对象，如`message`相关事件是`message.Message`的对象 (部分事件透传了后台数据，暂未实现对象缓存)``

#### 步骤3

设置机器人需要监听的事件通道，并启动`client`

```python
import botpy
from botpy.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")

intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)
client.run(appid="12345", secret="xxxx")
```

### 备注

也可以通过预设置的类型，设置需要监听的事件通道

```python
import botpy

intents = botpy.Intents.none()
intents.public_guild_messages=True
```

### 使用API

如果要使用`api`方法，可以参考如下方式:

```python
import botpy
from botpy.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")
```

## 示例机器人

[`examples`](./examples/) 目录下存放示例机器人，具体使用可参考[`Readme.md`](./examples/README.md) 

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

# 参与开发

## 环境配置

```bash
pip install -r requirements.txt   # 安装依赖的pip包

pre-commit install                 # 安装格式化代码的钩子
```

## 单元测试

代码库提供API接口测试和 websocket 的单测用例，位于 `tests` 目录中。如果需要自己运行，可以在 `tests` 目录重命名 `.test.yaml` 文件后添加自己的测试参数启动测试：

### 单测执行方法

先确保已安装 `pytest` ：

```bash
pip install pytest
```

然后在项目根目录下执行单测：

```bash
pytest
```

## 致谢

感谢感谢以下开发者对 `botpy` 作出的贡献：

<a href="https://github.com/tencent-connect/botpy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tencent-connect/botpy" />
</a>

# 加入官方社区

欢迎扫码加入**QQ 频道开发者社区**。

![开发者社区](https://guild-1251316161.cos.ap-guangzhou.myqcloud.com/miniapp/icons/qq_guild_developer_doc.png)
