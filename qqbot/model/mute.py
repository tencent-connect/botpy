# -*- coding: utf-8 -*-


class MuteOption:
    def __init__(self, mute_end_timstamp: str, mute_seconds: str):
        """

        :param mute_end_timstamp: 禁言到期时间戳，绝对时间戳，单位：秒（与 seconds 字段同时赋值的话，以该字段为准）
        :param mute_seconds: 禁言多少秒（两个字段二选一，默认以 timeTo 为准）
        """
        self.mute_end_timstamp = mute_end_timstamp
        self.mute_seconds = mute_seconds
