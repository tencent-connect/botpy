#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import qqbot
from qqbot.core.exception.error import (
    AuthenticationFailedError,
    SequenceNumberError,
    ServerError,
)
from qqbot.core.util import logging
from qqbot.model.api_permission import (
    PermissionDemandToCreate,
    APIPermissionDemandIdentify,
)
from qqbot.model.emoji import EmojiType
from tests import test_config

logger = logging.getLogger()

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
CHANNEL_SCHEDULE_ID = test_params_["channel_schedule_id"]
ROBOT_NAME = test_params_["robot_name"]
IS_SANDBOX = test_params_["is_sandbox"]
MESSAGE_ID = test_params_["message_id"]

class GuildAPITestCase(unittest.TestCase):
    api = qqbot.GuildAPI(token, IS_SANDBOX)

    def test_guild(self):
        guild = self.api.get_guild(GUILD_ID)
        self.assertNotEqual("", guild.name)


class GuildRoleAPITest(unittest.TestCase):
    api = qqbot.GuildRoleAPI(token, IS_SANDBOX)

    def test_guild_roles(self):
        guild_roles = self.api.get_guild_roles(GUILD_ID)
        self.assertEqual(GUILD_ID, guild_roles.guild_id)

    def test_guild_role_create_update_delete(self):
        role_info = qqbot.RoleUpdateInfo("Test Role", 4278245297, 0)
        result = self.api.create_guild_role(GUILD_ID, role_info)
        role_id = result.role_id
        self.assertEqual("Test Role", result.role.name)

        role_info = qqbot.RoleUpdateInfo("Test Update Role", 4278245297, 0)
        result = self.api.update_guild_role(GUILD_ID, role_id, role_info)
        self.assertEqual("Test Update Role", result.role.name)

        result = self.api.delete_guild_role(GUILD_ID, role_id)
        self.assertEqual(True, result)

    def test_guild_role_member_add_delete(self):
        result = self.api.create_guild_role_member(
            GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID
        )
        self.assertEqual(True, result)

    def test_guild_role_member_delete(self):
        result = self.api.delete_guild_role_member(
            GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID
        )
        self.assertEqual(True, result)


class GuildMemberAPITestCase(unittest.TestCase):
    api = qqbot.GuildMemberAPI(token, IS_SANDBOX)

    def test_guild_member(self):
        member = self.api.get_guild_member(GUILD_ID, GUILD_OWNER_ID)
        self.assertEqual(GUILD_OWNER_NAME, member.user.username)

    def test_guild_members(self):
        query_params = qqbot.QueryParams("0", 1)
        try:
            members = self.api.get_guild_members(GUILD_ID, query_params)
            print(members)
        except AuthenticationFailedError as e:
            print(e.args)


class ChannelAPITestCase(unittest.TestCase):
    api = qqbot.ChannelAPI(token, IS_SANDBOX)

    def test_channel(self):
        channel = self.api.get_channel(CHANNEL_ID)
        self.assertEqual(CHANNEL_NAME, channel.name)

    def test_channels(self):
        channels = self.api.get_channels(GUILD_ID)
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
        channel = self.api.create_channel(GUILD_ID, request)
        # patch
        patch_channel = qqbot.PatchChannelRequest(
            "update_channel", qqbot.ChannelType.TEXT_CHANNEL, 99, CHANNEL_PARENT_ID
        )
        api_patch_channel = self.api.update_channel(channel.id, patch_channel)
        self.assertEqual("update_channel", api_patch_channel.name)
        # delete
        delete_channel = self.api.delete_channel(channel.id)
        self.assertEqual("update_channel", delete_channel.name)


class ChannelPermissionsTestCase(unittest.TestCase):
    api = qqbot.ChannelPermissionsAPI(token, IS_SANDBOX)

    def test_channel_permissions(self):
        channel_permissions = self.api.get_channel_permissions(
            CHANNEL_ID, GUILD_OWNER_ID
        )
        self.assertEqual("6", channel_permissions.permissions)

    def test_channel_permissions_update(self):
        request = qqbot.UpdatePermission(add="4")
        result = self.api.update_channel_permissions(
            CHANNEL_ID, GUILD_TEST_MEMBER_ID, request
        )
        self.assertEqual(True, result)

    def test_channel_role_permissions(self):
        channel_permissions = self.api.get_channel_role_permissions(
            CHANNEL_ID, GUILD_TEST_ROLE_ID
        )
        self.assertEqual("0", channel_permissions.permissions)

    def test_channel_role_permissions_update(self):
        request = qqbot.UpdatePermission(add="0")
        result = self.api.update_channel_permissions(
            CHANNEL_ID, GUILD_TEST_ROLE_ID, request
        )
        self.assertEqual(True, result)


