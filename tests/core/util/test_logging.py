#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest

from qqbot.core.util import logging as new_logging

logger = new_logging.getLogger()


class MyTestCase(unittest.TestCase):
    def test__getLevel(self):
        level = new_logging._getLevel()
        logger.info("level: %d" % level)
        self.assertTrue(
            level
            in (
                logging.NOTSET,
                logging.DEBUG,
                logging.INFO,
                logging.WARNING,
                logging.ERROR,
                logging.CRITICAL,
            )
        )

    def test_getLogger(self):
        self.assertIsInstance(logger, logging.Logger)


if __name__ == "__main__":
    unittest.main()
