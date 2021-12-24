# -*- coding: utf-8 -*-

import os.path

from qqbot.core.util.yaml_util import YamlUtil

# github下修改为 .test_github.yaml
test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), ".test.yaml"))
