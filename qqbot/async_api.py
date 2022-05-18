# -*- coding: utf-8 -*-

# 异步api
import json
from json import JSONDecodeError
from typing import List

from qqbot import WebsocketAPI
from qqbot.core.network.async_http import AsyncHttp
from qqbot.core.network.url import get_url, APIConstant
from qqbot.core.network.ws.ws_intents_handler import Handler, register_handlers
from qqbot.core.network.ws_async.ws_async_manager import SessionManager
from qqbot.core.util.json_util import JsonUtil
from qqbot.model.announce import (
    CreateAnnounceRequest,
    Announce,
    CreateChannelAnnounceRequest,
    RecommendChannelRequest,
)
from qqbot.model.api_permission import (
    APIPermission,
    PermissionDemandToCreate,
    APIPermissionDemand,
    APIs,
)
from qqbot.model.audio import AudioControl
from qqbot.model.channel import (
    Channel,
    ChannelResponse,
    CreateChannelRequest,
    PatchChannelRequest,
)
from qqbot.model.channel_permissions import (
    ChannelPermissions,
    UpdatePermission,
)
from qqbot.model.guild import Guild
from qqbot.model.guild_member import QueryParams
from qqbot.model.guild_role import (
    GuildRoles,
    RoleUpdateResult,
    RoleUpdateRequest,
    RoleUpdateFilter,
    RoleUpdateInfo,
)
from qqbot.model.interaction import InteractionData
from qqbot.model.member import User, Member
from qqbot.model.message import (
    MessageSendRequest,
    Message,
    CreateDirectMessageRequest,
    DirectMessageGuild,
    MessagesPager,
    MessageGet,
    MessageKeyboard,
)
from qqbot.model.mute import (
    MuteOption,
    MultiMuteOption,
    UserIds,
)
from qqbot.model.pins_message import PinsMessage
from qqbot.model.schedule import (
    Schedule,
    GetSchedulesRequest,
    ScheduleToCreate,
    ScheduleToPatch,
)
from qqbot.model.token import Token
from qqbot.model.user import ReqOption
from qqbot.model.reaction import (
    ReactionUsers,
    ReactionUsersPager,
)


def async_listen_events(t_token: Token, is_sandbox: bool, *handlers: Handler, ret_coro=False):
    """
    异步注册并监听频道相关事件

    :param t_token: Token对象
    :param handlers: 包含事件类型和事件回调的Handler对象，支持多个对象
    :param is_sandbox:是否沙盒环境，默认为False
    :param ret_coro: 是否返回协程对象
    """
    # 通过api获取websocket链接
    ws_api = WebsocketAPI(t_token, is_sandbox)
    ws_ap = ws_api.ws()
    # 新建和注册监听事件
    t_intent = register_handlers(handlers)
    # 实例一个session_manager
    manager = SessionManager(ret_coro=ret_coro)
    return manager.start(ws_ap, t_token.bot_token(), t_intent)


class AsyncAPIBase:
    def __init__(self, token: Token, is_sandbox: bool, timeout: int = 3):
        """
        API初始化信息

        :param token: Token对象
        :param is_sandbox: 是否沙盒环境
        :param timeout: 设置超时时间
        """
        self.is_sandbox = is_sandbox
        self.token = token
        self.http_async = AsyncHttp(timeout, token.get_string(), token.get_type())


class AsyncGuildAPI(AsyncAPIBase):
    """
    频道相关接口
    """

    async def get_guild(self, guild_id: str) -> Guild:
        """
        获取频道信息

        :param guild_id: 频道ID（一般从事件中获取相关的ID信息）
        :return: 频道Guild对象
        """
        url = get_url(APIConstant.guildURI, self.is_sandbox).format(guild_id=guild_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=Guild)


