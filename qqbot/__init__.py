# -*- coding: utf-8 -*-
import json
from enum import Enum
from typing import List

from qqbot.core.network.http import Http, HttpStatus
from qqbot.core.network.url import get_url, APIConstant
from qqbot.core.network.websocket.ws_intents_handler import register_handlers, Handler
from qqbot.core.network.websocket.ws_session_manager import SessionManager
from qqbot.core.util import logging
from qqbot.core.util.json_util import JsonUtil
from qqbot.model.audio import AudioControl
from qqbot.model.channel import (
    Channel,
    ChannelResponse,
    CreateChannelRequest,
    PatchChannelRequest,
)
from qqbot.model.channel_permissions import (
    ChannelPermissions,
    ChannelPermissionsUpdateRequest,
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
from qqbot.model.member import User, Member
from qqbot.model.message import (
    MessageSendRequest,
    Message,
    CreateDirectMessageRequest,
    DirectMessageGuild,
    MessagesPager,
)
from qqbot.model.token import Token

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


def listen_events(t_token: Token, is_sandbox: bool, *handlers: Handler):
    """
    注册并监听频道相关事件

    :param t_token: Token对象
    :param handlers: 包含事件类型和事件回调的Handler对象，支持多个对象
    :param is_sandbox:是否沙盒环境，默认为False
    """
    # 通过api获取websocket链接
    ws_api = WebsocketAPI(t_token, is_sandbox)
    ws_ap = ws_api.ws()
    # 新建和注册监听事件
    t_intent = register_handlers(handlers)
    # 实例一个session_manager
    manager = SessionManager()
    manager.start(ws_ap, t_token.bot_token(), t_intent)


class APIBase:
    timeout = 3

    def __init__(self, token: Token, is_sandbox: bool):
        """
        API初始化信息

        :param token: Token对象
        :param is_sandbox: 是否沙盒环境
        """
        self.is_sandbox = is_sandbox
        self.token = token
        self.http = Http(self.timeout, token.get_string(), token.get_type())

    def with_timeout(self, timeout):
        self.timeout = timeout
        return self


class GuildAPI(APIBase):
    """
    频道相关接口
    """

    def get_guild(self, guild_id: str) -> Guild:
        """
        获取频道信息

        :param guild_id: 频道ID（一般从事件中获取相关的ID信息）
        :return: 频道Guild对象
        """
        url = get_url(APIConstant.guildURI, self.is_sandbox).format(guild_id=guild_id)
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Guild)


