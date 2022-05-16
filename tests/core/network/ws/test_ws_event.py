#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from botpy.core.network.ws.ws_event import WsEvent


class EventTestCase(unittest.TestCase):
    def test_register_handlers(self):
        intent = WsEvent.event_to_intent(WsEvent.EventGuildCreate, WsEvent.EventMessageCreate)
        self.assertEqual(intent, 513)


if __name__ == "__main__":
    unittest.main()