class AsyncGuildRoleAPI(AsyncAPIBase):
    """
    频道身份组相关接口
    """

    async def get_guild_roles(self, guild_id: str) -> GuildRoles:
        """
        获取频道身份组列表

        :param guild_id:频道ID
        :return:GuildRoles对象
        """
        url = get_url(APIConstant.rolesURI, self.is_sandbox).format(guild_id=guild_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=GuildRoles)

    async def create_guild_role(self, guild_id: str, role_info: RoleUpdateInfo) -> RoleUpdateResult:
        """
        创建频道身份组

        :param guild_id:频道ID
        :param role_info:RoleUpdateInfo对象，需要自己创建的身份数据
        :return:RoleUpdateResult对象
        """
        url = get_url(APIConstant.rolesURI, self.is_sandbox).format(guild_id=guild_id)
        params = RoleUpdateRequest()
        params.filter = RoleUpdateFilter(1, 1, 1)
        params.guild_id = guild_id
        params.info = role_info
        serialize = JsonUtil.obj2json_serialize(params)
        response = await self.http_async.post(url, request=serialize)
        return json.loads(response, object_hook=RoleUpdateResult)

    async def update_guild_role(self, guild_id: str, role_id: str, role_info: RoleUpdateInfo) -> RoleUpdateResult:
        """
        修改频道身份组

        :param guild_id:频道ID
        :param role_id:身份组ID
        :param role_info:更新后的RoleUpdateInfo对象
        :return:RoleUpdateResult对象
        """
        url = get_url(APIConstant.roleURI, self.is_sandbox).format(guild_id=guild_id, role_id=role_id)
        params = RoleUpdateRequest()
        params.filter = RoleUpdateFilter(1, 1, 1)
        params.guild_id = guild_id
        params.info = role_info
        serialize = JsonUtil.obj2json_serialize(params)
        response = await self.http_async.patch(url, request=serialize)
        return json.loads(response, object_hook=RoleUpdateResult)

    async def delete_guild_role(self, guild_id: str, role_id: str) -> bool:
        """
        删除频道身份组

        :param guild_id: 频道ID
        :param role_id: 身份组ID
        :return: 是否删除成功
        """
        url = get_url(APIConstant.roleURI, self.is_sandbox).format(guild_id=guild_id, role_id=role_id)
        response = await self.http_async.delete(url)
        return response == ""

    async def create_guild_role_member(
        self,
        guild_id: str,
        role_id: str,
        user_id: str,
        role_req: Channel = None,
    ) -> bool:
        """
        增加频道身份组成员
        需要使用的 token 对应的用户具备删除身份组成员权限。如果是机器人，要求被添加为管理员。
        如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        :param guild_id:频道ID
        :param role_id:身份组ID
        :param user_id:用户ID
        :param role_req:RoleMemberRequest数据对象
        :return:是否添加成功
        """
        url = get_url(APIConstant.memberRoleURI, self.is_sandbox).format(
            guild_id=guild_id, role_id=role_id, user_id=user_id
        )
        response = await self.http_async.put(url, request=JsonUtil.obj2json_serialize(role_req))
        return response == ""

    async def delete_guild_role_member(
            self,
            guild_id: str,
            role_id: str,
            user_id: str,
            role_req: Channel = None
    ) -> bool:
        """
        删除频道身份组成员
        需要使用的 token 对应的用户具备删除身份组成员权限。如果是机器人，要求被添加为管理员。
        如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        :param guild_id:频道ID
        :param role_id:身份组ID
        :param user_id:用户ID
        :param role_req:RoleMemberRequest数据对象
        :return:是否删除成功
        """
        url = get_url(APIConstant.memberRoleURI, self.is_sandbox).format(
            guild_id=guild_id, role_id=role_id, user_id=user_id
        )
        response = await self.http_async.delete(url, request=JsonUtil.obj2json_serialize(role_req))
        return response == ""


