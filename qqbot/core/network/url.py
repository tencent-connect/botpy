# -*- coding: utf-8 -*-


class BaseConstant:
    domain = "api.sgroup.qq.com"
    sandBoxDomain = "sandbox.api.sgroup.qq.com"
    scheme = "https"


class APIConstant:
    """目前提供的接口的 uri"""

    guildURI = "/guilds/{guild_id}"
    guildMembersURI = "/guilds/{guild_id}/members"
    guildMemberURI = "/guilds/{guild_id}/members/{user_id}"

    rolesURI = "/guilds/{guild_id}/roles"
    roleURI = "/guilds/{guild_id}/roles/{role_id}"
    memberRoleURI = "/guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    channelsURI = "/guilds/{guild_id}/channels"
    channelURI = "/channels/{channel_id}"
    channelPermissionsURI = "/channels/{channel_id}/members/{user_id}/permissions"

    messagesURI = "/channels/{channel_id}/messages"
    messageURI = "/channels/{channel_id}/messages/{message_id}"

    userMeURI = "/users/@me"
    userMeGuildsURI = "/users/@me/guilds"
    userMeDMURI = "/users/@me/dms"

    gatewayURI = "/gateway"
    gatewayBotURI = "/gateway/bot"

    audioControlURI = "/channels/{channel_id}/audio"
    dmsURI = "/dms/{guild_id}/messages"


def get_url(url_format, is_sandbox):
    d = BaseConstant.domain
    if is_sandbox:
        d = BaseConstant.sandBoxDomain
    s__format = "{}://{}{}".format(BaseConstant.scheme, d, url_format)
    return s__format
