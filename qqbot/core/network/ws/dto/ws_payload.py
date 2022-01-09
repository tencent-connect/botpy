# -*- coding: utf-8 -*-

from qqbot.core.network.ws.dto.enum_intents import Intents
from qqbot.model.token import Token


class WSPayload:
    def __init__(self, d, op):
        self.op = op
        self.d = d


class WsIdentifyData:
    def __init__(self, token=Token, intents=Intents, shard=None):
        if shard is None:
            shard = []
        self.shard = shard
        self.token = token
        self.intents = intents


class WSResumeData:
    def __init__(self, token, session_id, seq):
        self.session_id = session_id
        self.token = token
        self.seq = seq


class Message:
    pass


class WSMessageData(Message):
    pass
