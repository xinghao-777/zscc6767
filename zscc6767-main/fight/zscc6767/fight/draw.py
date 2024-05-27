import pygame
import random


# 假设有一个Hexagon类表示六边形网格，这里我们只关心其行列索引

# Sprite类，继承自pygame.sprite.Sprite
class MySprite(pygame.sprite.Sprite):
    def __init__(self, hexagon, screen, sprite_image):
        super().__init__()
        self.image = sprite_image
        self.rect = self.image.get_rect(topleft=(hexagon.col * hex_size, hexagon.row * hex_height_adj))
        self.hexagon = hexagon
        self.path = self.generate_path_to_center()
        self.current_hex = (hexagon.row, hexagon.col)

    def generate_path_to_center(self):
        # 假设中心点为 (middle_row, 0)
        middle_row = self.hexagon.row_count // 2
        path = []
        current_row, current_col = self.hexagon.row, self.hexagon.col
        while current_row > middle_row:
            path.append((current_row, current_col))
            if current_col == 0:
                current_col += 1
            elif current_col == current_row:
                current_row -= 1
            else:
                current_col -= 1
        path.append((middle_row, 0))  # 添加中心点
        return path

    def update(self):
        if self.current_hex in self.path:
            next_hex = self.path[self.path.index(self.current_hex) + 1]
            self.rect.topleft = (next_hex[1] * hex_size, next_hex[0] * hex_height_adj)
            self.current_hex = next_hex

        # 地图生成逻辑（假设这部分已经存在）


class HexagonalMap:
    # ... 省略其他属性和方法 ...

    def generate_sprites(self, screen, sprite_image):
        sprites = pygame.sprite.Group()
        # 只在外圈生成Sprite
        for row in (0, self.num_rows - 1):
            for col in range(row + (self.middle_row - 1) // 2):
                hexagon = Hexagon(row, col, self.num_rows)  # 假设Hexagon类接受行列和总行数作为参数
                sprite = MySprite(hexagon, screen, sprite_image)
                sprites.add(sprite)
                # 随机选择一个外圈Sprite作为起点（可选）
        # ...
        return sprites

    # pygame初始化


pygame.init()
screen = pygame.display.set_mode((800, 600))  # 假设屏幕大小
clock = pygame.time.Clock()
hex_size = 30  # 假设每个六边形的宽度
hex_height = 20 * (3 ** 0.5 / 2)  # 正六边形高度（等边三角形高）
hex_height_adj = hex_height * 2 / 3  # 调整高度以适应竖直放置的六边形
sprite_image = pygame.Surface((hex_size, hex_height_adj))  # 假设Sprite图像大小与六边形匹配
sprite_image.fill((255, 0, 0))  # 红色

# 创建地图和Sprite（假设HexagonalMap已经创建好）
map_instance = HexagonalMap(13)  # 假设这是一个已存在的类实例
sprites = map_instance.generate_sprites(screen, sprite_image)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # 填充背景色
    sprites.update()  # 更新Sprite位置
    sprites.draw(screen)  # 绘制Sprite
    pygame.display.flip()  # 更新屏幕显示
    clock.tick(60)  # 控制帧率

pygame.quit()