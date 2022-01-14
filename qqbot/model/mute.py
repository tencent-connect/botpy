# -*- coding: utf-8 -*-


class MuteOption:
    def __init__(self, mute_end_timestamp: str = None, mute_seconds: str = None):
        """

        :param mute_end_timestamp: 禁言到期时间戳，绝对时间戳，单位：秒（与 seconds 字段同时赋值的话，以该字段为准）
        :param mute_seconds: 禁言多少秒（两个字段二选一，默认以 timeTo 为准）
        """
        self.mute_end_timestamp = mute_end_timestamp
        self.mute_seconds = mute_seconds
