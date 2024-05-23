import math
import pygame as pg
import hexmap
import mask
import random

# 防御精灵
class Cardsprite(pg.sprite.Sprite): # 继承父类
    def __init__(self, Map, image_path=None):
        super().__init__()
        self.Map = Map # 接受地图实例
        self.rc = None # 未放之前无行列坐标
        self.levelpoint = 1 # 等级点数
        self.levels = 1 # 初始等级
        self.cost = None # 留给下级继承
        self.health = None # 留给下级继承
        self.damage = None # 留给下级继承(当前血量)
        self.max_health = None # 留给下级继承(初始血量)
        self.image = mask.Mask_Surface(hexmap.HexagonalMap().HEX_SIZE, image_path).solving() # 加载蒙版后的图片

    def place(self, game_state, pos): # 放置塔数据在地图格上（pos为鼠标的位置（元组））
        if game_state >= self.cost:
            self.rc = self.Map.get_closest_hexagon_xy(self, pos)  # 获取当前鼠标点的行列
            if not self.Map.hexagons[self.rc[0]][self.rc[1]]["c"]:
                game_state -= self.cost
                self.xy = self.Map.hexagons[self.rc[0]][self.rc[1]]["x"], self.Map.hexagons[self.rc[0]][self.rc[1]]["y"] # 根据行列坐标创建实际坐标
                self.Map.hexagons[self.rc[0]][self.rc[1]]["c"] = 1 # 更改hex_map的属性，表示该格有牌
                return game_state
        else:
            print("没有足够的资源来放置这个卡牌。")


    def destroy(self, attach, hex_map):  # 摧毁，需要改逻辑，self.health被enemgy调用而减少，还有铲子的操作
        if self.health <= 0:
            if not self.rc:
                hex_map.hexagons[self.rc[0]][self.rc[1]]["c"] = None
                self.rc = None


    def _up_level(self):  # 与击杀关联
        if self.levels < 3:
            if self.levelpoint >= 5:  # 每五点经验升一级
                self.max_health += 5
                self.health = self.max_health
                self.damage += 1
                self.levelpoint = 0
                self.levels += 1


class Shooter(Cardsprite):
    def __init__(self):
        super().__init__(Cardsprite)
        self.cost = 20
        self.health = 20
        self.max_health = 20
        self.damage = 5
        self.attack_rate = 1
        self.shoot_distance = None  # 默认攻击距离

    def __shoot_distance__(self, distance = None): # 设定攻击距离
        if self.damage > 0:
            self.shoot_distance = float("inf")
        if not distance:
            self.shoot_distance = distance

    def __shoot_rate__(self, speed = None): # 设定攻击速度
        if self.damage > 0:
            self.attack_rate = 1 # 一秒为间隔
        if not speed:
            self.attack_rate = speed

    def shoot(self, enemgy_xy, Shooter_bullet): # 射击
        self.__shoot_distance__()
        self.__shoot_rate__()
        if self.damage > 0:
            dx = enemgy_xy[0] - self.xy[0]
            dy = enemgy_xy[1] - self.xy[1]
            return dx, dy


# 子弹模型
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = None
        self.image = None
        self.direction = None
        self.x = x
        self.y = y


    def flying(self):
        self.x += self.change_x
        self.y += self.change_y


class Shooter_bullet(Bullet):
    def __init__(self):
        super().__init__(x, y)
        self.x = x
        self.y = y


# 敌方
class Basic_enemgy(pg.sprite.Sprite):
    def __init__(self, Map):
        super().__init__()
        self.health = 20  # 血量
        self.attack = 10  # 攻击
        self.speed = 0 # 速度
        self.survive = None  # 是否存活
        self.rc = (1, 1) # 行列
        self.Map = Map # 获取地图实例
        self.xy = Map.hexagons[self.rc[0]][self.rc[1]]["x"], Map.hexagons[self.rc[0]][self.rc[1]]["y"]

    def create(self, rc, Map):
        self.Map.hexagons[rc[0]][rc[1]]["e"] += 1

    def _move_(self):
        pass

    def attach(self):
        pass

    def die(self):
        pass
