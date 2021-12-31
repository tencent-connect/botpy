# examples

该目录用于存放基于 botpy 开发的机器人的完整示例。

```
examples/
 ┣ README.md
 ┣ config.example.yaml  # 示例配置文件
 ┗ run_websocket.py  # 机器人被动回复示例
```

## 环境安装

``` bash
pip install qq-bot
```

## 使用方法

1. 拷贝 config.example.yaml 为 config.yaml ：

    ``` bash
    cp config.example.yaml config.yaml
    ```

2. 修改 config.yaml ，填入自己的 BotAppID 和  Bot token 。
3. 运行机器人。例如：

    ``` bash
    python3 run_websocket.py
    ```
