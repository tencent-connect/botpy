#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from botpy import logging
from botpy.url import get_url, APIConstant

logger = logging.getLogger()


class MyTestCase(unittest.TestCase):
    def test_get_url(self):
        url = get_url(APIConstant.guildMembersURI, False)
        logger.info(url.format(guild_id="123"))
        self.assertEqual(url.format(guild_id="123"), "https://api.sgroup.qq.com/guilds/123/members")

        url = get_url(APIConstant.guildMembersURI, True)
        logger.info(url.format(guild_id="123"))
        self.assertEqual(
            url.format(guild_id="123"),
            "https://sandbox.api.sgroup.qq.com/guilds/123/members",
        )


if __name__ == "__main__":
    unittest.main()
