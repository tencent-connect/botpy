# -*- coding: utf-8 -*-


class ReqOption:
    def __init__(self, before: str = None, after: str = None, limit: int = None):
        """
        获取频道列表的请求

        :param before: 读取此 guild id 之前的数据
        :param after: 读取此 guild id 之后的数据
        :param limit: 每次拉取多少条数据，最大不超过 100，默认 100
        """
        if before is not None:
            self.before = before
        if after is not None:
            self.after = after
        if limit is not None:
            self.limit = limit
