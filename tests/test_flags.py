import unittest

import botpy


class IntentsTestCase(unittest.TestCase):
    def test_none(self):
        intents = botpy.Intents.none()
        self.assertEqual(intents.value, 0)  # add assertion here

    def test_multi_intents(self):
        intents = botpy.Intents(guilds=True, guild_messages=True)
        self.assertEqual(513, intents.value)

    def test_default(self):
        intents = botpy.Intents.default()
        self.assertEqual(1879047679, intents.value)


if __name__ == "__main__":
    unittest.main()
