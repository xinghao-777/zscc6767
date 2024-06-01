import pygame
import math

# 初始化Pygame
pygame.init()

# 设置屏幕大小和标题
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("旋转图像示例")

# 加载图像
image = pygame.image.load("images/Card_tower/shooter/shooter.png")
image_rect = image.get_rect()
image_center = image_rect.center

# 设置旋转角度
angle = 60

# 旋转图像
rotated_image = pygame.transform.rotate(image, angle)

# 获取旋转后图像的矩形边界
rotated_rect = rotated_image.get_rect()

# 计算旋转后图像的新位置
dx = image_rect.centerx - rotated_rect.centerx
dy = image_rect.centery - rotated_rect.centery
rotated_rect.x += dx
rotated_rect.y += dy

# 游戏循环
running = True
while running:
    # 更新屏幕
    screen.fill((255, 255, 255))
    screen.blit(rotated_image, rotated_rect)
    pygame.display.flip()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
