#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import time
import unittest
from typing import List

import botpy
from botpy import logging, BotHttp, Permission
from botpy.errors import (
    AuthenticationFailedError,
    ServerError,
)
from botpy.types import guild, user, channel, message
from botpy.types.announce import AnnouncesType
from botpy.types.channel import ChannelType, ChannelSubType
from tests import test_config

logger = logging.get_logger()

token = botpy.Token(test_config["token"]["appid"], test_config["token"]["token"])
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


class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        print("setUp")
        self.loop = asyncio.get_event_loop()
        self.http = BotHttp(timeout=5, app_id=test_config["token"]["appid"], token=test_config["token"]["token"])
        self.api = botpy.BotAPI(self.http)

    def tearDown(self) -> None:
        print("tearDown")
        self.loop.run_until_complete(self.http.close())

    def test_guild(self):
        result: guild.GuildPayload = self.loop.run_until_complete(self.api.get_guild(GUILD_ID))
        self.assertNotEqual("", result["name"])

    def test_guild_roles(self):
        result: guild.GuildRoles = self.loop.run_until_complete(self.api.get_guild_roles(GUILD_ID))
        self.assertEqual(GUILD_ID, result["guild_id"])

    def test_guild_role_create_update_delete(self):
        coroutine = self.api.create_guild_role(GUILD_ID, name="Test Role", color=4278245297)
        result: guild.GuildRole = self.loop.run_until_complete(coroutine)
        self.assertEqual("Test Role", result["role"]["name"])
        id = result["role"]["id"]

        coroutine = self.api.update_guild_role(GUILD_ID, role_id=id, name="Test Update Role")
        result = self.loop.run_until_complete(coroutine)
        self.assertEqual("Test Update Role", result["role"]["name"])

        result = self.loop.run_until_complete(self.api.delete_guild_role(GUILD_ID, role_id=id))
        self.assertEqual(None, result)

    def test_guild_role_member_add_delete(self):
        result = self.loop.run_until_complete(
            self.api.create_guild_role_member(GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID)
        )
        self.assertEqual(None, result)

    def test_guild_role_member_delete(self):
        result = self.loop.run_until_complete(
            self.api.delete_guild_role_member(GUILD_ID, GUILD_TEST_ROLE_ID, GUILD_TEST_MEMBER_ID)
        )
        self.assertEqual(None, result)

    def test_guild_member(self):
        member: user.Member = self.loop.run_until_complete(self.api.get_guild_member(GUILD_ID, GUILD_OWNER_ID))
        self.assertEqual(GUILD_OWNER_NAME, member["user"]["username"])

    def test_guild_members(self):
        try:
            members = self.loop.run_until_complete(self.api.get_guild_members(GUILD_ID))
            print(members)
        except AuthenticationFailedError as e:
            print(e.args)

    def test_channel(self):
        result: channel.ChannelPayload = self.loop.run_until_complete(self.api.get_channel(CHANNEL_ID))
        self.assertEqual(CHANNEL_NAME, result["name"])

    def test_channels(self):
        result: List[channel.ChannelPayload] = self.loop.run_until_complete(self.api.get_channels(GUILD_ID))
        self.assertNotEqual(0, len(result))

    def test_create_update_delete_channel(self):
        # create
        coro = self.api.create_channel(GUILD_ID, "channel_test", ChannelType.TEXT_CHANNEL, ChannelSubType.TALK)
        result: channel.ChannelPayload = self.loop.run_until_complete(coro)
        # patch
        coro = self.api.update_channel(result["id"], name="update_channel")
        result: channel.ChannelPayload = self.loop.run_until_complete(coro)
        self.assertEqual("update_channel", result["name"])
        # delete
        coro = self.api.delete_channel(result["id"])
        delete_channel: channel.ChannelPayload = self.loop.run_until_complete(coro)
        self.assertTrue(result["name"], delete_channel["name"])

    def test_channel_permissions(self):
        coroutine = self.api.get_channel_user_permissions(CHANNEL_ID, GUILD_OWNER_ID)
        channel_permissions: channel.ChannelPermissions = self.loop.run_until_complete(coroutine)
        # 可查看、可发言、可管理
        self.assertEqual("7", channel_permissions["permissions"])

    def test_channel_permissions_update(self):
        remove = Permission(manager_permission=True)
        coroutine = self.api.update_channel_user_permissions(CHANNEL_ID, GUILD_TEST_MEMBER_ID, remove=remove)
        result = self.loop.run_until_complete(coroutine)
        self.assertEqual(None, result)

    def test_channel_role_permissions(self):
        coroutine = self.api.get_channel_role_permissions(CHANNEL_ID, GUILD_TEST_ROLE_ID)
        channel_permissions: channel.ChannelPermissions = self.loop.run_until_complete(coroutine)
        self.assertEqual("0", channel_permissions["permissions"])

    def test_channel_role_permissions_update(self):
        add = Permission(manager_permission=True)
        coroutine = self.api.update_channel_role_permissions(CHANNEL_ID, GUILD_TEST_MEMBER_ID, add=add)
        result = self.loop.run_until_complete(coroutine)
        self.assertEqual(None, result)

    def test_me(self):
        user = self.loop.run_until_complete(self.api.me())
        self.assertEqual(ROBOT_NAME, user["username"])

    def test_me_guilds(self):
        guilds = self.loop.run_until_complete(self.api.me_guilds())
        self.assertEqual(1, len(guilds))

        guilds = self.loop.run_until_complete(self.api.me_guilds(GUILD_ID, limit=1, desc=True))
        self.assertEqual(0, len(guilds))

    def test_post_audio(self):
        payload = {"audio_url": "test", "text": "test", "status": 0}
        try:
            result = self.loop.run_until_complete(self.api.update_audio(CHANNEL_ID, payload))
            print(result)
        except (AuthenticationFailedError, ServerError) as e:
            print(e)

    def test_create_and_send_dms(self):
        payload: message.DmsPayload = self.loop.run_until_complete(self.api.create_dms(GUILD_ID, GUILD_OWNER_ID))
        self.assertIsNotNone(payload["guild_id"])
        self.loop.run_until_complete(self.api.post_dms(payload["guild_id"], content="test", msg_id=MESSAGE_ID))
        # 私信有限制频率
        # self.assertTrue("test", _message["content"])

    def test_ws(self):
        ws = self.loop.run_until_complete(self.api.get_ws_url())
        self.assertEqual(ws["url"], "wss://api.sgroup.qq.com/websocket")

    def test_mute_all(self):
        result = self.loop.run_until_complete(self.api.mute_all(GUILD_ID, mute_seconds="20"))
        self.assertEqual(None, result)

    def test_mute_member(self):
        result = self.loop.run_until_complete(self.api.mute_member(GUILD_ID, GUILD_TEST_MEMBER_ID, mute_seconds="20"))
        self.assertEqual(None, result)

    def test_mute_multi_member(self):
        result: List[str] = self.loop.run_until_complete(
            self.api.mute_multi_member(GUILD_ID, mute_seconds="120", user_ids=[GUILD_TEST_MEMBER_ID])
        )
        self.assertEqual(1, len(result))

    def test_post_recommend_channel(self):
        channel_list = [{"channel_id": CHANNEL_ID, "introduce": "introduce"}]
        result = self.loop.run_until_complete(
            self.api.create_recommend_announce(GUILD_ID, AnnouncesType.MEMBER, channel_list)
        )
        self.assertEqual(len(channel_list), len(result["recommend_channels"]))

    def test_get_permissions(self):
        result = self.loop.run_until_complete(self.api.get_permissions(GUILD_ID))
        self.assertNotEqual(0, len(result))

    def test_post_permissions_demand(self):
        demand_identity = {"path": "/guilds/{guild_id}/members/{user_id}", "method": "GET"}
        result = self.loop.run_until_complete(
            self.api.post_permission_demand(GUILD_ID, CHANNEL_ID, api_identify=demand_identity, desc="test")
        )
        print(result["title"])

    def test_get_schedules(self):
        schedules = self.loop.run_until_complete(self.api.get_schedules(CHANNEL_SCHEDULE_ID))
        self.assertEqual(None, schedules)

    def test_put_and_delete_reaction(self):
        result = self.loop.run_until_complete(self.api.put_reaction(CHANNEL_ID, MESSAGE_ID, 1, "4"))
        self.assertEqual(None, result)

        time.sleep(1)  # 表情表态操作有频率限制，中间隔一秒

        result = self.loop.run_until_complete(self.api.delete_reaction(CHANNEL_ID, MESSAGE_ID, 1, "4"))
        self.assertEqual(None, result)

    def test_get_reaction_users(self):
        result = self.loop.run_until_complete(self.api.get_reaction_users(CHANNEL_ID, MESSAGE_ID, 1, "4"))
        self.assertEqual(result["is_end"], True)

    def test_put_and_delete_pin(self):
        result = self.loop.run_until_complete(self.api.put_pin(CHANNEL_ID, MESSAGE_ID))
        self.assertIsNotNone(result)

        result = self.loop.run_until_complete(self.api.delete_pin(CHANNEL_ID, MESSAGE_ID))
        self.assertEqual(None, result)

    def test_get_pins(self):
        result = self.loop.run_until_complete(self.api.get_pins(CHANNEL_ID))
        self.assertTrue(len(result["message_ids"]) >= 0)


if __name__ == "__main__":
    unittest.main()
