# -*- coding: utf-8 -*-

# This relies on each of the submodules having an __all__ variable.
from enum import Enum

from qqbot.api import *
from qqbot.async_api import *
from qqbot.core.util import logging

logger = logging.getLogger(__name__)


class HandlerType(Enum):
    PLAIN_EVENT_HANDLER = 0
    GUILD_EVENT_HANDLER = 1
    GUILD_MEMBER_EVENT_HANDLER = 2
    CHANNEL_EVENT_HANDLER = 3
    MESSAGE_EVENT_HANDLER = 4
    AT_MESSAGE_EVENT_HANDLER = 5
    DIRECT_MESSAGE_EVENT_HANDLER = 6
    AUDIO_EVENT_HANDLER = 7