class AsyncGuildMemberAPI(AsyncAPIBase):
    """
    成员相关接口，添加成员到用户组等
    """

    async def get_guild_member(self, guild_id: str, user_id: str) -> Member:
        """
        获取频道指定成员

        :param guild_id:频道ID
        :param user_id:用户ID（一般从事件消息中获取）
        :return:
        """
        url = get_url(APIConstant.guildMemberURI, self.is_sandbox).format(guild_id=guild_id, user_id=user_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=Member)

    async def get_guild_members(self, guild_id: str, guild_member_pager: QueryParams) -> List[Member]:
        """
        获取成员列表，需要申请接口权限

        :param guild_id: 频道ID
        :param guild_member_pager: GuildMembersPager分页数据对象
        :return: Member列表
        """
        url = get_url(APIConstant.guildMembersURI, self.is_sandbox).format(guild_id=guild_id)
        response = await self.http_async.get(url, params=guild_member_pager.__dict__)
        return json.loads(response, object_hook=Member)


class AsyncChannelAPI(AsyncAPIBase):
    """子频道相关接口"""

    async def get_channel(self, channel_id) -> Channel:
        """
        获取子频道信息

        :param channel_id:子频道ID
        :return:子频道对象Channel
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(channel_id=channel_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=Channel)

    async def get_channels(self, guild_id: str) -> List[Channel]:
        """
        获取频道下的子频道列表

        :param guild_id: 频道ID
        :return: Channel列表
        """
        url = get_url(APIConstant.channelsURI, self.is_sandbox).format(guild_id=guild_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=Channel)

    async def create_channel(self, guild_id: str, request: CreateChannelRequest) -> ChannelResponse:
        """
        创建子频道

        :param guild_id: 频道ID
        :param request: 创建子频道的请求对象CreateChannelRequest
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelsURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=ChannelResponse)

    async def update_channel(self, channel_id: str, request: PatchChannelRequest) -> ChannelResponse:
        """
        修改子频道

        :param channel_id: 频道ID
        :param request: PatchChannelRequest
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.patch(url, request_json)
        return json.loads(response, object_hook=ChannelResponse)

    async def delete_channel(self, channel_id: str) -> ChannelResponse:
        """
        删除子频道

        :param channel_id: 频道ID
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(channel_id=channel_id)
        response = await self.http_async.delete(url)
        return json.loads(response, object_hook=ChannelResponse)


class AsyncChannelPermissionsAPI(AsyncAPIBase):
    """子频道权限相关接口"""

    async def get_channel_permissions(self, channel_id: str, user_id: str) -> ChannelPermissions:
        """
        获取指定子频道的权限

        :param channel_id:子频道ID
        :param user_id:用户ID
        :return:ChannelPermissions对象
        """
        url = get_url(APIConstant.channelPermissionsURI, self.is_sandbox).format(channel_id=channel_id, user_id=user_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=ChannelPermissions)

    async def update_channel_permissions(self, channel_id, user_id, request: UpdatePermission) -> bool:
        """
        修改指定子频道的权限

        :param channel_id:子频道ID
        :param user_id:用户ID
        :param request:ChannelPermissionsUpdateRequest数据对象（构造可以查看具体的对象注释）
        :return:
        """
        url = get_url(APIConstant.channelPermissionsURI, self.is_sandbox).format(channel_id=channel_id, user_id=user_id)
        if request.add != "":
            request.add = str(int(request.add, 16))
        if request.remove != "":
            request.remove = str(int(request.remove, 16))
        response = await self.http_async.put(url, request=JsonUtil.obj2json_serialize(request))
        return response == ""

    async def get_channel_role_permissions(self, channel_id: str, role_id: str) -> ChannelPermissions:
        """
        获取指定子频道的权限

        :param channel_id:子频道ID
        :param role_id:身份组ID
        :return:ChannelPermissions对象
        """
        url = get_url(APIConstant.channelRolePermissionsURI, self.is_sandbox).format(
            channel_id=channel_id, role_id=role_id
        )
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=ChannelPermissions)

    async def update_channel_role_permissions(self, channel_id: str, role_id: str, request: UpdatePermission) -> bool:
        """
        修改指定子频道的权限

        :param channel_id:子频道ID
        :param role_id:身份组ID
        :param request:ChannelPermissionsUpdateRequest数据对象（构造可以查看具体的对象注释）
        :return:
        """
        url = get_url(APIConstant.channelRolePermissionsURI, self.is_sandbox).format(
            channel_id=channel_id, role_id=role_id
        )
        if request.add != "":
            request.add = str(int(request.add, 16))
        if request.remove != "":
            request.remove = str(int(request.remove, 16))
        response = await self.http_async.put(url, request=JsonUtil.obj2json_serialize(request))
        return response == ""