class UserAPITestCase(unittest.TestCase):
    api = qqbot.UserAPI(token, IS_SANDBOX)

    def test_me(self):
        user = self.api.me()
        self.assertEqual(ROBOT_NAME, user.username)

    def test_me_guilds(self):
        guilds = self.api.me_guilds()
        self.assertNotEqual(0, len(guilds))

        option = qqbot.ReqOption(after=GUILD_ID)
        guilds = self.api.me_guilds(option)
        self.assertEqual(0, len(guilds))


class AudioTestCase(unittest.TestCase):
    api = qqbot.AudioAPI(token, IS_SANDBOX)

    def test_post_audio(self):
        audio = qqbot.AudioControl("", "Test", qqbot.STATUS.START)
        try:
            result = self.api.post_audio(CHANNEL_ID, audio)
            print(result)
        except AuthenticationFailedError as e:
            print(e)


class DmsTestCase(unittest.TestCase):
    api = qqbot.DmsAPI(token, IS_SANDBOX)

    def test_create_and_send_dms(self):
        try:
            # 私信接口需要链接ws，单元测试无法测试可以在run_websocket测试
            request = qqbot.CreateDirectMessageRequest(GUILD_ID, GUILD_OWNER_ID)
            direct_message_guild = self.api.create_direct_message(request)
            send_msg = qqbot.MessageSendRequest("test")
            message = self.api.post_direct_message(
                direct_message_guild.guild_id, send_msg
            )
            print(message.content)
        except (SequenceNumberError, ServerError) as e:
            print(e)


class WebsocketTestCase(unittest.TestCase):
    api = qqbot.WebsocketAPI(token, IS_SANDBOX)

    def test_ws(self):
        ws = self.api.ws()
        self.assertEqual(ws["url"], "wss://api.sgroup.qq.com/websocket")


class MuteTestCase(unittest.TestCase):
    api = qqbot.MuteAPI(token, IS_SANDBOX)

    def test_mute_all(self):
        option = qqbot.MuteOption(mute_seconds="120")
        result = self.api.mute_all(GUILD_ID, option)
        self.assertEqual(True, result)

    def test_mute_member(self):
        option = qqbot.MuteOption(mute_seconds="120")
        result = self.api.mute_member(GUILD_ID, GUILD_TEST_MEMBER_ID, option)
        self.assertEqual(True, result)


class APIPermissionTestCase(unittest.TestCase):
    api = qqbot.APIPermissionAPI(token, IS_SANDBOX)

    def test_get_permissions(self):
        result = self.api.get_permissions(GUILD_ID)
        self.assertNotEqual(0, result)

    def test_post_permissions_demand(self):
        demand_identity = APIPermissionDemandIdentify(
            "/guilds/{guild_id}/members/{user_id}", "GET"
        )
        permission_demand_to_create = PermissionDemandToCreate(
            CHANNEL_ID, demand_identity
        )
        result = self.api.post_permission_demand(GUILD_ID, permission_demand_to_create)
        print(result.title)


class APIScheduleTestCase(unittest.TestCase):
    api = qqbot.ScheduleAPI(token, IS_SANDBOX)

    def test_get_schedules(self):
        schedules = self.api.get_schedules(CHANNEL_SCHEDULE_ID)
        self.assertEqual(None, schedules)


class APIReactionTestCase(unittest.TestCase):
    api = qqbot.ReactionAPI(token, IS_SANDBOX)

    def test_put_reaction(self):
        result = self.api.put_reaction(CHANNEL_ID, MESSAGE_ID, EmojiType.system, "4")
        self.assertEqual(True, result)

    def test_delete_reaction(self):
        result = self.api.delete_reaction(CHANNEL_ID, MESSAGE_ID, EmojiType.system, "4")
        self.assertEqual(True, result)


class APIPinstestCase(unittest.TestCase):
    api = qqbot.PinsAPI(token, IS_SANDBOX)

    def test_put_pin(self):
        result = self.api.put_pin(CHANNEL_ID, MESSAGE_ID)
        self.assertTrue(MESSAGE_ID in result.message_ids)

    def test_delete_pin(self):
        result = self.api.delete_pin(CHANNEL_ID, MESSAGE_ID)
        self.assertEqual(True, result)

    def test_get_pins(self):
        result = self.api.get_pins(CHANNEL_ID)
        self.assertTrue(len(result.message_ids) >= 0)


if __name__ == "__main__":
    unittest.main()
