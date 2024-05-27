import math
import pygame as pg
import hexmap
import mask
import random


# 防御精灵
class Cardsprite(pg.sprite.Sprite):  # 继承父类
    def __init__(self, Map, pos=(0, 0), image_path=None):
        super().__init__()
        self.Map = Map  # 接受地图实例
        self.rc = None  # 未放之前无行列坐标
        self.levelpoint = 1  # 等级点数
        self.levels = 1  # 初始等级
        self.cost = None  # 留给下级继承
        self.health = None  # 留给下级继承
        self.damage = None  # 留给下级继承(当前血量)
        self.max_health = None  # 留给下级继承(初始血量)
        self.image = pg.image.load(image_path) if image_path else None
        self.rect = self.image.get_rect(topleft=pos) if self.image else None

    def place(self, game_state, pos):  # 放置塔数据在地图格上（pos为鼠标的位置（元组））
        if game_state >= self.cost:
            self.rc = self.Map.get_closest_hexagon_xy(self, pos)  # 获取当前鼠标点的行列
            if not self.Map.hexagons[self.rc[0]][self.rc[1]]["c"]:
                game_state -= self.cost
                self.xy = self.Map.hexagons[self.rc[0]][self.rc[1]]["xy"] # 根据行列坐标创建实际坐标
                self.Map.hexagons[self.rc[0]][self.rc[1]]["c"] = 1  # 更改hex_map的属性，表示该格有牌
                return game_state
        else:
            print("没有足够的资源来放置这个卡牌。")

    def destroy(self):  # 摧毁，需要改逻辑，self.health被enemgy调用而减少，还有铲子的操作
        if self.rect and self.rc is not None:  # 确保 self.rect 和 self.rc 都被设置了
            self.Map.hexagons[self.rc[0]][self.rc[1]]["c"] = None
            self.kill()
            self.rc = None

    def up_level(self):  # 与击杀关联
        if self.levels < 3:
            if self.levelpoint >= 5:  # 每五点经验升一级
                self.max_health += 5
                self.health = self.max_health
                self.damage += 1
                self.levelpoint = 0
                self.levels += 1

    def updata(self):
        if self.health <= 0:
            self.destroy()
        self.up_level()


class Shooter(Cardsprite):
    def __init__(self, Map, image_path, pos=(0, 0)):
        super().__init__(Map, pos, image_path)  # 传递必要的参数给父类
        # Shooter 特有的属性初始化
        self.cost = 10
        self.health = 10
        self.max_health = self.health
        self.damage = 2
        self.attack_rate = 1
        self.shoot_distance = float("inf")

    def set_shoot_distance(self, distance):
        if distance is not None:
            self.shoot_distance = distance

    def set_shoot_rate(self, speed):
        if speed is not None:
            self.attack_rate = speed

    def shoot(self, enemy_xy, Shooter_bullet):
        if self.damage > 0:
            dx = enemy_xy[0] - self.xy[0]
            dy = enemy_xy[1] - self.xy[1]
            bullet = Shooter_bullet(self.xy[0], self.xy[1])  # 创建子弹实例
            return bullet


# 子弹模型
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = None
        self.image = None
        self.direction = None
        self.x = x
        self.y = y

    def updata(self):
        self.x += self.change_x
        self.y += self.change_y
        # 检查子弹是否移出屏幕，如果是，则将其标记为“死亡”
        if not screen.get_rect().colliderect(self.rect):
            self.is_alive = False


class Shooter_bullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)


# 敌方
class Basic_enemgy(pg.sprite.Sprite):
    def __init__(self, Map, screen, image_address = None):
        super().__init__()
        self.Map = Map  # 获取地图实例
        self.health = 20  # 血量
        self.attack = 10  # 攻击
        self.speed = self.Map.HEX_SIZE_In * 2  # 速度
        self.survive = None  # 是否存活
        self.image = pg.image.load(image_address)
        self.create(screen)  # 调用本体方法，生成初始位置，并返回创建的精灵
        self.xy = Map.hexagons[self.rc[0]][self.rc[1]]["xy"]

    def create(self, screen):
        sprites = pg.sprite.Group()
        # 只在外圈生成敌人
        row = random.randint(1,13) # 随机行（1到13）
        if row != 1 or row != 13: # 非首尾行只取改行的首尾列
            col = random.choice([1, row + 6])
        else:
            col = random.randint(1,row + 6)
        self.Map.hexagons[row][col]["e"] += 1
        self.rc = row, col
        sprites.add((screen, self.image))
        return sprites

    def move(self):
        angle = math.degrees(math.atan2(self.rc[0], self.rc[1]))
        if - 150 <= angle < - 90: # 左下
            self.xy[1] += abs(1/60 * self.speed * math.sin(-120))
            self.xy[0] -= abs(1/60 * self.speed * math.cos(-120))
        elif -90 <= angle < -30: # 右下
            self.xy[1] += abs(1/60 * self.speed * math.sin(-60))
            self.xy[0] += abs(1/60 * self.speed * math.cos(-60))
        elif -30 <= angle < 30: # 右
            self.xy[0] += 1/60 * self.speed
        elif 30 <= angle < 90: # 右上
            self.xy[1] -= abs(1/60 * self.speed * math.sin(60))
            self.xy[0] += abs(1/60 * self.speed * math.cos(60))
        elif 90 <= angle < 150: # 左上
            self.xy[1] -= abs(1/60 * self.speed * math.sin(120))
            self.xy[0] -= abs(1/60 * self.speed * math.cos(120))
        elif angle < -150 or angle >= 150: # 左
            self.xy[0] -= 1/60 * self.speed

    def attach(self):
        pass

    def die(self):
        if self.health <= 0:
            self.kill()
            self.Map.hexagons[self.rc[0]][self.rc[1]]['e'] -= 1
