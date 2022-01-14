#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import unittest

import qqbot
from qqbot.core.exception.error import (
    AuthenticationFailedError,
    SequenceNumberError,
    ServerError,
)
from qqbot.core.util import logging
from tests import test_config

logger = logging.getLogger(__name__)

token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
test_params_ = test_config["test_params"]
GUILD_ID = test_params_["guild_id"]
GUILD_OWNER_ID = test_params_["guild_owner_id"]
GUILD_OWNER_NAME = test_params_["guild_owner_name"]
GUILD_TEST_MEMBER_ID = test_params_["guild_test_member_id"]
GUILD_TEST_ROLE_ID = test_params_["guild_test_role_id"]
CHANNEL_ID = test_params_["channel_id"]
CHANNEL_NAME = test_params_["channel_name"]
CHANNEL_PARENT_ID = test_params_["channel_parent_id"]
ROBOT_NAME = test_params_["robot_name"]
IS_SANDBOX = test_params_["is_sandbox"]


class GuildAPITestCase(unittest.TestCase):
    api = qqbot.AsyncGuildAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_guild(self):
        guild = self.loop.run_until_complete(self.api.get_guild(GUILD_ID))
        self.assertNotEqual("", guild.name)


class GuildRoleAPITest(unittest.TestCase):
    api = qqbot.AsyncGuildRoleAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_guild_roles(self):
        guild_roles = self.loop.run_until_complete(self.api.get_guild_roles(GUILD_ID))
        self.assertEqual(GUILD_ID, guild_roles.guild_id)

    def test_guild_role_create_update_delete(self):
        role_info = qqbot.RoleUpdateInfo("Test Role", 4278245297, 0)
        result = self.loop.run_until_complete(
            self.api.create_guild_role(GUILD_ID, role_info)
        )
        role_id = result.role_id
        self.assertEqual("Test Role", result.role.name)

        role_info = qqbot.RoleUpdateInfo("Test Update Role", 4278245297, 0)
        result = self.loop.run_until_complete(
            self.api.update_guild_role(GUILD_ID, role_id, role_info)
        )
        self.assertEqual("Test Update Role", result.role.name)

        result = self.loop.run_until_complete(
            self.api.delete_guild_role(GUILD_ID, role_id)
        )
        self.assertEqual(True, result)

    def test_guild_role_member_add_delete(self):
        result = self.loop.run_until_complete(
            self.api.create_guild_role_member(
                GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID
            )
        )
        self.assertEqual(True, result)

    def test_guild_role_member_delete(self):
        result = self.loop.run_until_complete(
            self.api.delete_guild_role_member(
                GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID
            )
        )
        self.assertEqual(True, result)


class GuildMemberAPITestCase(unittest.TestCase):
    api = qqbot.AsyncGuildMemberAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_guild_member(self):
        member = self.loop.run_until_complete(
            self.api.get_guild_member(GUILD_ID, GUILD_OWNER_ID)
        )
        self.assertEqual(GUILD_OWNER_NAME, member.user.username)

    def test_guild_members(self):
        query_params = qqbot.QueryParams("0", 1)
        try:
            members = self.loop.run_until_complete(
                self.api.get_guild_members(GUILD_ID, query_params)
            )
            print(members)
        except AuthenticationFailedError as e:
            print(e.args)


class ChannelAPITestCase(unittest.TestCase):
    api = qqbot.AsyncChannelAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_channel(self):
        channel = self.loop.run_until_complete(self.api.get_channel(CHANNEL_ID))
        self.assertEqual(CHANNEL_NAME, channel.name)

    def test_channels(self):
        channels = self.loop.run_until_complete(self.api.get_channels(GUILD_ID))
        self.assertNotEqual(0, len(channels))

    def test_create_update_delete_channel(self):
        # create
        request = qqbot.CreateChannelRequest(
            "channel_test",
            qqbot.ChannelType.TEXT_CHANNEL,
            qqbot.ChannelSubType.TALK,
            99,
            CHANNEL_PARENT_ID,
        )
        channel = self.loop.run_until_complete(
            self.api.create_channel(GUILD_ID, request)
        )
        # patch
        patch_channel = qqbot.PatchChannelRequest(
            "update_channel", qqbot.ChannelType.TEXT_CHANNEL, 99, CHANNEL_PARENT_ID
        )
        api_patch_channel = self.loop.run_until_complete(
            self.api.update_channel(channel.id, patch_channel)
        )
        self.assertEqual("update_channel", api_patch_channel.name)
        # delete
        delete_channel = self.loop.run_until_complete(
            self.api.delete_channel(channel.id)
        )
        self.assertEqual("update_channel", delete_channel.name)


