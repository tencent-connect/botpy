# -*- coding: utf-8 -*-

import logging
import os
import platform
import sys
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler

LOG_COLORS_CONFIG = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}
# 解决Windows系统cmd运行日志输出不会显示颜色问题
os.system('')

log_path = os.getenv("QQBOT_LOG_PATH", os.path.join(os.getcwd(), "%(name)s.log"))

print_format = os.getenv("QQBOT_LOG_PRINT_FORMAT",
                         "\033[1;33m[%(levelname)s] %(funcName)s (%(filename)s:%(lineno)s):\033[0m%(message)s")
file_format = os.getenv("QQBOT_LOG_FILE_FORMAT",
                        "%(asctime)s [%(levelname)s] %(funcName)s (%(filename)s:%(lineno)s): %(message)s")


def _getLevel():
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


def getLogger(name=None):
    if name is None:
        logger = logging.getLogger("qqbot")
    else:
        logger = logging.getLogger(name)

    logging.basicConfig(format=print_format)

    # 从用户命令行接收是否打印debug日志
    argv = sys.argv
    if len(argv) > 1 and argv[1] in ["-d", "--debug"]:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=_getLevel())

    # FileHandler
    no_log = os.getenv("QQBOT_DISABLE_LOG", "0")
    if no_log == "0":
        formatter = logging.Formatter(file_format)
        if name is None:
            name = "qqbot"
        log_file = log_path % {"name": name}
        file_handler = None
        if platform.system().lower() != "windows":
            # do not use RotatingFileHandler under Windows
            # due to multi-process issue
            # file_handler = RotatingFileHandler(
            #     log_file,
            #     maxBytes=1024 * 1024,
            #     backupCount=5,
            # )
            # save last 7 days log
            file_handler = TimedRotatingFileHandler(
                filename=log_file,
                when="D",
                backupCount=7,
            )
        else:
            file_handler = FileHandler(log_file, encoding="utf-8")
        if len(logger.handlers) == 0:
            file_handler.setLevel(level=logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
