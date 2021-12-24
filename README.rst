qq-bot-python
=============

sdk安装
=======

外发版本通过下面方式安装

.. code:: bash

   pip install qq-bot


更新包的话需要添加 ``--upgrade`` ``注：需要python3.7+``

sdk使用
=======

需要使用的地方import SDK

.. code:: python

   import qqbot

qqbot-API
---------

基于 https://bot.q.qq.com/wiki/develop/api/
机器人开放平台API实现的API接口封装。

使用方法
~~~~~~~~

通过 ``import`` 对应API的类来进行使用，构造参数（\ ``Token``
对象，是否沙盒模式）。

比如下面的例子，通过api当前机器人的相关信息：

.. code:: py

   import qqbot

   token = qqbot.Token("{appid}","{token}")
   api = qqbot.UserAPITestCase(token, False)
   user = api.me()

   print(user.username)  # 打印机器人名字

qqbot-事件监听
--------------

异步模块基于 websocket
技术用于监听频道内的相关事件，如消息、成员变化等事件，用于开发者对事件进行相应的处理。

.. _使用方法-1:

使用方法
~~~~~~~~

通过注册需要监听的事件并设置回调函数后，即可完成对事件的监听。

比如下面这个例子：需要监听机器人被@后消息并进行相应的回复。

-  先初始化需要用的 ``token`` 对象
-  通过 ``qqbot.listen_events`` 注册需要监听的事件
-  通过 ``qqbot.HandlerType``
   定义需要监听的事件（部分事件可能需要权限申请）

.. code:: py


   t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
   # 注册事件类型和回调，可以注册多个
   qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
   qqbot.listen_events(t_token, False, qqbot_handler)

-  最后定义注册事件回调执行函数,如 ``_message_handler`` 。

.. code:: py

   def _message_handler(event, message: Message):
       msg_api = qqbot.MessageAPI(t_token, False)
       # 打印返回信息
       qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
       # 构造消息发送请求数据对象
       send = qqbot.MessageSendRequest("<@%s>谢谢你，加油" % message.author.id, message.id)
       # 通过api发送回复消息
       msg_api.post_message(message.channel_id, send)

注：当前支持事件及回调数据对象为：

.. code:: py

   class HandlerType(Enum):
       PLAIN_EVENT_HANDLER = 0 #透传事件    
       GUILD_EVENT_HANDLER = 1 #频道事件   
       GUILD_MEMBER_EVENT_HANDLER = 2 #频道成员事件    
       CHANNEL_EVENT_HANDLER = 3 #子频道事件    
       MESSAGE_EVENT_HANDLER = 4 #消息事件    
       AT_MESSAGE_EVENT_HANDLER = 5 #At消息事件 
       # DIRECT_MESSAGE_EVENT_HANDLER = 6 #私信消息事件
       # AUDIO_EVENT_HANDLER = 7 #音频事件

事件回调函数的参数 1 为事件名称，参数 2 返回具体的数据对象。

.. code:: py

   #透传事件（无具体的数据对象，根据后台返回Json对象）
   def _plain_handler(event, data):
   #频道事件
   def _guild_handler(event, guild:Guild):
   #频道成员事件
   def _guild_member_handler(event, guild_member: GuildMember):
   #子频道事件
   def _channel_handler(event, channel: Channel):
   #消息事件 #At消息事件
   def _message_handler(event, message: Message):

日志打印
--------

基于自带的 logging
模块封装的日志模块，提供了日志写入以及美化了打印格式，并支持通过设置
``QQBOT_LOG_LEVEL`` 环境变量来调整日志打印级别（默认打印级别为
``INFO``\ ）。

.. _使用方法-2:

使用方法
~~~~~~~~

引用模块，并获取 ``logger`` 实例：

.. code:: py

   from core.util import logging

   logger = logging.getLogger(__name__)

然后就可以愉快地使用 logger 进行打印。例如：

.. code:: py

   logger.info("hello world!")

设置日志级别
~~~~~~~~~~~~

通过 ``export`` 命令添加 ``QQBOT_LOG_LEVEL``
环境变量可以设置日志级别。例如：

.. code:: bash

   export QQBOT_LOG_LEVEL=10  # 10表示DEBUG级别

几个可选取值（参考了\ `logging模块的取值 <https://docs.python.org/3/library/logging.html#levels>`__\ ）：

======== ====
Level    取值
======== ====
CRITICAL 50
ERROR    40
WARNING  30
INFO     20
DEBUG    10
NOTSET   0
======== ====

禁用日志文件输出
~~~~~~~~~~~~~~~~

默认情况下 qqbot 会在当前执行目录下生成格式为 ``qqbot.log.*``
的日志文件。如果想禁用这些日志文件，可以通过设置 ``QQBOT_DISABLE_LOG``
环境变量为 1 来关闭。

.. code:: bash

   export QQBOT_DISABLE_LOG=1  # 1表示禁用日志

