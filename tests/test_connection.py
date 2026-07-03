import unittest

from botpy.connection import ConnectionState
from botpy.message import GroupMessage


class ConnectionStateTestCase(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.state = ConnectionState(lambda event, *args: self.events.append((event, args)), api=None)

    def test_parse_group_message_create(self):
        payload = {
            "id": "GROUP_MESSAGE_CREATE:test",
            "d": {
                "author": {
                    "id": "member-id",
                    "member_openid": "member-openid",
                },
                "content": "#帮助",
                "group_openid": "group-openid",
                "id": "message-id",
                "timestamp": "2026-07-03T02:41:56+08:00",
            },
        }

        self.assertIn("group_message_create", self.state.parsers)
        self.state.parsers["group_message_create"](payload)

        self.assertEqual(1, len(self.events))
        event, args = self.events[0]
        self.assertEqual("group_message_create", event)

        message = args[0]
        self.assertIsInstance(message, GroupMessage)
        self.assertEqual("#帮助", message.content)
        self.assertEqual("group-openid", message.group_openid)
        self.assertEqual("member-openid", message.author.member_openid)
        self.assertEqual("GROUP_MESSAGE_CREATE:test", message.event_id)


if __name__ == "__main__":
    unittest.main()