class AsyncMessageAPI(AsyncAPIBase):
    """消息"""

    async def get_message(self, channel_id: str, message_id: str) -> MessageGet:
        """
        获取指定消息

        :param channel_id: 频道ID
        :param message_id: 消息ID
        :return: Message 对象
        """
        url = get_url(APIConstant.messageURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=MessageGet)

    async def get_messages(self, channel_id: str, pager: MessagesPager) -> List[Message]:
        """
        获取指定消息列表

        :param channel_id: 频道ID
        :param pager: MessagesPager对象
        :return: Message 对象
        """
        url = get_url(APIConstant.messagesURI, self.is_sandbox).format(channel_id=channel_id)
        query = {}
        if pager.limit != "":
            query["limit"] = pager.limit

        if pager.type != "" and pager.id != "":
            query[pager.type] = pager.id

        response = await self.http_async.get(url, params=query)
        return json.loads(response, object_hook=Message)

    async def post_message(self, channel_id: str, message_send: MessageSendRequest) -> Message:
        """
        发送消息

        要求操作人在该子频道具有发送消息的权限。
        发送成功之后，会触发一个创建消息的事件。
        被动回复消息有效期为 5 分钟
        主动推送消息每日每个子频道限 2 条
        发送消息接口要求机器人接口需要链接到websocket gateway 上保持在线状态

        :param channel_id: 子频道ID
        :param message_send: MessageSendRequest对象
        :return: Message对象
        """

        url = get_url(APIConstant.messagesURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(message_send)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Message)

    async def recall_message(self, channel_id: str, message_id: str, hide_tip: bool = False):
        """
        撤回消息

        管理员可以撤回普通成员的消息
        频道主可以撤回所有人的消息

        :param channel_id: 子频道ID
        :param message_id: 消息ID
        :param hide_tip: 是否隐藏撤回提示小灰条
        """
        url = get_url(APIConstant.messageURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
        response = await self.http_async.delete(url, params={"hidetip": str(hide_tip)})
        return response == ""

    async def post_keyboard_message(self, channel_id: str, keyboard: MessageKeyboard) -> Message:
        """
        发送含有消息按钮组件的消息

        :param channel_id: 子频道ID
        :param keyboard: MessageKeyboard对象
        :return: Message对象
        """
        url = get_url(APIConstant.messagesURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(keyboard)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Message)


class AsyncDmsAPI(AsyncAPIBase):
    """私信消息"""

    async def create_direct_message(self, create_direct_message: CreateDirectMessageRequest) -> DirectMessageGuild:
        """
        创建私信频道

        :param create_direct_message: 构造request数据
        :return: 私信频道对象
        """
        url = get_url(APIConstant.userMeDMURI, self.is_sandbox)
        request_json = JsonUtil.obj2json_serialize(create_direct_message)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=DirectMessageGuild)

    async def post_direct_message(self, guild_id: str, message_send: MessageSendRequest) -> Message:
        """
        发送私信

        :param guild_id: 创建的私信频道id
        :param message_send: 发送消息的数据请求对象 MessageSendRequest
        :return Message对象
        """
        url = get_url(APIConstant.dmsURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(message_send)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Message)


