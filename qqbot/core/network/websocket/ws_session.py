# -*- coding: utf-8 -*-

from qqbot.model.token import Token


class Intent:
    pass


class ShardConfig:
    def __init__(self, shard_id, shard_count):
        self.shard_id = shard_id
        self.shard_count = shard_count


class Session:
    def __init__(
        self, session_id, url, intent, last_seq, token=Token, shards=ShardConfig
    ):
        self.shards = shards
        self.last_seq = last_seq
        self.intent = intent
        self.token = token
        self.url = url
        self.session_id = session_id