class ChannelPermissionsTestCase(unittest.TestCase):
    api = qqbot.AsyncChannelPermissionsAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_channel_permissions(self):
        channel_permissions = self.loop.run_until_complete(
            self.api.get_channel_permissions(CHANNEL_ID, GUILD_OWNER_ID)
        )
        self.assertEqual("6", channel_permissions.permissions)

    def test_channel_permissions_update(self):
        request = qqbot.UpdatePermission("0x0000000002", "")
        result = self.loop.run_until_complete(
            self.api.update_channel_permissions(
                CHANNEL_ID, GUILD_TEST_MEMBER_ID, request
            )
        )
        self.assertEqual(True, result)

    def test_channel_role_permissions(self):
        channel_permissions = self.loop.run_until_complete(
            self.api.get_channel_role_permissions(CHANNEL_ID, GUILD_TEST_ROLE_ID)
        )
        self.assertEqual("0", channel_permissions.permissions)

    def test_channel_role_permissions_update(self):
        request = qqbot.UpdatePermission("0x0000000002", "")
        result = self.loop.run_until_complete(
            self.api.update_channel_permissions(CHANNEL_ID, GUILD_TEST_ROLE_ID, request)
        )
        self.assertEqual(True, result)


class UserAPITestCase(unittest.TestCase):
    api = qqbot.AsyncUserAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_me(self):
        user = self.loop.run_until_complete(self.api.me())
        self.assertEqual(ROBOT_NAME, user.username)

    def test_me_guilds(self):
        guilds = self.loop.run_until_complete(self.api.me_guilds())
        self.assertNotEqual(0, len(guilds))

        option = qqbot.ReqOption("", GUILD_ID, "1")
        guilds = self.loop.run_until_complete(self.api.me_guilds(option))
        self.assertEqual(1, len(guilds))


class AudioTestCase(unittest.TestCase):
    api = qqbot.AsyncAudioAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_post_audio(self):
        audio = qqbot.AudioControl("", "Test", qqbot.STATUS.START)
        try:
            result = self.loop.run_until_complete(
                self.api.post_audio(CHANNEL_ID, audio)
            )
            print(result)
        except AuthenticationFailedError as e:
            print(e)


class MessageTestCase(unittest.TestCase):
    api = qqbot.AsyncMessageAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_create_and_send_dms(self):
        try:
            # 私信接口需要链接ws，单元测试无法测试可以在run_websocket测试
            request = qqbot.CreateDirectMessageRequest(GUILD_ID, GUILD_OWNER_ID)
            direct_message_guild = self.loop.run_until_complete(
                self.api.create_direct_message(request)
            )
            send_msg = qqbot.MessageSendRequest("test")
            message = self.loop.run_until_complete(
                self.api.post_direct_message(direct_message_guild.guild_id, send_msg)
            )
            print(message.content)
        except (SequenceNumberError, ServerError) as e:
            print(e)


class WebsocketTestCase(unittest.TestCase):
    api = qqbot.AsyncWebsocketAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_ws(self):
        ws = self.loop.run_until_complete(self.api.ws())
        self.assertEqual(ws["url"], "wss://api.sgroup.qq.com/websocket")


class MuteTestCase(unittest.TestCase):
    api = qqbot.AsyncMuteAPI(token, IS_SANDBOX)
    loop = asyncio.get_event_loop()

    def test_mute_all(self):
        option = qqbot.MuteOption(mute_seconds="120")
        result = self.loop.run_until_complete(self.api.mute_all(GUILD_ID, option))
        self.assertEqual(True, result)

    def test_mute_member(self):
        option = qqbot.MuteOption(mute_seconds="120")
        result = self.loop.run_until_complete(
            self.api.mute_member(GUILD_ID, GUILD_OWNER_ID, option)
        )
        self.assertEqual(True, result)


if __name__ == "__main__":
    unittest.main()