class AsyncAudioAPI(AsyncAPIBase):
    """音频接口"""

    async def post_audio(self, channel_id: str, audio_control: AudioControl) -> bool:
        """
        音频控制

        :param channel_id:频道ID
        :param audio_control:AudioControl对象
        :return:是否成功
        """
        url = get_url(APIConstant.audioControlURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(audio_control)
        response = await self.http_async.post(url, request=request_json)
        return response == ""


class AsyncUserAPI(AsyncAPIBase):
    """用户相关接口"""

    async def me(self) -> User:
        """
        :return:使用当前用户信息填充的 User 对象
        """
        url = get_url(APIConstant.userMeURI, self.is_sandbox)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=User)

    async def me_guilds(self, option: ReqOption = None) -> List[Guild]:
        """
        当前用户所加入的 Guild 对象列表

        :param option: ReqOption对象
        :return:Guild对象列表
        """
        url = get_url(APIConstant.userMeGuildsURI, self.is_sandbox)
        if option is None:
            query = {}
        else:
            query = option.__dict__

        response = await self.http_async.get(url, params=query)
        return json.loads(response, object_hook=Guild)


class AsyncWebsocketAPI(AsyncAPIBase):
    """WebsocketAPI"""

    async def ws(self):
        url = get_url(APIConstant.gatewayBotURI, self.is_sandbox)
        response = await self.http_async.get(url)
        websocket_ap = json.loads(response)
        return websocket_ap


