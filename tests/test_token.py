#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from botpy.robot import Token


class MyTestCase(unittest.TestCase):
    def test_something(self):
        token = Token("123", "123")
        self.assertEqual(token.get_string(), "123.123")


if __name__ == "__main__":
    unittest.main()
