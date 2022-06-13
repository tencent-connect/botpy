# -*- coding: utf-8 -*-


class ColorUtil:
    @staticmethod
    def convert(color: tuple or str):
        """
        将 RGB 值的元组或 HEX 值的字符串转换为单个整数

        Args:
          color (tuple or str): 输入RGB的三位tuple或HEX的sting颜色

        Returns:
          颜色的 RGB 值。
        """
        colors = []
        if isinstance(color, tuple):
            if len(color) == 3:
                for items in color:
                    if not isinstance(items, int) or items > 255 or items < 0:
                        raise TypeError("RGB颜色应为一个三位数的tuple，且当中每个数值都应该介乎于0和255之间，如(255,255,255)")
                    colors.append(int(items))
            else:
                raise TypeError("RGB颜色应为一个三位数的tuple，且当中每个数值都应该介乎于0和255之间，如(255,255,255)")
        elif isinstance(color, str):
            colour = color.replace("#", "")
            if len(colour) == 6:
                for items in [colour[:2], colour[2:4], colour[4:]]:
                    try:
                        local_colour = int(items, 16)
                    except ValueError:
                        raise TypeError("该HEX颜色不存在，请检查其颜色值是否准确")
                    if local_colour > 255 or local_colour < 0:
                        raise TypeError("该HEX颜色不存在，请检查其颜色值是否准确")
                    colors.append(local_colour)
            else:
                raise TypeError('HEX颜色应为一个 #加六位数字或字母 的string，如"#ffffff"')
        else:
            raise TypeError('颜色值应为RGB的三位tuple，如(255,255,255)；或HEX的sting颜色，如"#ffffff"')
        return colors[0] + 256 * colors[1] + 256 * 256 * colors[2]
