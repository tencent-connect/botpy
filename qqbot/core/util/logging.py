# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_COLORS_CONFIG = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}


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


def getLogger(name):
    print_format = (
        """\033[1;33m%(levelname)s: %(name)s(line: %(lineno)s):\033[0m%(message)s"""
    )
    file_format = "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - line %(lineno)s - %(levelname)s - %(message)s"

    logger = logging.getLogger(name)
    logging.basicConfig(format=print_format)
    logger.setLevel(level=_getLevel())

    # FileHandler
    no_log = os.getenv("QQBOT_DISABLE_LOG", "0")
    if no_log == "0":
        formatter = logging.Formatter(file_format)
        log_file = os.path.join(os.getcwd(), "qqbot.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,
            backupCount=5,
        )
        logger.debug(
            "qqbot: dumping log file to {path}".format(path=os.path.realpath(log_file))
        )
        file_handler.setLevel(level=_getLevel())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
