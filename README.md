# qq-bot-python
![PyPI](https://img.shields.io/pypi/v/qq-bot)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-f17c900164974f5785c436b359876877/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](http://devops.oa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-f17c900164974f5785c436b359876877/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)

## sdk安装

外发版本通过下面方式安装

``` bash
pip install qq-bot  # 注意是 qq-bot 而不是 qqbot！
```

更新包的话需要添加 ``--upgrade`` ``注：需要python3.7+``

## sdk使用

需要使用的地方import SDK

```python
import qqbot
```

## 示例机器人

[`examples`](./examples/) 目录下存放示例机器人，可供实现参考。

## qqbot-API

基于 https://bot.q.qq.com/wiki/develop/api/ 机器人开放平台API实现的API接口封装。

### 使用方法

通过 `import` 对应API的类来进行使用，构造参数（`Token` 对象，是否沙盒模式）。

比如下面的例子，通过api当前机器人的相关信息：

``` py
import qqbot

token = qqbot.Token("{appid}","{token}")
api = qqbot.UserAPI(token, False)

user = api.me()

print(user.username)  # 打印机器人名字
```

async 示例：

``` py
import qqbot

token = qqbot.Token("{appid}","{token}")
api = qqbot.AsyncUserAPI(token, False)

# 获取loop
loop = asyncio.get_event_loop()
user = loop.run_until_complete(api.me())

print(user.username)  # 打印机器人名字
```

## qqbot-事件监听

异步模块基于 websocket 技术用于监听频道内的相关事件，如消息、成员变化等事件，用于开发者对事件进行相应的处理。

### 使用方法

通过注册需要监听的事件并设置回调函数后，即可完成对事件的监听。

比如下面这个例子：需要监听机器人被@后消息并进行相应的回复。

- 先初始化需要用的 `token` 对象（ `appid`和`token`参数从机器人管理端获取 ）
- 通过 `qqbot.listen_events` 注册需要监听的事件
- 通过 `qqbot.HandlerType` 定义需要监听的事件（部分事件可能需要权限申请）

  ``` py
  token = qqbot.Token("{appid}","{token}")
  # 注册事件类型和回调，可以注册多个
  qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
  qqbot.listen_events(token, False, qqbot_handler)
  ```

- 最后定义注册事件回调执行函数,如 `_message_handler` 。

  ``` py
  def _message_handler(event, message: Message):
      msg_api = qqbot.MessageAPI(token, False)
      # 打印返回信息
      qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
      # 构造消息发送请求数据对象
      send = qqbot.MessageSendRequest("<@%s>谢谢你，加油" % message.author.id, message.id)
      # 通过api发送回复消息
      msg_api.post_message(message.channel_id, send)
  ```

- async 示例:

  ``` py
  # async的异步接口的使用示例
  token = qqbot.Token("{appid}","{token}")
  qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
  qqbot.async_listen_events(token, False, qqbot_handler)
  ```
  ``` py
  async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理

    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
    for i in range(5):
        await asyncio.sleep(5)
        # 构造消息发送请求数据对象
        send = qqbot.MessageSendRequest("<@%s>谢谢你，加油 " % message.author.id, message.id)
        # 通过api发送回复消息
        await msg_api.post_message(message.channel_id, send)

  ```
- 注：当前支持事件及回调数据对象为：

  ``` py
  class HandlerType(Enum):
      PLAIN_EVENT_HANDLER = 0  # 透传事件
      GUILD_EVENT_HANDLER = 1  # 频道事件
      GUILD_MEMBER_EVENT_HANDLER = 2  # 频道成员事件
      CHANNEL_EVENT_HANDLER = 3  # 子频道事件
      MESSAGE_EVENT_HANDLER = 4  # 消息事件
      AT_MESSAGE_EVENT_HANDLER = 5  # At消息事件
      # DIRECT_MESSAGE_EVENT_HANDLER = 6  # 私信消息事件
      # AUDIO_EVENT_HANDLER = 7  # 音频事件
  ```

  事件回调函数的参数 1 为事件名称，参数 2 返回具体的数据对象。

  ``` py
  # 透传事件（无具体的数据对象，根据后台返回Json对象）
  def _plain_handler(event, data):
  # 频道事件
  def _guild_handler(event, guild:Guild):
  # 频道成员事件
  def _guild_member_handler(event, guild_member: GuildMember):
  # 子频道事件
  def _channel_handler(event, channel: Channel):
  # 消息事件
  # At消息事件
  def _message_handler(event, message: Message):
  ```

## 日志打印

基于自带的 logging 模块封装的日志模块，提供了日志写入以及美化了打印格式，并支持通过设置 `QQBOT_LOG_LEVEL` 环境变量来调整日志打印级别（默认打印级别为 `INFO`）。

### 使用方法

引用模块，并获取 `logger` 实例：

``` py
from core.util import logging

logger = logging.getLogger()
```

或者通过`qqbot.logger`也可以获取logger对象

然后就可以愉快地使用 logger 进行打印。例如：

``` py
logger.info("hello world!")
```

### 设置日志级别
SDK默认的日志级别为`INFO`级别，需要修改请查看下面信息
#### Debug日志
命令行启动py后通过增加参数`-d` 或 `--debug`可以打开debug日志

```bash
python3 demo_at_reply.py -d
```


#### 其他级别日志
通过 `export` 命令添加 `QQBOT_LOG_LEVEL` 环境变量可以设置日志级别。例如：

``` bash
export QQBOT_LOG_LEVEL=10  # 10表示DEBUG级别
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

### 禁用日志文件输出

默认情况下 qqbot 会在当前执行目录下生成格式为 `qqbot.log.*` 的日志文件。如果想禁用这些日志文件，可以通过设置 `QQBOT_DISABLE_LOG` 环境变量为 1 来关闭。

``` bash
export QQBOT_DISABLE_LOG=1  # 1表示禁用日志
```

# sdk开发

## 环境配置

``` bash
pip install -r requirements.txt   # 安装依赖的pip包

pre-commit install                 # 安装格式化代码的钩子
```

## 单元测试

代码库提供API接口测试和 websocket 的单测用例，位于 `tests` 目录中。如果需要自己运行，可以在 `tests` 目录重命名 `.test.yaml` 文件后添加自己的测试参数启动测试：

```yaml
# test yaml 用于设置test相关的参数，开源版本需要去掉参数
token:
  appid: "xxx"
  token: "xxxxx"
test_params:
  guild_id: "xx"
  guild_owner_id: "xx"
  guild_owner_name: "xx"
  guild_test_member_id: "xx"
  guild_test_role_id: "xx"
  channel_id: "xx"
  channel_name: "xx"
  robot_name: "xxx"
  is_sandbox: False
```

单测执行方法：

先确保已安装 `pytest` ：

``` bash
pip install pytest
```

然后在项目根目录下执行单测：

``` bash
pytest
```

# 加入官方社区

欢迎扫码加入**QQ 频道开发者社区**。

![开发者社区](https://mpqq.gtimg.cn/privacy/qq_guild_developer.png)
