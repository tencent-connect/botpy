from typing import List


class Permission:
    def __init__(self, type: int, specify_role_ids: List[str] = None, specify_user_ids: List[str] = None):
        if type:
            self.type = type
        if specify_role_ids:
            self.specify_role_ids = specify_role_ids
        if specify_user_ids:
            self.specify_user_ids = specify_user_ids


class RenderData:
    def __init__(self, label: str, visited_label: str, style: int):
        self.label = label
        self.visited_label = visited_label
        self.style = style


class Action:
    def __init__(self, type: int, permission: Permission, click_limit: int, data: str, at_bot_show_channel_list: bool):
        self.type = type
        self.permission = permission
        self.click_limit = click_limit
        self.data = data
        self.at_bot_show_channel_list = at_bot_show_channel_list


class Button:
    def __init__(self, id: str, render_data: RenderData, action: Action):
        self.id = id
        self.render_data = render_data
        self.action = action


class InlineKeyboardRow:
    def __init__(self, buttons: List[Button]):
        self.buttons = buttons


class InlineKeyboard:
    def __init__(self, rows: List[InlineKeyboardRow]):
        self.rows = rows


