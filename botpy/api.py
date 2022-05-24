# -*- coding: utf-8 -*-

# 异步api
from typing import Any, List, Dict

from .flags import Permission
from .http import BotHttp, Route
from .types import guild, user, channel, message


def _handle_message_parameters(
    content: str = None,
    embed: message.Embed = None,
    ark: message.Ark = None,
    message_reference: message.Reference = None,
    image: str = None,
    msg_id: str = None,
    event_id: str = None,
    markdown: message.Markdown = None,
) -> Dict:
    payload = {}
    if content is not None:
        payload["content"] = content
    if embed is not None:
        payload["embed"] = embed
    if ark is not None:
        payload["ark"] = ark
    if message_reference is not None:
        payload["message_reference"] = message_reference
    if image is not None:
        payload["image"] = image
    if msg_id is not None:
        payload["msg_id"] = msg_id
    if event_id is not None:
        payload["event_id"] = event_id
    if markdown is not None:
        payload["markdown"] = markdown
    return payload


class BotAPI:
    def __init__(self, http: BotHttp):
        """API初始化信息"""
        self._http = http

    # TODO 重写所有的api及单测

    # 频道相关接口
    async def get_guild(self, guild_id: str) -> guild.Guild:
        """获取频道信息

        :param guild_id: 频道ID（一般从事件中获取相关的ID信息）
        :return: GuildPayload
        """
        route = Route("GET", "/guilds/{guild_id}", guild_id=guild_id)
        return await self._http.request(route)

    # 频道身份组相关接口
    async def get_guild_roles(self, guild_id: str) -> guild.GuildRoles:
        """获取频道身份组列表

        :param guild_id:频道ID
        :return:GuildRolesPayload
        """
        route = Route("GET", "/guilds/{guild_id}/roles", guild_id=guild_id)
        return await self._http.request(route)

    async def create_guild_role(self, guild_id: str, **fields: Any) -> guild.GuildRole:
        """创建频道身份组

        guild_id:str
            频道ID

        fields
            参数字段，可以通过字典设置参数值，如 `create_guild_role(guild_id,name="test")`
            name	string	名称(非必填)
            color	uint32	ARGB 的 HEX 十六进制颜色值转换后的十进制数值(非必填)
            hoist	int32	在成员列表中单独展示: 0-否, 1-是(非必填)
        return::class:GuildRole
        """
        valid_keys = ("name", "color", "hoist")
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        route = Route("POST", "/guilds/{guild_id}/roles", guild_id=guild_id)
        return await self._http.request(route, json=payload)

    async def update_guild_role(self, guild_id: str, role_id: str, **fields: Any) -> guild.GuildRole:
        """修改频道身份组

        guild_id:
            频道ID
        role_id:
            身份组ID
        fields
            参数字段，可以通过字典设置参数值，如 `create_guild_role(guild_id,name="test")`
            name	string	名称(非必填)
            color	uint32	ARGB 的 HEX 十六进制颜色值转换后的十进制数值(非必填)
            hoist	int32	在成员列表中单独展示: 0-否, 1-是(非必填)
        return:class:GuildRole
        """
        valid_keys = ("name", "color", "hoist")
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        route = Route("PATCH", "/guilds/{guild_id}/roles/{role_id}", guild_id=guild_id, role_id=role_id)
        return await self._http.request(route, json=payload)

    async def delete_guild_role(self, guild_id: str, role_id: str) -> str:
        """删除频道身份组

        :param guild_id:
            频道ID
        :param role_id:
            身份组ID
        :return: 删除正常返回空字符串
        """
        route = Route("DELETE", "/guilds/{guild_id}/roles/{role_id}", guild_id=guild_id, role_id=role_id)
        return await self._http.request(route)

    async def create_guild_role_member(
        self,
        guild_id: str,
        role_id: str,
        user_id: str,
        channel_id: str = None,
    ) -> str:
        """增加频道身份组成员

        如果是机器人，要求被添加为管理员。

        :param guild_id:
            频道ID
        :param role_id:
            身份组ID
        :param user_id:
            用户ID
        :param channel_id:
            如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        :return:删除正常返回空字符串
        """
        payload = {}
        if channel_id:
            payload = {"channel": {"id": channel_id}}

        route = Route(
            "PUT",
            "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            guild_id=guild_id,
            user_id=user_id,
            role_id=role_id,
        )
        return await self._http.request(route, json=payload)

    async def delete_guild_role_member(self, guild_id: str, role_id: str, user_id: str, channel_id: str = None) -> str:
        """删除频道身份组成员

        注意：
            如果是机器人，要求被添加为管理员。

        :param guild_id:
            频道ID
        :param role_id:
            身份组ID
        :param user_id:
            用户ID
        :param channel_id:
            如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        :return: 删除正常返回空字符串
        """
        payload = {}
        if channel_id:
            payload = {"channel": {"id": channel_id}}

        route = Route(
            "DELETE",
            "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            guild_id=guild_id,
            user_id=user_id,
            role_id=role_id,
        )
        return await self._http.request(route, json=payload)

    # 成员相关接口，添加成员到用户组等
    async def get_guild_member(self, guild_id: str, user_id: str) -> user.Member:
        """获取频道指定成员

        :param guild_id:
            频道ID
        :param user_id:
            用户ID（一般从事件消息中获取）

        :return:user.Member
        """
        route = Route(
            "GET",
            "/guilds/{guild_id}/members/{user_id}",
            guild_id=guild_id,
            user_id=user_id,
        )
        return await self._http.request(route)

    async def get_guild_members(self, guild_id: str, after: str = "0", limit: int = 1) -> List[user.Member]:
        """获取成员列表

        注意
            该接口为私域机器人权限, 需要在管理端申请权限

        :param guild_id:
            频道ID
        :param after: str
            上一次回包中最后一个member的user id， 如果是第一次请求填 0，默认为 0
        :param limit: int
            分页大小，1-400，默认是 1。成员较多的频道尽量使用较大的limit值，以减少请求数

        :return: List[user.Member]
        """
        params: Dict[str, Any] = {}

        if after is not None:
            params["after"] = after
        if limit is not None:
            params["limit"] = limit

        route = Route(
            "GET",
            "/guilds/{guild_id}/members",
            guild_id=guild_id,
        )
        return await self._http.request(route, params=params)

    # 子频道相关接口
    async def get_channel(self, channel_id: str) -> channel.Channel:
        """获取子频道信息

        :param channel_id:
            子频道ID
        :return:channel.Channel
        """
        route = Route(
            "GET",
            "/channels/{channel_id}",
            channel_id=channel_id,
        )
        return await self._http.request(route)

    async def get_channels(self, guild_id: str) -> List[channel.Channel]:
        """获取频道下的子频道列表

        :param guild_id:
            频道ID

        :return: List[channel.Channel]
        """
        route = Route(
            "GET",
            "/guilds/{guild_id}/channels",
            guild_id=guild_id,
        )
        return await self._http.request(route)

    async def create_channel(
        self, guild_id: str, name: str, type: channel.ChannelType, sub_type: channel.ChannelSubType, **fields
    ) -> channel.Channel:
        """创建子频道

        :param guild_id:
            频道ID
        :param name:
            子频道名
        :param type: channel.ChannelType
            子频道类型
        :param sub_type: channel.ChannelSubType
            子频道子类型
        :param 扩展参数，通过 `kwargs` 传入参数
            position	number	否	排序，非必填
            parent_id	string	否	分组 ID

        :return:Dict: ChannelResponse 对象
        """

        payload = {
            "name": name,
            "type": type.value,
            "subtype": sub_type.value,
        }
        valid_keys = ("position", "parent_id")
        payload.update({k: v for k, v in fields.items() if k in valid_keys and v is not None})
        route = Route("POST", "/guilds/{guild_id}/channels", guild_id=guild_id)
        return await self._http.request(route, json=payload)

    async def update_channel(self, channel_id: str, **fields) -> channel.Channel:
        """修改子频道

        :param channel_id:
            频道ID
        :**fields: 修改指定参数，通过`**kwargs` 传入:
            name	            string	子频道名
            position	        int	    排序
            parent_id	        string	分组 id
            private_type	    int	    子频道私密类型 PrivateType
            speak_permission	int	    子频道发言权限 SpeakPermission

        :return:Dict: channel.Channel
        """

        valid_keys = ("name", "position", "parent_id", "private_type", "speak_permission")
        payload = {k: v for k, v in fields.items() if k in valid_keys and v is not None}
        route = Route("PATCH", "/channels/{channel_id}", channel_id=channel_id)
        return await self._http.request(route, json=payload)

    async def delete_channel(self, channel_id: str) -> channel.Channel:
        """删除子频道

        :param channel_id:
            频道ID

        :return: Dict: 删除后的channel.Channel
        """
        route = Route("DELETE", "/channels/{channel_id}", channel_id=channel_id)
        return await self._http.request(route)

    # 子频道权限相关接口
    async def get_channel_user_permissions(self, channel_id: str, user_id: str) -> channel.ChannelPermissions:
        """获取指定子频道用户的权限

        :param channel_id:
            子频道ID
        :param user_id:
            用户ID

        :return:Dict:channel.ChannelPermissions
        """
        route = Route(
            "GET", "/channels/{channel_id}/members/{user_id}/permissions", channel_id=channel_id, user_id=user_id
        )
        return await self._http.request(route)

    async def update_channel_user_permissions(
        self, channel_id: str, user_id: str, add: Permission = None, remove: Permission = None
    ) -> str:
        """修改指定子频道用户的权限

        注意
            如果是公共频道不能进行添加和移除查看或发言权限

        :param channel_id:
            子频道ID
        :param user_id:
            用户ID
        :param add:Permission
            添加的权限类型，示例：
            add = Permission(view_permission=True)
        :param remove:Permission
            删除的权限类型，示例：
            remove = Permission(view_permission=True,manager_permission=True)

        :return: 成功返回空字符串
        """
        payload = {}
        if add is not None:
            payload.update({"add": str(add.value)})
        if remove is not None:
            payload.update({"remove": str(remove.value)})

        route = Route(
            "PUT", "/channels/{channel_id}/members/{user_id}/permissions", channel_id=channel_id, user_id=user_id
        )
        return await self._http.request(route, json=payload)

    async def get_channel_role_permissions(self, channel_id: str, role_id: str) -> channel.ChannelPermissions:
        """获取指定子频道身份组的权限

        :param channel_id:
            子频道ID
        :param role_id:
            身份组ID

        :return:Dict:channel.ChannelPermissions
        """
        route = Route(
            "GET", "/channels/{channel_id}/roles/{role_id}/permissions", channel_id=channel_id, role_id=role_id
        )
        return await self._http.request(route)

    async def update_channel_role_permissions(
        self, channel_id: str, role_id: str, add: Permission = None, remove: Permission = None
    ) -> str:
        """修改指定子频道身份组的权限

        :param channel_id:
            子频道ID
        :param role_id:
            身份组ID
        :param add:Permission
            添加的权限类型，示例：添加可读权限
            add = Permission(view_permission=True)
        :param remove:Permission
            删除的权限类型，示例：删除可读和发言权限
            remove = Permission(view_permission=True,speak_permission=True)

        :return: 成功返回空字符串
        """
        payload = {}
        if add is not None:
            payload.update({"add": str(add.value)})
        if remove is not None:
            payload.update({"remove": str(remove.value)})

        route = Route(
            "PUT", "/channels/{channel_id}/roles/{role_id}/permissions", channel_id=channel_id, role_id=role_id
        )
        return await self._http.request(route, json=payload)

    # 消息
    # async def get_message(self, channel_id: str, message_id: str) -> MessageGet:
    #     """
    #     获取指定消息
    #
    #     :param channel_id: 频道ID
    #     :param message_id: 消息ID
    #     :return: Message 对象
    #     """
    #     url = get_url(APIConstant.messageURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
    #     response = await self._http.get(url)
    #     return json.loads(response, object_hook=MessageGet)
    #
    # async def get_messages(self, channel_id: str, pager: MessagesPager) -> List[Message]:
    #     """
    #     获取指定消息列表
    #
    #     :param channel_id: 频道ID
    #     :param pager: MessagesPager对象
    #     :return: Message 对象
    #     """
    #     url = get_url(APIConstant.messagesURI, self.is_sandbox).format(channel_id=channel_id)
    #     query = {}
    #     if pager.limit != "":
    #         query["limit"] = pager.limit
    #
    #     if pager.type != "" and pager.id != "":
    #         query[pager.type] = pager.id
    #
    #     response = await self._http.get(url, params=query)
    #     return json.loads(response, object_hook=Message)

    async def post_message(
        self,
        channel_id: str,
        content: str = None,
        embed: message.Embed = None,
        ark: message.Ark = None,
        message_reference: message.Reference = None,
        image: str = None,
        msg_id: str = None,
        event_id: str = None,
        markdown: message.Markdown = None,
    ) -> message.Message:
        """发送消息

        注意
            - 要求操作人在该子频道具有发送消息的权限。
            - 发送成功之后，会触发一个创建消息的事件。
            - 被动回复消息有效期为 5 分钟
            - 主动推送消息每日每个子频道限 2 条
            - 发送消息接口要求机器人接口需要链接到websocket gateway 上保持在线状态

        :param channel_id:
            子频道ID
        :param content:
            消息内容，文本内容，支持内嵌格式
        :param msg_id:
            要回复的消息id(Message.id), 在 AT_CREATE_MESSAGE 事件中获取。带了 msg_id 视为被动回复消息，否则视为主动推送消息
        :param embed:
            embed 消息，一种特殊的 ark
        :param ark:
            ark 消息
        :param image:
            图片url地址
        :param message_reference:
            引用消息

        :return: Message
        """
        params = _handle_message_parameters(content, embed, ark, message_reference, image, msg_id, event_id, markdown)
        route = Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id)
        return await self._http.request(route, json=params)

    # async def recall_message(self, channel_id: str, message_id: str, hide_tip: bool = False):
    #     """
    #     撤回消息
    #
    #     管理员可以撤回普通成员的消息
    #     频道主可以撤回所有人的消息
    #
    #     :param channel_id: 子频道ID
    #     :param message_id: 消息ID
    #     :param hide_tip: 是否隐藏撤回提示小灰条
    #     """
    #     url = get_url(APIConstant.messageURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
    #     response = await self._http.delete(url, params={"hidetip": str(hide_tip)})
    #     return response == ""
    #
    # """私信消息"""
    #
    # async def create_direct_message(self, create_direct_message: CreateDirectMessageRequest) -> DirectMessageGuild:
    #     """
    #     创建私信频道
    #
    #     :param create_direct_message: 构造request数据
    #     :return: 私信频道对象
    #     """
    #     url = get_url(APIConstant.userMeDMURI, self.is_sandbox)
    #     request_json = JsonUtil.obj2json_serialize(create_direct_message)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=DirectMessageGuild)
    #
    # async def post_direct_message(self, guild_id: str, message_send: MessageSendRequest) -> Message:
    #     """
    #     发送私信
    #
    #     :param guild_id: 创建的私信频道id
    #     :param message_send: 发送消息的数据请求对象 MessageSendRequest
    #     :return Message对象
    #     """
    #     url = get_url(APIConstant.dmsURI, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(message_send)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=Message)
    #
    # """音频接口"""
    #
    # async def post_audio(self, channel_id: str, audio_control: AudioControl) -> bool:
    #     """
    #     音频控制
    #
    #     :param channel_id:频道ID
    #     :param audio_control:AudioControl对象
    #     :return:是否成功
    #     """
    #     url = get_url(APIConstant.audioControlURI, self.is_sandbox).format(channel_id=channel_id)
    #     request_json = JsonUtil.obj2json_serialize(audio_control)
    #     response = await self._http.post(url, request=request_json)
    #     return response == ""
    #
    # """用户相关接口"""
    #
    # async def me(self) -> User:
    #     """
    #     :return:使用当前用户信息填充的 User 对象
    #     """
    #     url = get_url(APIConstant.userMeURI, self.is_sandbox)
    #     response = await self._http.get(url)
    #     return json.loads(response, object_hook=User)
    #
    # async def me_guilds(self, option: ReqOption = None) -> List[Guild]:
    #     """
    #     当前用户所加入的 Guild 对象列表
    #
    #     :param option: ReqOption对象
    #     :return:Guild对象列表
    #     """
    #     url = get_url(APIConstant.userMeGuildsURI, self.is_sandbox)
    #     if option is None:
    #         query = {}
    #     else:
    #         query = option.__dict__
    #
    #     response = await self._http.get(url, params=query)
    #     return json.loads(response, object_hook=Guild)
    #
    # WebsocketAPI
    async def ws(self):
        return await self._http.request(Route("GET", "/gateway/bot"))

    #
    # """禁言接口"""
    #
    # async def mute_all(self, guild_id: str, options: MuteOption):
    #     """
    #     禁言全员
    #
    #     :param guild_id: 频道ID
    #     :param options: MuteOptions对象
    #     """
    #     url = get_url(APIConstant.guildMuteURI, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(options)
    #     response = await self._http.patch(url, request=request_json)
    #     return response == ""
    #
    # async def mute_member(self, guild_id: str, user_id: str, options: MuteOption):
    #     """
    #     禁言指定成员
    #
    #     :param guild_id: 频道ID
    #     :param user_id: 用户ID
    #     :param options: MuteOptions对象
    #     """
    #     url = get_url(APIConstant.guildMemberMuteURI, self.is_sandbox).format(guild_id=guild_id, user_id=user_id)
    #     request_json = JsonUtil.obj2json_serialize(options)
    #     response = await self._http.patch(url, request=request_json)
    #     return response == ""
    #
    # async def mute_multi_member(self, guild_id: str, options: MultiMuteOption):
    #     """
    #     禁言指定用户
    #
    #     :param guild_id: 频道ID
    #     :param options: MultiMuteOption对象
    #     """
    #     url = get_url(APIConstant.guildMuteURI, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(options)
    #     response = await self._http.patch(url, request=request_json)
    #     user_ids = json.loads(response, object_hook=UserIds)
    #     return user_ids.user_ids
    #
    # """公告接口"""
    #
    # async def create_announce(self, guild_id: str, request: CreateAnnounceRequest) -> Announce:
    #     """
    #     创建频道全局公告
    #
    #     :param guild_id: 频道ID
    #     :param request: CreateAnnounceRequest对象
    #     """
    #     url = get_url(APIConstant.guildAnnounceURI, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(request)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=Announce)
    #
    # async def delete_announce(self, guild_id: str, message_id: str):
    #     """
    #     删除频道全局公告
    #     message_id 有值时，会校验 message_id 合法性，若不校验校验 message_id，请将 message_id 设置为 all
    #
    #     :param guild_id: 频道ID
    #     :param message_id: 消息ID
    #     """
    #     url = get_url(APIConstant.deleteGuildAnnounceURI, self.is_sandbox).format(
    #         guild_id=guild_id, message_id=message_id
    #     )
    #     response = await self._http.delete(url)
    #     return response == ""
    #
    # async def create_channel_announce(self, channel_id: str, request: CreateChannelAnnounceRequest) -> Announce:
    #     """
    #     设置消息为指定子频道公告
    #
    #     :param channel_id: 频道ID
    #     :param request: CreateChannelAnnounceRequest对象
    #     """
    #     url = get_url(APIConstant.channelAnnounceURI, self.is_sandbox).format(channel_id=channel_id)
    #     request_json = JsonUtil.obj2json_serialize(request)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=Announce)
    #
    # async def delete_channel_announce(self, channel_id: str, message_id: str):
    #     """
    #     删除子频道公告
    #     message_id 有值时，会校验 message_id 合法性，若不校验校验 message_id，请将 message_id 设置为 all
    #
    #     :param channel_id: 频道ID
    #     :param message_id: 消息ID
    #     """
    #     url = get_url(APIConstant.deleteChannelAnnounceURI, self.is_sandbox).format(
    #         channel_id=channel_id, message_id=message_id
    #     )
    #     response = await self._http.delete(url)
    #     return response == ""
    #
    # async def post_recommended_channels(self, guild_id: str, request: RecommendChannelRequest) -> Announce:
    #     """
    #     创建子频道类型的频道全局公告
    #
    #     :param guild_id: 频道ID
    #     :param request: RecommendChannelRequest 对象
    #     """
    #     url = get_url(APIConstant.guildAnnounceURI, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(request)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=Announce)
    #
    # """接口权限接口"""
    #
    # async def get_permissions(self, guild_id: str) -> List[APIPermission]:
    #     """
    #     获取机器人在频道 guild_id 内可以使用的权限列表
    #
    #     :param guild_id: 频道ID
    #     """
    #     url = get_url(APIConstant.guildAPIPermissionURL, self.is_sandbox).format(guild_id=guild_id)
    #     response = await self._http.get(url)
    #     apis = json.loads(response, object_hook=APIs)
    #     return apis.apis
    #
    # async def post_permission_demand(self, guild_id: str, request: PermissionDemandToCreate) -> APIPermissionDemand:
    #     """
    #     用于创建 API 接口权限授权链接，该链接指向guild_id对应的频道 。
    #     每天只能在一个频道内发 3 条（默认值）频道权限授权链接，如需调整，请联系平台申请权限。
    #
    #     :param guild_id: 频道ID
    #     :param request: PermissionDemandToCreate对象
    #     """
    #     url = get_url(APIConstant.guildAPIPermissionDemandURL, self.is_sandbox).format(guild_id=guild_id)
    #     request_json = JsonUtil.obj2json_serialize(request)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=APIPermissionDemand)
    #
    # """日程接口"""
    #
    # async def get_schedules(self, channel_id: str, since: str = "") -> List[Schedule]:
    #     """
    #     获取某个日程子频道里中当天的日程列表。
    #     若带了参数 since，则返回结束时间在 since 之后的日程列表；若未带参数 since，则默认返回当天的日程列表。
    #
    #     :param channel_id: 子频道ID
    #     :param since: 起始时间戳(ms)
    #     """
    #     url = get_url(APIConstant.channelSchedulesURI, self.is_sandbox).format(channel_id=channel_id)
    #     if since == "":
    #         request = None
    #     else:
    #         request = GetSchedulesRequest(int(since))
    #     request_json = JsonUtil.obj2json_serialize(request)
    #     response = await self._http.get(url, request_json)
    #     return json.loads(response, object_hook=Schedule)
    #
    # async def get_schedule(self, channel_id: str, schedule_id: str) -> Schedule:
    #     """
    #     获取日程子频道的某个日程详情
    #
    #     :param channel_id: 子频道ID
    #     :param schedule_id: 日程ID
    #     """
    #     url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
    #         channel_id=channel_id, schedule_id=schedule_id
    #     )
    #     response = await self._http.get(url)
    #     return json.loads(response, object_hook=Schedule)
    #
    # async def create_schedule(self, channel_id: str, schedule_to_create: ScheduleToCreate) -> Schedule:
    #     """
    #     用于在日程子频道创建一个日程。
    #     要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。
    #     创建成功后，返回创建成功的日程对象。
    #     创建操作频次限制
    #     单个管理员每天限10次
    #     单个频道每天100次
    #
    #     :param channel_id: 子频道ID
    #     :param schedule_to_create: 没有ID的日程对象
    #     """
    #     url = get_url(APIConstant.channelSchedulesURI, self.is_sandbox).format(channel_id=channel_id)
    #     request_json = JsonUtil.obj2json_serialize(schedule_to_create)
    #     response = await self._http.post(url, request_json)
    #     return json.loads(response, object_hook=Schedule)
    #
    # async def update_schedule(self, channel_id: str, schedule_id: str, schedule_to_patch: ScheduleToPatch)
    # -> Schedule:
    #     """
    #     要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。
    #     修改成功后，返回修改后的日程对象。
    #
    #     :param channel_id: 子频道ID
    #     :param schedule_id: 日程ID
    #     :param schedule_to_patch: 修改前的日程对象
    #     """
    #     url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
    #         channel_id=channel_id, schedule_id=schedule_id
    #     )
    #     request_json = JsonUtil.obj2json_serialize(schedule_to_patch)
    #     response = await self._http.patch(url, request_json)
    #     return json.loads(response, object_hook=Schedule)
    #
    # async def delete_schedule(self, channel_id: str, schedule_id: str):
    #     """
    #     要求操作人具有管理频道的权限，如果是机器人，则需要将机器人设置为管理员。
    #
    #     :param channel_id: 子频道ID
    #     :param schedule_id: 日程ID
    #     """
    #     url = get_url(APIConstant.channelSchedulesIdURI, self.is_sandbox).format(
    #         channel_id=channel_id, schedule_id=schedule_id
    #     )
    #     response = await self._http.delete(url)
    #     return response == ""
    #
    # """异步表情表态接口"""
    #
    # async def put_reaction(self, channel_id: str, message_id: str, emo_type: int, emo_id: str):
    #     """
    #     对一条消息进行表情表态
    #
    #     :param channel_id: 子频道ID
    #     :param message_id: 该条消息对应的id
    #     :param emo_type: 表情类型
    #     :param emo_id: 表情ID
    #     """
    #     url = get_url(APIConstant.reactionURI, self.is_sandbox).format(
    #         channel_id=channel_id, message_id=message_id, type=emo_type, id=emo_id
    #     )
    #     response = await self._http.put(url)
    #     return response == ""
    #
    # async def delete_reaction(self, channel_id: str, message_id: str, emo_type: int, emo_id: str):
    #     """
    #     删除自己对消息的进行表情表态
    #
    #     :param channel_id: 子频道ID
    #     :param message_id: 该条消息对应的id
    #     :param emo_type: 表情类型
    #     :param emo_id: 表情ID
    #     """
    #     url = get_url(APIConstant.reactionURI, self.is_sandbox).format(
    #         channel_id=channel_id, message_id=message_id, type=emo_type, id=emo_id
    #     )
    #     response = await self._http.delete(url)
    #     return response == ""
    #
    # """精华消息API"""
    #
    # async def put_pin(self, channel_id: str, message_id: str) -> PinsMessage:
    #     """
    #     在子频道内添加一条精华消息，
    #     每个子频道最多20条精华消息
    #     只有可见的消息才能被设置为精华消息
    #     返回对象中 message_ids 为当前请求后子频道内所有精华消息数组
    #
    #     :param channel_id: 子频道ID
    #     :param message_id: 该条消息对应的id
    #     """
    #     url = get_url(APIConstant.changePinsURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
    #     try:
    #         response = await self._http.put(url)
    #         return json.loads(response, object_hook=PinsMessage)
    #     except (Exception, JSONDecodeError):
    #         return PinsMessage()
    #
    # async def delete_pin(self, channel_id: str, message_id: str):
    #     """
    #     用于移除子频道下的一条精华消息
    #
    #     :param channel_id: 子频道ID
    #     :param message_id: 该条消息对应的id
    #     """
    #     url = get_url(APIConstant.changePinsURI, self.is_sandbox).format(channel_id=channel_id, message_id=message_id)
    #     response = await self._http.delete(url)
    #     return response == ""
    #
    # async def get_pins(self, channel_id: str) -> PinsMessage:
    #     """
    #     用于获取子频道内的所有精华消息
    #     成功后返回 PinsMessage 对象
    #
    #     :param channel_id: 子频道ID
    #     """
    #     url = get_url(APIConstant.getPinsURI, self.is_sandbox).format(channel_id=channel_id)
    #     response = await self._http.get(url)
    #     return json.loads(response, object_hook=PinsMessage)
    #
    # """互动回调API"""
    #
    # async def put_interaction(self, interaction_id: str, interaction_data: InteractionData):
    #     """
    #     对 interaction_id 进行互动回调数据异步回复更新
    #
    #     :param interaction_id: 互动事件的ID
    #     :param interaction_data: 互动事件数据体
    #     """
    #     url = get_url(APIConstant.interactionURI, self.is_sandbox).format(interaction_id=interaction_id)
    #     request_json = JsonUtil.obj2json_serialize(interaction_data)
    #     response = await self._http.put(url, request_json)
    #     return response == ""
