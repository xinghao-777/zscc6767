import pygame as pg
import math
class Mask_Surface():
    def __init__(self, hex_size, image_address):
        self.hex_size = hex_size
        self.image_address = image_address
    def solving(self):
        image = pg.image.load(self.image_address).convert_alpha()  # convert_alpha()转化像素格式
        # 图片六边形中心与顶点
        center_x, center_y = image.get_width() // 2, image.get_height() // 2
        vertices = [(center_x + self.hex_size * math.sin(i * math.pi / 3),
                     center_y - self.hex_size * math.cos(i * math.pi / 3))
                    for i in range(6)]

        # 创建蒙版Surface
        mask_surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))  # 填充为黑色透明

        # 绘制六边形蒙版
        pg.draw.polygon(mask_surface, (255, 255, 255, 255), vertices)

        # 应用蒙版
        result_surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        result_surface.blit(image, (0, 0))  # 绘制原始图像到result_surface,坐标不能改
        result_surface.blit(mask_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

        return result_surface  # 返回遮罩后的图像
