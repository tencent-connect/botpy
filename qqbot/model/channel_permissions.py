# -*- coding: utf-8 -*-


class ChannelPermissions:
    def __init__(self, data=None):
        self.channel_id: str = ""
        self.user_id: str = ""
        self.permissions: str = ""
        self.role_id: str = ""
        if data is not None:
            self.__dict__ = data


class UpdatePermission:
    def __init__(self, add: str = None, remove: str = None):
        """
        要求操作人具有管理子频道的权限，如果是机器人，则需要将机器人设置为管理员。
        参数包括add和remove两个字段，分别表示授予的权限以及删除的权限。要授予用户权限即把add对应位置1，删除用户权限即把remove对应位置1。当两个字段同一位都为1，表现为删除权限。
        本接口不支持修改可管理子频道权限。

        :param add: 字符串形式的位图表示赋予用户的权限
        :param remove:字符串形式的位图表示删除用户的权限
        """
        self.add = add
        self.remove = remove