class AsyncMuteAPI(AsyncAPIBase):
    """禁言接口"""

    async def mute_all(self, guild_id: str, options: MuteOption):
        """
        禁言全员

        :param guild_id: 频道ID
        :param options: MuteOptions对象
        """
        url = get_url(APIConstant.guildMuteURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(options)
        response = await self.http_async.patch(url, request=request_json)
        return response == ""

    async def mute_member(self, guild_id: str, user_id: str, options: MuteOption):
        """
        禁言指定成员

        :param guild_id: 频道ID
        :param user_id: 用户ID
        :param options: MuteOptions对象
        """
        url = get_url(APIConstant.guildMemberMuteURI, self.is_sandbox).format(guild_id=guild_id, user_id=user_id)
        request_json = JsonUtil.obj2json_serialize(options)
        response = await self.http_async.patch(url, request=request_json)
        return response == ""

    async def mute_multi_member(self, guild_id: str, options: MultiMuteOption):
        """
        禁言指定用户

        :param guild_id: 频道ID
        :param options: MultiMuteOption对象
        """
        url = get_url(APIConstant.guildMuteURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(options)
        response = await self.http_async.patch(url, request=request_json)
        user_ids = json.loads(response, object_hook=UserIds)
        return user_ids.user_ids


class AsyncAnnouncesAPI(AsyncAPIBase):
    """公告接口"""

    async def create_announce(self, guild_id: str, request: CreateAnnounceRequest) -> Announce:
        """
        创建频道全局公告

        :param guild_id: 频道ID
        :param request: CreateAnnounceRequest对象
        """
        url = get_url(APIConstant.guildAnnounceURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Announce)

    async def delete_announce(self, guild_id: str, message_id: str):
        """
        删除频道全局公告
        message_id 有值时，会校验 message_id 合法性，若不校验校验 message_id，请将 message_id 设置为 all

        :param guild_id: 频道ID
        :param message_id: 消息ID
        """
        url = get_url(APIConstant.deleteGuildAnnounceURI, self.is_sandbox).format(
            guild_id=guild_id, message_id=message_id
        )
        response = await self.http_async.delete(url)
        return response == ""

    async def create_channel_announce(self, channel_id: str, request: CreateChannelAnnounceRequest) -> Announce:
        """
        设置消息为指定子频道公告

        :param channel_id: 频道ID
        :param request: CreateChannelAnnounceRequest对象
        """
        url = get_url(APIConstant.channelAnnounceURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Announce)

    async def delete_channel_announce(self, channel_id: str, message_id: str):
        """
        删除子频道公告
        message_id 有值时，会校验 message_id 合法性，若不校验校验 message_id，请将 message_id 设置为 all

        :param channel_id: 频道ID
        :param message_id: 消息ID
        """
        url = get_url(APIConstant.deleteChannelAnnounceURI, self.is_sandbox).format(
            channel_id=channel_id, message_id=message_id
        )
        response = await self.http_async.delete(url)
        return response == ""

    async def post_recommended_channels(self, guild_id: str, request: RecommendChannelRequest) -> Announce:
        """
        创建子频道类型的频道全局公告

        :param guild_id: 频道ID
        :param request: RecommendChannelRequest 对象
        """
        url = get_url(APIConstant.guildAnnounceURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Announce)


class AsyncAPIPermissionAPI(AsyncAPIBase):
    """接口权限接口"""

    async def get_permissions(self, guild_id: str) -> List[APIPermission]:
        """
        获取机器人在频道 guild_id 内可以使用的权限列表

        :param guild_id: 频道ID
        """
        url = get_url(APIConstant.guildAPIPermissionURL, self.is_sandbox).format(guild_id=guild_id)
        response = await self.http_async.get(url)
        apis = json.loads(response, object_hook=APIs)
        return apis.apis

    async def post_permission_demand(self, guild_id: str, request: PermissionDemandToCreate) -> APIPermissionDemand:
        """
        用于创建 API 接口权限授权链接，该链接指向guild_id对应的频道 。
        每天只能在一个频道内发 3 条（默认值）频道权限授权链接，如需调整，请联系平台申请权限。

        :param guild_id: 频道ID
        :param request: PermissionDemandToCreate对象
        """
        url = get_url(APIConstant.guildAPIPermissionDemandURL, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=APIPermissionDemand)


class AsyncScheduleAPI(AsyncAPIBase):
    """日程接口"""

    async def get_schedules(self, channel_id: str, since: str = "") -> List[Schedule]:
        """
        获取某个日程子频道里中当天的日程列表。
        若带了参数 since，则返回结束时间在 since 之后的日程列表；若未带参数 since，则默认返回当天的日程列表。

        :param channel_id: 子频道ID
        :param since: 起始时间戳(ms)
        """
        url = get_url(APIConstant.channelSchedulesURI, self.is_sandbox).format(channel_id=channel_id)
        if since == "":
            request = None
        else:
            request = GetSchedulesRequest(int(since))
        request_json = JsonUtil.obj2json_serialize(request)
        response = await self.http_async.get(url, request_json)
        return json.loads(response, object_hook=Schedule)

    async def get_schedule(self, channel_id: str, schedule_id: str) -> Schedule:
        """
        获取日程子频道的某个日程详情

        :param channel_id: 子频道ID
        :param schedule_id: 日程ID
        """
        url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
            channel_id=channel_id, schedule_id=schedule_id
        )
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=Schedule)

    async def create_schedule(self, channel_id: str, schedule_to_create: ScheduleToCreate) -> Schedule:
        """
        用于在日程子频道创建一个日程。
        要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。
        创建成功后，返回创建成功的日程对象。
        创建操作频次限制
        单个管理员每天限10次
        单个频道每天100次

        :param channel_id: 子频道ID
        :param schedule_to_create: 没有ID的日程对象
        """
        url = get_url(APIConstant.channelSchedulesURI, self.is_sandbox).format(channel_id=channel_id)
        request_json = JsonUtil.obj2json_serialize(schedule_to_create)
        response = await self.http_async.post(url, request_json)
        return json.loads(response, object_hook=Schedule)

    async def update_schedule(self, channel_id: str, schedule_id: str, schedule_to_patch: ScheduleToPatch) -> Schedule:
        """
        要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。
        修改成功后，返回修改后的日程对象。

        :param channel_id: 子频道ID
        :param schedule_id: 日程ID
        :param schedule_to_patch: 修改前的日程对象
        """
        url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
            channel_id=channel_id, schedule_id=schedule_id
        )
        request_json = JsonUtil.obj2json_serialize(schedule_to_patch)
        response = await self.http_async.patch(url, request_json)
        return json.loads(response, object_hook=Schedule)

    async def delete_schedule(self, channel_id: str, schedule_id: str):
        """
        要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。

        :param channel_id: 子频道ID
        :param schedule_id: 日程ID
        """
        url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
            channel_id=channel_id, schedule_id=schedule_id
        )
        response = await self.http_async.delete(url)
        return response == ""


