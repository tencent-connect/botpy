# -*- coding: utf-8 -*-

import json


class JsonUtil:
    @staticmethod
    def json_str2obj(json_str, obj):
        """
        转换的对象默认值会带上，建议还是用json.loads(object_hook)的方式
        """
        py_data = json.loads(json_str)
        _dic2class(py_data, obj)
        return obj

    @staticmethod
    def obj2json_str(obj):
        return json.dumps(obj, default=_convert_to_builtin_type)

    @staticmethod
    def obj2json_serialize(obj):
        return json.loads(JsonUtil.obj2json_str(obj))


def _dic2class(py_data, obj):
    for name in [name for name in dir(obj) if not name.startswith("_")]:
        if name not in py_data:
            setattr(obj, name, None)
        else:
            value = getattr(obj, name)
            setattr(obj, name, _set_value(value, py_data[name]))


def _set_value(value, py_data):
    if str(type(value)).__contains__("."):
        # value 为自定义类
        _dic2class(py_data, value)
    elif str(type(value)) == "<class 'list'>":
        # value为列表
        if value.__len__() == 0:
            # value列表中没有元素，无法确认类型
            value = py_data
        else:
            # value列表中有元素，以第一个元素类型为准
            child_value_type = type(value[0])
            value.clear()
            for child_py_data in py_data:
                child_value = child_value_type()
                child_value = _set_value(child_value, child_py_data)
                value.append(child_value)
    else:
        value = py_data
    return value


def _convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    return d
