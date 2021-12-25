# -*- coding: utf-8 -*-

import os

from qqbot.core.util.yaml_util import YamlUtil

# github下修改 .test(demo).yaml 为 .test.yaml
test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), ".test.yaml"))