class AsyncReactionAPI(AsyncAPIBase):
    """异步表情表态接口"""

    async def put_reaction(self, channel_id: str, message_id: str, emo_type: int, emo_id: str):
        """
        对一条消息进行表情表态

        :param channel_id: 子频道ID
        :param message_id: 该条消息对应的id
        :param emo_type: 表情类型
        :param emo_id: 表情ID
        """
        url = get_url(APIConstant.reactionURI, self.is_sandbox).format(
            channel_id=channel_id, message_id=message_id, type=emo_type, id=emo_id
        )
        response = await self.http_async.put(url)
        return response == ""

    async def delete_reaction(self, channel_id: str, message_id: str, emo_type: int, emo_id: str):
        """
        删除自己对消息的进行表情表态

        :param channel_id: 子频道ID
        :param message_id: 该条消息对应的id
        :param emo_type: 表情类型
        :param emo_id: 表情ID
        """
        url = get_url(APIConstant.reactionURI, self.is_sandbox).format(
            channel_id=channel_id, message_id=message_id, type=emo_type, id=emo_id
        )
        response = await self.http_async.delete(url)
        return response == ""

    async def get_reaction_users(self, channel_id: str, message_id: str, emo_type: int, emo_id: str, pager: ReactionUsersPager) -> ReactionUsers:
        """
        获取对消息 messageId 指定表情表态的用户列表

        :param channel_id: 子频道ID
        :param message_id: 该条消息对应的id
        :param emo_type: 表情类型
        :param emo_id: 表情ID
        :param pager: 请求用户列表的分页数据对象
        """
        url = get_url(APIConstant.reactionURI, self.is_sandbox).format(
            channel_id=channel_id, message_id=message_id, type=emo_type, id=emo_id
        )
        query = {"cookie": pager.cookie, "limit": pager.limit}
        response = await self.http_async.get(url, params=query)
        return json.loads(response, object_hook=ReactionUsers)


class AsyncPinsAPI(AsyncAPIBase):
    """精华消息API"""

    async def put_pin(self, channel_id: str, message_id: str) -> PinsMessage:
        """
        在子频道内添加一条精华消息，
        每个子频道最多20条精华消息
        只有可见的消息才能被设置为精华消息
        返回对象中 message_ids 为当前请求后子频道内所有精华消息数组

        :param channel_id: 子频道ID
        :param message_id: 该条消息对应的id
        """
        url = get_url(APIConstant.changePinsURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
        try:
            response = await self.http_async.put(url)
            return json.loads(response, object_hook=PinsMessage)
        except (Exception, JSONDecodeError):
            return PinsMessage()

    async def delete_pin(self, channel_id: str, message_id: str):
        """
        用于移除子频道下的一条精华消息

        :param channel_id: 子频道ID
        :param message_id: 该条消息对应的id
        """
        url = get_url(APIConstant.changePinsURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
        response = await self.http_async.delete(url)
        return response == ""

    async def get_pins(self, channel_id: str) -> PinsMessage:
        """
        用于获取子频道内的所有精华消息
        成功后返回 PinsMessage 对象

        :param channel_id: 子频道ID
        """
        url = get_url(APIConstant.getPinsURI, self.is_sandbox).format(channel_id=channel_id)
        response = await self.http_async.get(url)
        return json.loads(response, object_hook=PinsMessage)


class AsyncInteractionAPI(AsyncAPIBase):
    """互动回调API"""

    async def put_interaction(self, interaction_id: str, interaction_data: InteractionData):
        """
        对 interaction_id 进行互动回调数据异步回复更新

        :param interaction_id: 互动事件的ID
        :param interaction_data: 互动事件数据体
        """
        url = get_url(APIConstant.interactionURI, self.is_sandbox).format(interaction_id=interaction_id)
        request_json = JsonUtil.obj2json_serialize(interaction_data)
        response = await self.http_async.put(url, request_json)
        return response == ""
