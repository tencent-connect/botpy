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
    params = locals()
    payload.update({k: v for k, v in params.items() if v})
    return payload


class BotAPI:
    """
    机器人相关的API接口类

    使用注意:
        - 如果要直接使用api，可以通过client的内部成员变量，通过`self.api.xx`来使用
        - 设置超时时间: Client(timeout=5)
        - API当前返回的所有自定义类型数据为字典数据，通过TypedDict进行类型提示
    """

    def __init__(self, http: BotHttp):
        """
        Args:
          http (BotHttp): 用于发送请求的 http 客户端。
        """
        self._http = http

    # TODO 重写所有的api及单测 @veehou

    # 频道相关接口
    async def get_guild(self, guild_id: str) -> guild.Guild:
        """
        获取频道信息。

        Args:
          guild_id (str): 频道ID（一般从事件中获取相关的ID信息）

        Returns:
          GuildPayload (字典数据)
        """
        route = Route("GET", "/guilds/{guild_id}", guild_id=guild_id)
        return await self._http.request(route)

    # 频道身份组相关接口
    async def get_guild_roles(self, guild_id: str) -> guild.GuildRoles:
        """
        获取频道身份组列表

        Args:
          guild_id (str): 频道ID。

        Returns:
          GuildRolesPayload
        """
        route = Route("GET", "/guilds/{guild_id}/roles", guild_id=guild_id)
        return await self._http.request(route)

    async def create_guild_role(self, guild_id: str, **fields: Any) -> guild.GuildRole:
        """
        创建频道身份组

        Args:
          guild_id (str): 在其中创建角色的频道ID。

        Kwargs（fields）:
          name (str): 名称(非必填)
          color (int): ARGB 的 HEX 十六进制颜色值转换后的十进制数值(非必填)
          hoist (int): 在成员列表中单独展示: 0-否, 1-是(非必填)

        Returns:
          class:GuildRole
        """
        valid_keys = ("name", "color", "hoist")
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        route = Route("POST", "/guilds/{guild_id}/roles", guild_id=guild_id)
        return await self._http.request(route, json=payload)

    async def update_guild_role(self, guild_id: str, role_id: str, **fields: Any) -> guild.GuildRole:
        """
        修改频道身份组

        Args:
          guild_id (str): 在其中创建角色的公会 ID。
          role_id (str): 您要修改的角色的 ID。

        Kwargs（fields）:
          name (str): 名称(非必填)
          color (int): ARGB 的 HEX 十六进制颜色值转换后的十进制数值(非必填)
          hoist (int): 在成员列表中单独展示: 0-否, 1-是(非必填)

        Returns:
          class:GuildRole
        """
        valid_keys = ("name", "color", "hoist")
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        route = Route("PATCH", "/guilds/{guild_id}/roles/{role_id}", guild_id=guild_id, role_id=role_id)
        return await self._http.request(route, json=payload)

    async def delete_guild_role(self, guild_id: str, role_id: str) -> str:
        """
        删除频道身份组

        Args:
          guild_id (str): 频道 ID。
          role_id (str): 身份组 ID。

        Returns:
          返回值是一个字符串。
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
        """
        增加频道身份组成员。

        Args:
          guild_id (str): 频道 ID。
          role_id (str): 身份组 ID。
          user_id (str): 要添加到角色的用户的用户 ID。
          channel_id (str): 您要在其中创建角色的频道的 ID。如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        Returns:
          返回值是一个字符串。
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
        """
        删除频道身份组成员。

        Args:
          guild_id (str): 频道 ID。
          role_id (str): 身份组 ID。
          user_id (str): 用户的标识。
          channel_id (str): 您要从中删除角色的子频道的 ID。
            如果要删除的身份组ID是5-子频道管理员，需要增加channel对象来指定具体是哪个子频道

        Returns:
          返回值是一个字符串。
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
        """
        获取频道指定成员。

        Args:
          guild_id (str): 频道 ID。
          user_id (str): 用户 ID（一般从事件消息中获取。

        Returns:
          user.Member
        """
        route = Route(
            "GET",
            "/guilds/{guild_id}/members/{user_id}",
            guild_id=guild_id,
            user_id=user_id,
        )
        return await self._http.request(route)

    async def get_guild_members(self, guild_id: str, after: str = "0", limit: int = 1) -> List[user.Member]:
        """
        获取成员列表。

        注意:该接口为私域机器人权限, 需要在管理端申请权限

        Args:
          guild_id (str): 频道 ID。
          after (str): 上一批用户中最后一个用户的ID。如果这是第一个请求，请使用 0。. Defaults to 0
          limit (int): 分页大小，1-400。成员较多的频道尽量使用较大的limit值，以减少请求数。. Defaults to 1

        Returns:
          user.Member 对象的列表。
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
        """
        它获取频道信息。

        Args:
          channel_id (str): 子频道 ID。

        Returns:
          channel.Channel
        """
        route = Route(
            "GET",
            "/channels/{channel_id}",
            channel_id=channel_id,
        )
        return await self._http.request(route)

    async def get_channels(self, guild_id: str) -> List[channel.Channel]:
        """
        获取频道下的子频道列表

        Args:
          guild_id (str): 频道 ID。

        Returns:
          List[channel.Channel]
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
        """
        创建子频道

        Args:
          guild_id (str): 频道 ID。
          name (str): 子频道名。
          type (channel.ChannelType): 子频道类型
          sub_type (channel.ChannelSubType): 子频道子类型

        Kwargs（fields）:
          position (int): 排序，非必填
          parent_id (str): 否,分组 ID

        Returns:
          通道对象。
        """
        payload = {
            "name": name,
            "type": type.value,
            "subtype": sub_type.value,
        }
        valid_keys = ("position", "parent_id")
        payload.update({k: v for k, v in fields.items() if k in valid_keys and v})
        route = Route("POST", "/guilds/{guild_id}/channels", guild_id=guild_id)
        return await self._http.request(route, json=payload)

    async def update_channel(self, channel_id: str, **fields) -> channel.Channel:
        """
        更新子频道。

        Args:
          channel_id (str): 要修改的子频道ID。

        Kwargs:
          name	            string	子频道名
          position	        int	    排序
          parent_id	        string	分组 id
          private_type	    int	    子频道私密类型 PrivateType
          speak_permission	int	    子频道发言权限 SpeakPermission

        Returns:Dict:
          channel.Channel
        """
        valid_keys = ("name", "position", "parent_id", "private_type", "speak_permission")
        payload = {k: v for k, v in fields.items() if k in valid_keys and v}
        route = Route("PATCH", "/channels/{channel_id}", channel_id=channel_id)
        return await self._http.request(route, json=payload)

    async def delete_channel(self, channel_id: str) -> channel.Channel:
        """
        删除子频道

        Args:
          channel_id (str): 要删除的子频道 ID。

        Returns:Dict:
          删除后的channel.Channel
        """
        route = Route("DELETE", "/channels/{channel_id}", channel_id=channel_id)
        return await self._http.request(route)

    # 子频道权限相关接口
    async def get_channel_user_permissions(self, channel_id: str, user_id: str) -> channel.ChannelPermissions:
        """
        获取指定子频道用户的权限。

        Args:
          channel_id (str): 子频道 ID。
          user_id (str): 用户 ID。

        Returns:Dict
          channel.ChannelPermissions
        """
        route = Route(
            "GET", "/channels/{channel_id}/members/{user_id}/permissions", channel_id=channel_id, user_id=user_id
        )
        return await self._http.request(route)

    async def update_channel_user_permissions(
        self, channel_id: str, user_id: str, add: Permission = None, remove: Permission = None
    ) -> str:
        """
        修改指定子频道用户的权限。

        Args:
          channel_id (str): 子频道 ID。
          user_id (str): 您要更改其权限的用户的用户 ID。
          add (Permission): 添加到用户的权限。使用示例：`add = Permission(view_permission=True)`
          remove (Permission): 删除的权限类型，示例：`remove = Permission(view_permission=True,manager_permission=True)`

        Returns:
          返回值是一个字符串。
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
        """
        获取指定子频道身份组的权限。

        Args:
          channel_id (str): 您要获取权限的子频道的 ID。
          role_id (str): 您要编辑的身份组 ID。

        Returns:Dict
          channel.ChannelPermissions 的字典数据
        """
        route = Route(
            "GET", "/channels/{channel_id}/roles/{role_id}/permissions", channel_id=channel_id, role_id=role_id
        )
        return await self._http.request(route)

    async def update_channel_role_permissions(
        self, channel_id: str, role_id: str, add: Permission = None, remove: Permission = None
    ) -> str:
        """
        修改指定子频道身份组的权限

        Args:
          channel_id (str): 您要更改权限的子频道的 ID。
          role_id (str): 要修改的身份组 ID。
          add (Permission):  添加的权限类型，示例：添加可读权限，`add = Permission(view_permission=True)`
          remove (Permission):  删除的权限类型，示例：删除可读和发言权限, `remove = Permission(view_permission=True,speak_permission=True)`

        Returns:
          返回值是一个字符串。
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
        """
        发送消息。

        注意:
        - 要求操作人在该子频道具有发送消息的权限。
        - 发送成功之后，会触发一个创建消息的事件。
        - 被动回复消息有效期为 5 分钟
        - 主动推送消息每日每个子频道限 2 条
        - 发送消息接口要求机器人接口需要链接到websocket gateway 上保持在线状态

        Args:
          channel_id (str): 您要将消息发送到的子频道的 ID。
          content (str): 消息的文本内容。
          embed (message.Embed): embed 消息，一种特殊的 ark
          ark (message.Ark): ark 模版消息
          message_reference (message.Reference): 对消息的引用。
          image (str): 要发送的图像的 URL。
          msg_id (str): 您要回复的消息的 ID。您可以从 AT_CREATE_MESSAGE 事件中获取此 ID。
          event_id (str): 您要回复的消息的事件 ID。
          markdown (message.Markdown): markdown 消息

        Returns:
          message.Message: 一个消息字典对象。
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
    async def _get_ws_url(self):
        """
        返回机器人的 websocket URL

        Returns:
          url字典数据。通过 `data['urk']` 获取
        """
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
