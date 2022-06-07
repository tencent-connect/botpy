# -*- coding: utf-8 -*-

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

LOG_COLORS_CONFIG = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}
# 解决Windows系统cmd运行日志输出不会显示颜色问题
os.system("")


print_format = os.getenv(
    "QQBOT_LOG_PRINT_FORMAT", "\033[1;33m[%(levelname)s]\t(%(filename)s:%(lineno)s)%(funcName)s\t\033[0m%(message)s"
)
file_format = os.getenv(
    "QQBOT_LOG_FILE_FORMAT", "%(asctime)s\t[%(levelname)s]\t(%(filename)s:%(lineno)s)%(funcName)s\t%(message)s"
)


def _get_level():
    level = logging.INFO
    level_str = os.getenv("QQBOT_LOG_LEVEL", str(logging.INFO))
    try:
        level = int(level_str)
        if level not in (
            logging.NOTSET,
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ):
            logging.error("wrong logging level %s" % level_str)
            level = logging.INFO
    except ValueError:
        logging.error("wrong logging level %s" % level_str)
    logging.info("logging level: %d" % level)
    return level


def get_logger(name=None, log_path="log"):
    if not name:
        name = "botpy"
    logger = logging.getLogger(name)

    logging.basicConfig(format=print_format)

    # 从用户命令行接收是否打印debug日志
    argv = sys.argv
    if len(argv) > 1 and argv[1] in ["-d", "--debug"]:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=_get_level())

    # FileHandler
    log_flag = os.getenv("QQBOT_DISABLE_LOG", "0")
    if log_flag != "0":
        return

    formatter = logging.Formatter(file_format)
    if name is None:
        name = "botpy"
    log_file = os.path.join(os.getcwd(), log_path, f"{name}.log")

    # save last 7 days log
    try:
        file_handler = TimedRotatingFileHandler(filename=log_file, when="D", backupCount=7, encoding="utf-8")
        if len(logger.handlers) == 0:
            file_handler.setLevel(level=logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    except FileNotFoundError:
        os.makedirs(os.path.join(os.getcwd(), log_path))
        logger.warning("未找到存储日志的文件夹, 尝试重新创建成功")

    return logger
