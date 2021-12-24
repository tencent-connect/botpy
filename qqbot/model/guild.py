# -*- coding: utf-8 -*-


class Guild:
    def __init__(self, data=None):
        self.id: str = ""
        self.name: str = ""
        self.icon: str = ""
        self.owner_id: str = ""
        self.owner: bool = False
        self.member_count: int = 0
        self.max_members: int = 0
        self.description: str = ""
        self.joined_at: str = ""
        if data:
            self.__dict__ = data
