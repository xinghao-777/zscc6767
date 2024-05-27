import random
import pygame as pg
import hexmap
class Basic_enemgy(pg.sprite.Sprite):
    def __init__(self, Map, pos = None, image_path = None):
        super().__init__()
        self.Map = Map  # 获取地图实例
        self.health = 20  # 血量
        self.attack = 10  # 攻击
        self.speed = self.Map.HEX_SIZE_In * 2  # 速度
        self.image = pg.image.load(image_path) if image_path else None
        self.rect = self.image.get_rect(topleft=pos) if self.image else None
        c = self.create()  # 调用本体方法，生成初始位置
        self.xy = c

    def create(self):
        # 只在外圈生成敌人
        list = [_ for _ in range(1,14)]
        row = random.choices(list, weights=[7,2,2,2,2,2,2,2,2,2,2,2,7])[0] # 随机行（1到13）
        if row != 1 or row != 13: # 非首尾行只取改行的首尾列
            col = random.choice(["1", str(row + 6)])
        else:
            col = random.randint(1,row + 6)
        return row, int(col)
a = hexmap.HexagonalMap()
b = Basic_enemgy(a)
print(b.xy)