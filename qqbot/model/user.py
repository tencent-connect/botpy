# -*- coding: utf-8 -*-


class ReqOption:
    def __init__(self, before: str, after: str, limit: str):
        """
        获取频道列表的请求

        :param before: 读取此 id 之前的数据
        :param after: 读取此 id 之后的数据
        :param limit: 每次拉取多少条数据，最大不超过 100，默认 100
        """

        self.before = before
        self.after = after
        self.limit = limit