class GuildRoleAPI(APIBase):
    """
    频道身份组相关接口
    """

    def get_guild_roles(self, guild_id: str) -> GuildRoles:
        """
        获取频道身份组列表

        :param guild_id:频道ID
        :return:GuildRoles对象
        """
        url = get_url(APIConstant.rolesURI, self.is_sandbox).format(guild_id=guild_id)
        response = self.http.get(url)
        return json.loads(response.content, object_hook=GuildRoles)

    def create_guild_role(
        self, guild_id: str, role_info: RoleUpdateInfo
    ) -> RoleUpdateResult:
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
        response = self.http.post(url, request=serialize)
        return json.loads(response.content, object_hook=RoleUpdateResult)

    def update_guild_role(
        self, guild_id: str, role_id: str, role_info: RoleUpdateInfo
    ) -> RoleUpdateResult:
        """
        修改频道身份组

        :param guild_id:频道ID
        :param role_id:身份组ID
        :param role_info:更新后的RoleUpdateInfo对象
        :return:RoleUpdateResult对象
        """
        url = get_url(APIConstant.roleURI, self.is_sandbox).format(
            guild_id=guild_id, role_id=role_id
        )
        params = RoleUpdateRequest()
        params.filter = RoleUpdateFilter(1, 1, 1)
        params.guild_id = guild_id
        params.info = role_info
        serialize = JsonUtil.obj2json_serialize(params)
        response = self.http.patch(url, request=serialize)
        return json.loads(response.content, object_hook=RoleUpdateResult)

    def delete_guild_role(self, guild_id: str, role_id: str) -> bool:
        """
        删除频道身份组

        :param guild_id: 频道ID
        :param role_id: 身份组ID
        :return: 是否删除成功
        """
        url = get_url(APIConstant.roleURI, self.is_sandbox).format(
            guild_id=guild_id, role_id=role_id
        )
        response = self.http.delete(url)
        return response.status_code == HttpStatus.ACTION_OK

    def create_guild_role_member(
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
        response = self.http.put(url, request=JsonUtil.obj2json_serialize(role_req))
        return response.status_code == HttpStatus.ACTION_OK

    def delete_guild_role_member(
        self,
        guild_id: str,
        role_id: str,
        user_id: str,
        role_req: Channel = None,
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
        response = self.http.delete(url, request=JsonUtil.obj2json_serialize(role_req))
        return response.status_code == HttpStatus.ACTION_OK


class GuildMemberAPI(APIBase):
    """
    成员相关接口，添加成员到用户组等
    """

    def get_guild_member(self, guild_id: str, user_id: str) -> Member:
        """
        获取频道指定成员

        :param guild_id:频道ID
        :param user_id:用户ID（一般从事件消息中获取）
        :return:
        """
        url = get_url(APIConstant.guildMemberURI, self.is_sandbox).format(
            guild_id=guild_id, user_id=user_id
        )
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Member)

    def get_guild_members(
        self, guild_id: str, guild_member_pager: QueryParams
    ) -> List[Member]:
        """
        获取成员列表，需要申请接口权限

        :param guild_id: 频道ID
        :param guild_member_pager: GuildMembersPager分页数据对象
        :return: Member列表
        """
        url = get_url(APIConstant.guildMembersURI, self.is_sandbox).format(
            guild_id=guild_id
        )
        response = self.http.get(url, params=guild_member_pager.__dict__)
        return json.loads(response.content, object_hook=Member)


class ChannelAPI(APIBase):
    """子频道相关接口"""

    def get_channel(self, channel_id) -> Channel:
        """
        获取子频道信息

        :param channel_id:子频道ID
        :return:子频道对象Channel
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Channel)

    def get_channels(self, guild_id: str) -> List[Channel]:
        """
        获取频道下的子频道列表

        :param guild_id: 频道ID
        :return: Channel列表
        """
        url = get_url(APIConstant.channelsURI, self.is_sandbox).format(
            guild_id=guild_id
        )
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Channel)

    def create_channel(
        self, guild_id: str, request: CreateChannelRequest
    ) -> ChannelResponse:
        """
        创建子频道

        :param guild_id: 频道ID
        :param request: 创建子频道的请求对象CreateChannelRequest
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelsURI, self.is_sandbox).format(
            guild_id=guild_id
        )
        request_json = JsonUtil.obj2json_serialize(request)
        response = self.http.post(url, request_json)
        return json.loads(response.content, object_hook=ChannelResponse)

    def update_channel(
        self, channel_id: str, request: PatchChannelRequest
    ) -> ChannelResponse:
        """
        修改子频道

        :param channel_id: 频道ID
        :param request: PatchChannelRequest
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        request_json = JsonUtil.obj2json_serialize(request)
        response = self.http.patch(url, request_json)
        return json.loads(response.content, object_hook=ChannelResponse)

    def delete_channel(self, channel_id: str) -> ChannelResponse:
        """
        删除子频道

        :param channel_id: 频道ID
        :return ChannelResponse 对象
        """
        url = get_url(APIConstant.channelURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        response = self.http.delete(url)
        return json.loads(response.content, object_hook=ChannelResponse)


class ChannelPermissionsAPI(APIBase):
    """子频道权限相关接口"""

    def get_channel_permissions(
        self, channel_id: str, user_id: str
    ) -> ChannelPermissions:
        """
        获取指定子频道的权限

        :param channel_id:子频道ID
        :param user_id:用户ID
        :return:ChannelPermissions对象
        """
        url = get_url(APIConstant.channelPermissionsURI, self.is_sandbox).format(
            channel_id=channel_id, user_id=user_id
        )
        response = self.http.get(url)
        return json.loads(response.content, object_hook=ChannelPermissions)

    def update_channel_permissions(
        self, channel_id, user_id, request: ChannelPermissionsUpdateRequest
    ) -> bool:
        """
        修改指定子频道的权限

        :param channel_id:子频道ID
        :param user_id:用户ID
        :param request:ChannelPermissionsUpdateRequest数据对象（构造可以查看具体的对象注释）
        :return:
        """
        url = get_url(APIConstant.channelPermissionsURI, self.is_sandbox).format(
            channel_id=channel_id, user_id=user_id
        )
        if request.add != "":
            request.add = str(int(request.add, 16))
        if request.remove != "":
            request.remove = str(int(request.remove, 16))
        response = self.http.put(url, request=JsonUtil.obj2json_serialize(request))
        return response.status_code == HttpStatus.ACTION_OK


class MessageAPI(APIBase):
    """消息"""

    def get_message(self, channel_id: str, message_id: str) -> Message:
        """
        获取指定消息

        :param channel_id: 频道ID
        :param message_id: 消息ID
        :return: Message 对象
        """
        url = get_url(APIConstant.messageURI, self.is_sandbox).format(
            channel_id=channel_id, message_id=message_id
        )
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Message)

    def get_messages(self, channel_id: str, pager: MessagesPager) -> List[Message]:
        """
        获取指定消息列表

        :param channel_id: 频道ID
        :param pager: MessagesPager对象
        :return: Message 对象
        """
        url = get_url(APIConstant.messagesURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        query = {}
        if pager.limit != "":
            query["limit"] = pager.limit

        if pager.type != "" and pager.id != "":
            query[pager.type] = pager.id

        response = self.http.get(url, params=query)
        return json.loads(response.content, object_hook=Message)

    def post_message(
        self, channel_id: str, message_send: MessageSendRequest
    ) -> Message:
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

        url = get_url(APIConstant.messagesURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        request_json = JsonUtil.obj2json_serialize(message_send)
        response = self.http.post(url, request_json)
        return json.loads(response.content, object_hook=Message)

    def create_direct_message(
        self, create_direct_message: CreateDirectMessageRequest
    ) -> DirectMessageGuild:
        """
        创建私信频道

        :param create_direct_message: 构造request数据
        :return: 私信频道对象
        """
        url = get_url(APIConstant.userMeDMURI, self.is_sandbox)
        request_json = JsonUtil.obj2json_serialize(create_direct_message)
        response = self.http.post(url, request_json)
        return json.loads(response.content, object_hook=DirectMessageGuild)

    def post_direct_message(
        self, guild_id: str, message_send: MessageSendRequest
    ) -> Message:
        """
        发送私信

        :param guild_id: 创建的私信频道id
        :param message_send: 发送消息的数据请求对象 MessageSendRequest
        :return Message对象
        """
        url = get_url(APIConstant.dmsURI, self.is_sandbox).format(guild_id=guild_id)
        request_json = JsonUtil.obj2json_serialize(message_send)
        response = self.http.post(url, request_json)
        return json.loads(response.content, object_hook=Message)


class AudioAPI(APIBase):
    """音频接口"""

    def post_audio(self, channel_id: str, audio_control: AudioControl) -> bool:
        """
        音频控制

        :param channel_id:频道ID
        :param audio_control:AudioControl对象
        :return:是否成功
        """
        url = get_url(APIConstant.audioControlURI, self.is_sandbox).format(
            channel_id=channel_id
        )
        request_json = JsonUtil.obj2json_serialize(audio_control)
        response = self.http.post(url, request=request_json)
        return response.status_code == HttpStatus.ACTION_OK


class UserAPI(APIBase):
    """用户相关接口"""

    def me(self) -> User:
        """
        :return:使用当前用户信息填充的 User 对象
        """
        url = get_url(APIConstant.userMeURI, self.is_sandbox)
        response = self.http.get(url)
        return json.loads(response.content, object_hook=User)

    def me_guilds(self) -> List[Guild]:
        """
        当前用户所加入的 Guild 对象列表

        :return:Guild对象列表
        """
        url = get_url(APIConstant.userMeGuildsURI, self.is_sandbox)
        response = self.http.get(url)
        return json.loads(response.content, object_hook=Guild)


class WebsocketAPI(APIBase):
    """WebsocketAPI"""

    def ws(self):
        url = get_url(APIConstant.gatewayBotURI, self.is_sandbox)
        response = self.http.get(url)
        websocket_ap = json.loads(response.content)
        return websocket_ap
