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
