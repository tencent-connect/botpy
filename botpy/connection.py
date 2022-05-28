import asyncio
import inspect
from typing import List, Callable, Dict, Any, Optional

from .api import BotAPI
from .channel import Channel
from .message import Message
from .robot import Robot
from .logging import logging
from .types import gateway, channel, guild, user, session, reaction, interaction

_log = logging.getLogger()


class ConnectionSession:
    """Client的Websocket连接会话

    SessionPool主要支持session的重连,可以根据session的状态动态设置是否需要进行重连操作
    这里通过设置session_id=""空则任务session需要重连
    """

    def __init__(
        self,
        max_async,
        connect: Callable,
        dispatch: Callable,
        loop=None,
        api: BotAPI = None,
    ):
        self.dispatch = dispatch
        self.state = ConnectionState(dispatch, api)
        self.parser: Dict[str, Callable[[gateway.WsContext, Any], None]] = self.state.parsers

        self._connect = connect
        self._max_async = max_async
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        # session链接同时最大并发数
        self._session_list: List[session.Session] = []

    async def run(self, session_interval=5):
        if len(self._session_list) == 0:
            return
        # 根据并发数同时建立多个future
        index = 0
        session_list = self._session_list
        # 需要执行的链接列表，通过time_interval控制启动时间
        tasks = []

        while len(session_list) > 0:
            _log.debug("session list circle run")
            time_interval = session_interval * (index + 1)
            _log.info("[botpy]最大并发连接数: %s, 启动会话数: %s" % (self._max_async, len(session_list)))
            for i in range(self._max_async):
                if len(session_list) == 0:
                    break
                tasks.append(asyncio.ensure_future(self._runner(session_list.pop(i), time_interval), loop=self.loop))
            index += self._max_async

        await asyncio.wait(tasks)

    async def _runner(self, session, time_interval):
        await self._connect(session)
        # 后台有频率限制，根据间隔时间发起链接请求
        await asyncio.sleep(time_interval)

    def add(self, _session: session.Session):
        self._session_list.append(_session)


class ConnectionState:
    """Client的Websocket状态处理"""

    def __init__(self, dispatch: Callable, api: BotAPI):
        self.robot: Optional[Robot] = None

        self.parsers: Dict[str, Callable[[Any], None]]
        self.parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith("parse_"):
                self.parsers[attr[6:].lower()] = func

        self._dispatch = dispatch
        self.api = api

    # botpy.flags.Intents.guilds
    def parse_guild_create(self, ctx: gateway.WsContext, data: guild.GuildPayload):
        self._dispatch("guild_create", data)

    def parse_guild_update(self, ctx: gateway.WsContext, data: guild.GuildPayload):
        self._dispatch("guild_update", data)

    def parse_guild_delete(self, ctx: gateway.WsContext, data: guild.GuildPayload):
        self._dispatch("guild_delete", data)

    def parse_channel_create(self, ctx: gateway.WsContext, data: channel.ChannelPayload):
        _channel = Channel(self.api, ctx, data)
        self._dispatch("channel_create", _channel)

    def parse_channel_update(self, ctx: gateway.WsContext, data: channel.ChannelPayload):
        _channel = Channel(self.api, ctx, data)
        self._dispatch("channel_update", _channel)

    def parse_channel_delete(self, ctx: gateway.WsContext, data: channel.ChannelPayload):
        _channel = Channel(self.api, ctx, data)
        self._dispatch("channel_delete", _channel)

    # botpy.flags.Intents.guild_members
    def parse_guild_member_add(self, ctx: gateway.WsContext, data: user.GuildMemberPayload):
        self._dispatch("guild_member_add", data)

    def parse_guild_member_update(self, ctx: gateway.WsContext, data: user.GuildMemberPayload):
        self._dispatch("guild_member_update", data)

    def parse_guild_member_remove(self, ctx: gateway.WsContext, data: user.GuildMemberPayload):
        self._dispatch("guild_member_remove", data)

    # botpy.flags.Intents.guild_messages
    def parse_message_create(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("message_create", message)

    def parse_message_delete(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("message_delete", message)

    # botpy.flags.Intents.guild_message_reactions
    def parse_message_reaction_add(self, ctx: gateway.WsContext, data: reaction.Reaction):
        self._dispatch("message_reaction_add", data)

    def parse_message_reaction_remove(self, ctx: gateway.WsContext, data: reaction.Reaction):
        self._dispatch("message_reaction_remove", data)

    # botpy.flags.Intents.direct_message
    def parse_direct_message_create(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("direct_message_create", message)

    def parse_direct_message_delete(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("direct_message_delete", message)

    # botpy.flags.Intents.interaction
    def parse_interaction_create(self, ctx: gateway.WsContext, data: interaction.InteractionPayload):
        self._dispatch("interaction_create", data)

    # botpy.flags.Intents.message_audit
    def parse_message_audit_pass(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("direct_message_create", message)

    def parse_message_audit_reject(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("direct_message_delete", message)

    # botpy.flags.Intents.audio_action
    def parse_audio_start(self, ctx: gateway.WsContext, data):
        self._dispatch("direct_message_create", data)

    def parse_audio_finish(self, ctx: gateway.WsContext, data):
        self._dispatch("direct_message_delete", data)

    def parse_on_mic(self, ctx: gateway.WsContext, data):
        self._dispatch("direct_message_create", data)

    def parse_off_mic(self, ctx: gateway.WsContext, data):
        self._dispatch("direct_message_delete", data)

    # botpy.flags.Intents.public_guild_messages
    def parse_at_message_create(self, ctx: gateway.WsContext, data: gateway.MessagePayload):
        message = Message(self.api, data)
        self._dispatch("at_message_create", message)

    def parse_ready(self, ctx: gateway.WsContext, data: gateway.ReadyEvent):
        self._dispatch("ready")

    def parse_resumed(self, ctx: gateway.WsContext, data: gateway.ReadyEvent):
        self._dispatch("resumed")
