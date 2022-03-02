# -*- coding: utf-8 -*-
from qqbot.model.member import Member


class Schedule:
    def __init__(
        self,
        data=None,
        id: str = None,
        name: str = None,
        description: str = None,
        start_timestamp: str = None,
        end_timestamp: str = None,
        creator: Member = None,
        jump_channel_id: str = None,
        remind_type: str = None,
    ):
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if start_timestamp is not None:
            self.start_timestamp = start_timestamp
        if end_timestamp is not None:
            self.end_timestamp = end_timestamp
        if creator is not None:
            self.creator = creator
        if jump_channel_id is not None:
            self.jump_channel_id = jump_channel_id
        if remind_type is not None:
            self.remind_type = remind_type
        if data is not None:
            self.__dict__ = data


class GetSchedulesRequest:
    def __init__(self, since: int):
        self.since = since


class ScheduleToCreate:
    def __init__(
        self,
        name: str,
        start_timestamp: str,
        end_timestamp: str,
        remind_type: str,
        description: str = None,
        creator: Member = None,
        jump_channel_id: str = None,
    ):
        self.schedule = Schedule(
            name=name,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            remind_type=remind_type,
            description=description,
            creator=creator,
            jump_channel_id=jump_channel_id,
        )


class ScheduleToPatch:
    def __init__(
        self,
        start_timestamp: str,
        end_timestamp: str,
        remind_type: str,
        name: str = None,
        description: str = None,
        creator: Member = None,
        jump_channel_id: str = None,
    ):
        self.schedule = Schedule(
            name=name,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            remind_type=remind_type,
            description=description,
            creator=creator,
            jump_channel_id=jump_channel_id,
        )
