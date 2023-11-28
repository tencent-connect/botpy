## 准备工作

### 安装

直接拉取吧，将 `botpy` 文件夹单独放在项目库里的 `site-packages\botpy` 中

此库`兼容版本：python3.8+`

### 使用

需要使用的地方`import botpy`

```python
import botpy
```

### 兼容提示

> 原机器人的老版本`qq-bot`仍然可以使用，但新接口的支持上会逐渐暂停，此次升级不会影响线上使用的机器人 

## 分支改变
**本分支仅在原模板中新增了对普通QQ群的操作，其余部分未改动**
### 群管理

在Intents中设置group_manage=True以启用QQ群事件
目前支持：
1. :func:`group_add_robot`: 机器人加入群聊
2. :func:`group_del_robot`: 机器人退出群聊
3. :func:`group_msg_reject`: 群聊拒绝机器人主动消息
4. :func:`group_msg_receive`: 群聊接受机器人主动消息
5. :func:`group_at_message_create`: 当收到@机器人的消息时

消息结构体可使用reply进行回复


## 致谢

感谢感谢以下开发者对 `botpy` 作出的贡献：

<a href="https://github.com/tencent-connect/botpy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tencent-connect/botpy" />
</a>

# 加入官方社区

我甚至找不到在哪加入QAQ
