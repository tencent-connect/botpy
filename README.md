# botpy
**botpy** 是基于[机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的机器人框架，目的提供一个易使用、开发效率高地开发框架。

![PyPI](https://img.shields.io/pypi/v/qq-botpy)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-713959939bdc4adca0eea2d4420eef4b/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](https://devops.woa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-713959939bdc4adca0eea2d4420eef4b/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)

## 准备工作
### 安装
```bash
pip install qq-botpy
```

更新包的话需要添加 ``--upgrade`` ``注：需要python3.7+``

### 使用
需要使用的地方`import botpy`

```python 
import botpy
```

### 兼容提示
> 原机器人的老版本`qq-bot`仍然可以使用，但新接口的支持上会逐渐暂停，此次升级不会影响线上使用的机器人 


## 使用方式
### 快速入门

#### 步骤1
通过继承实现`bot.Client`, 实现自己的机器人Client 

#### 步骤2
实现机器人相关事件的处理方法,如 `on_at_message_create`， 详细的事件监听列表，请参考 [事件监听.md](./docs/事件监听.md)

如下，是定义机器人被@的后自动回复:
```python
import botpy
from botpy.types.message import Message

class MyClient(botpy.Client):
    async def on_ready(self):
        print(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
```

``注意:每个事件会下发具体的数据对象，如`message`相关事件是`message.Message`的对象 (部分事件透传了后台数据，暂未实现对象缓存)``

#### 步骤3
设置机器人需要监听的事件通道，并启动`client`
```python
import botpy
from botpy.types.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")

intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)
client.run(appid="12345", token="xxxx")
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
from botpy.types.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")
```

## 示例机器人

[`examples`](./examples/) 目录下存放示例机器人，具体使用可参考[`Readme.md`](./examples/README.md) 

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
```

## 日志打印

基于自带的 logging 模块封装的日志模块，提供了日志写入以及美化了打印格式，并支持调整打印级别（默认打印级别为 `INFO`）。

### 使用方法

引用模块，并获取 `logger` 实例：

``` python
from botpy import logging

logger = logging.get_logger()
```

或者通过`botpy.logger`也可以获取logger对象

然后就可以愉快地使用 logger 进行打印。例如：

``` python
logger.info("hello world!")
```

### 日志设置

目前，SDK的日志设置集成在Client的实例化阶段，也可通过logging.configure_logging修改(均为可选)

```python
from botpy import Client

Client(
    log_level=20,
    log_format="new format",
    bot_log=True,
    ext_handlers=False,
    log_config="log_config.json",
)

```

### log_level

修改日志级别，默认为`INFO`

命令行启动py可增加参数`-d` 或 `--debug`快捷打开debug日志

```bash
python3 demo_at_reply.py -d
```

几个可选取值（参考了[logging模块的取值](https://docs.python.org/3/library/logging.html#levels)）：

| Level | 取值 |
| ----- | ------------- |
| CRITICAL  | 50  |
| ERROR | 40 |
| WARNING | 30 |
| INFO | 20 |
| DEBUG | 10 |
| NOTSET | 0 |

### log_format

日志控制台输出格式

### bot_log

是否启用`botpy`日志

None -> 禁用 拓展  
False -> 禁用 拓展+控制台输出

### ext_handlers

日志Handler拓展，为True使用默认拓展，False不添加拓展，可用list添加多个拓展

[默认拓展](botpy/logging.py)

```yaml
{
    # 要实例化的Handler
    "handler": TimedRotatingFileHandler,
    # 可选 Default to DEFAULT_FILE_FORMAT
    "format": "%(asctime)s\t[%(levelname)s]\t(%(filename)s:%(lineno)s)%(funcName)s\t%(message)s",
    # 可选 Default to DEBUG
    "level": logging.DEBUG,
    # 可选，其中如有 %(name)s 会在实例化阶段填入相应的日志name
    "filename": os.path.join(os.getcwd(), "%(name)s.log"),
    # 以下是Handler相关参数
    "when": "D",
    "backupCount": 7,
    "encoding": "utf-8"
}
```

#### 修改默认拓展

```python
import os
from botpy import Client
from botpy.logging import DEFAULT_FILE_HANDLER

# 修改日志路径
DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")
# 修改日志格式
DEFAULT_FILE_HANDLER["format"] = "new format"

Client(ext_handlers=DEFAULT_FILE_HANDLER)
```

### log_config

该参数将传入`logging.config.dictConfig`(内置logging而非botpy.logging)，如果为.json/.yaml文件路径将从文件中读取配置

# 参与开发

## 环境配置

``` bash
pip install -r requirements.txt   # 安装依赖的pip包

pre-commit install                 # 安装格式化代码的钩子
```

## 单元测试

代码库提供API接口测试和 websocket 的单测用例，位于 `tests` 目录中。如果需要自己运行，可以在 `tests` 目录重命名 `.test.yaml` 文件后添加自己的测试参数启动测试：

### 单测执行方法

先确保已安装 `pytest` ：

``` bash
pip install pytest
```

然后在项目根目录下执行单测：

``` bash
pytest
```

## 致谢

感谢参与内测、开发和提出宝贵意见的开发者们（排名不分先后）：

[小念](https://github.com/ReadSmall), [Neutron](https://github.com/Huang1220), [晚柒载](https://github.com/wqzai)

# 加入官方社区

欢迎扫码加入**QQ 频道开发者社区**。

![开发者社区](https://mpqq.gtimg.cn/privacy/qq_guild_developer.png)