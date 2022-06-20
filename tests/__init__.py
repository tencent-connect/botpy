# -*- coding: utf-8 -*-

import os

from botpy.ext.cog_yaml import read

# github下修改 .test(demo).yaml 为 .test.yaml
test_config = read(os.path.join(os.path.dirname(__file__), ".test.yaml"))
