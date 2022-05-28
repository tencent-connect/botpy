# botpy
**botpy** 是基于[机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的机器人框架，目的提供一个易使用、开发效率高的开发框架。

![PyPI](https://img.shields.io/pypi/v/qq-botpy)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-f17c900164974f5785c436b359876877/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](http://devops.oa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-f17c900164974f5785c436b359876877/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)


## 准备工作
```bash
pip install qq-botpy
```

更新包的话需要添加 ``--upgrade`` ``注：需要python3.7+``

需要使用的地方`import botpy`

```python 
import botpy
```

### 使用方法

1. 通过继承实现`bot.Client`, 实现自己的机器人Client 
2. 实现机器人相关事件的处理方法,如 `on_at_message_create`，具体方法定义可以参考`botpy.flags::Intents`

如下，是定义机器人被@的后自动回复:
```python
class MyClient(botpy.Client):
    async def on_ready(self):
        print(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
```
注意:
每个事件会下发具体的数据对象，如`message`相关事件是`message.Message`的对象 (部分事件透传了后台数据，暂未实现对象缓存)

如果要使用`api`方法，可以参考如下方式:
```python
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")
```

3. 设置机器人需要监听的事件通道，并启动`client`
```python
intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)
client.run(appid="12345", token="xxxx")
```

也可以通过预设置的类型，设置需要监听的事件通道
```python
intents = botpy.Intents.none()
intents.public_guild_messages=True
```

## 示例机器人

[`examples`](./examples/) 目录下存放示例机器人，可供实现参考。

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

### 修改日志输出路径

SDK也支持修改日志输出路径，由于实际路径不尽相同，所以此处使用 `os` 模块来设置临时环境变量。

```python
import os

os.environ["QQBOT_LOG_PATH"] = os.path.join(os.getcwd(), "log", "%(name)s.log") # 日志将生成在执行目录下log文件夹内
```

### 修改日志格式

通过 `export` 命令添加 `QQBOT_LOG_FILE_FORMAT` 和 `QQBOT_LOG_PRINT_FORMAT` 环境变量可以设置日志格式。例如：

```bash
 # 设置文件输出格式
export QQBOT_LOG_FILE_FORMAT="%(asctime)s [%(levelname)s] %(funcName)s (%(filename)s:%(lineno)s): %(message)s"
```

如需使用转义字符，可以使用 `os` 模块添加。例如：

```python
 # 设置控制台输出格式
import os

os.environ["QQBOT_LOG_PRINT_FORMAT"] = "%(asctime)s \033[1;33m[%(levelname)s] %(funcName)s (%(filename)s:%(lineno)s):\033[0m %(message)s"
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
