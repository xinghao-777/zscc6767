import math
import pygame as pg
import random


# 塔精灵
class Tower(pg.sprite.Sprite):  # 继承父类
    def __init__(self, Map, fps, pos): # 有bug，pos在place时使用
        super().__init__()
        self.Map = Map  # 接受地图实例
        self.fps = fps
        self.xy = None # 未放之前无xy坐标
        self.rc = None  # 未放之前无行列坐标
        self.levelpoint = 1  # 等级点数
        self.levels = 1  # 初始等级
        self.cost = None  # 留给下级继承
        self.health = None  # 留给下级继承
        self.damage = None  # 留给下级继承(当前血量)
        self.max_health = None  # 留给下级继承(初始血量)
        self.image = None # 留给下级继承
        self.rect = None # 留给下级继承

    def place(self, game_state, pos, surface):  # 放置塔数据在地图格上（pos为鼠标的位置（元组））
        if game_state >= self.cost:
            self.rc = self.Map.get_closest_hexagon_rc(self, pos)  # 获取当前鼠标点的行列
            if not self.Map.hexagons[self.rc[0]][self.rc[1]]["c"]:
                game_state -= self.cost
                self.xy = self.Map.hexagons[self.rc[0]][self.rc[1]]["xy"] # 根据行列坐标创建实际坐标
                self.Map.hexagons[self.rc[0]][self.rc[1]]["c"] = 1  # 更改hex_map的属性，表示该格有牌
                surface.blit(self.image,(self.xy[0]-self.Map.HEX_SIZE,self.xy[1]-self.Map.HEX_SIZE_In))
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
                self.health = self.max_health # 回复满血
                if self.damage:
                    self.damage += 2
                self.levelpoint = 0
                self.levels += 1

    def updata(self, updata):
        if self.health <= 0:
            self.destroy()
        self.up_level()


class Shooter(Tower):
    def __init__(self, Map, fps = 60, pos = (0, 0)):
        super().__init__(Map, fps, pos)  # 传递必要的参数给父类
        # Shooter 特有的属性初始化
        self.cost = 10
        self.health = 10
        self.max_health = self.health # 用于回复血量
        self.damage = 2 # 伤害
        self.shoot_rate = 1 # 攻速
        self.shoot_direction = 90 # 攻击方向，默认朝右（竖直向上为0）
        self.shoot_distance = 4 # 攻击距离,格为单位
        # 精灵属性
        self.image_path="images/Card_tower/shooter/shooter.png"
        self.image = pg.image.load(self.image_path)
        if self.xy is not None:  # 确保pos不是None
            self.xy[0] -= self.Map.HEX_SIZE_In
            self.xy[1] -= self.Map.HEX_SIZE
        self.rect = self.image.get_rect(topleft=self.xy)
        # 子弹的精灵组
        self.bullet_group = pg.sprite.Group()

    def set_shoot_distance(self, distance):
        if distance is not None:
            self.shoot_distance = distance
    def set_shoot_rate(self, rate):
        if rate is not None:
            self.shoot_rate = rate
    def set_shoot_direction(self, direction):
        if direction is not None:
            self.shoot_distance = direction
    def rotate(self): # 旋转，默认顺时针60°
        self.shoot_direction += 60

    def shoot(self, Shooter_bullet):
        rc = self.rc # 储存当前行列
        xy = self.xy # 储存当前xy坐标
        d = 0 # 计算距离
        n = self.shoot_rate * self.fps - 1# 计算攻速
        if self.damage > 0: # 能攻击
            while True:
                if (not self.Map.is_valid_position(rc[0], rc[1])) and d > self.shoot_distance: # 遍历的格是否在地图内 and 敌人是否在攻击范围里
                    break
                xy[0] += math.sin(self.shoot_direction) * 2 * self.Map.HEX_SIZE_In
                xy[1] -= math.cos(self.shoot_direction) * 2 * self.Map.HEX_SIZE_In
                d += 1
                n += 1
                rc = self.Map.get_hexagon_rc(xy[0], xy[1])
                if self.Map.hexagons[rc[0]][rc[1]]['e'] and n == self.fps * self.shoot_rate: # 有怪且满足攻击间隔，
                    bullet = Shooter_bullet(self.xy, self.Map, self.shoot_direction, self.damage)  # 创建子弹实例,bullet只是临时变量名，若要访问它，在group里遍历得到指定bullet
                    self.bullet_group.add(bullet)
                    n = 0

class Golder(Tower):
    def __init__(self, Map, fps = 60, pos=(0, 0)):
        super().__init__(Map, fps, pos)  # 传递必要的参数给父类
        self.cost = 10
        self.health = 10
        self.product_rate = 5 # 每隔多少秒产生$
        self.max_health = self.health
        self.last_product_time = 0  # 上次产生资源的时间
        # 精灵属性
        self.image_path = "images/Card_tower/golder/golder.png"
        self.image = pg.image.load(self.image_path)
        if self.xy is not None:  # 确保pos不是None
            self.xy[0] -= self.Map.HEX_SIZE_In
            self.xy[1] -= self.Map.HEX_SIZE
        self.rect = self.image.get_rect(topleft=self.xy)

    def product(self, game_state, current_time):
        # 如果当前时间与上次产生资源的时间之差大于或等于生产速率
        if current_time - self.last_product_time >= self.product_rate:
            # 产生资源
            game_state += 5  # 每次加5$
            # 更新上次产生资源的时间
            self.last_product_time = current_time
            return game_state
class Shooter_bullet(pg.sprite.Sprite):
    def __init__(self, xy, Map, direction, damage = None):
        super().__init__()
        self.Map = Map
        self.direction = direction  # 攻击方向，用角度表示，当竖直向上为0，顺时针增大
        self.damage = damage  # 威力
        # shooter的子弹精灵属性
        self.image_path = "images/Card_tower/shooter/shoot_arrow.png"
        self.image = pg.image.load(self.image_path)
        if xy is not None:
            xy[0] -= self.Map.HEX_SIZE_In
            xy[1] -= self.Map.HEX_SIZE
        self.rect = self.image.get_rect(topleft=xy)  # 图片以左上角点为图片放置参考点
        self.rect.x = xy[0]
        self.rect.y = xy[1]
        self.speed = 2 * self.Map.HEX_SIZE_In  # 每秒移动2个格的距离
    def updata(self, screen):
        self.rect.x += math.sin(self.direction) * 2 * self.Map.HEX_SIZE_In
        self.rect.y -= math.cos(self.direction) * 2 * self.Map.HEX_SIZE_In
        # 检查子弹是否移出屏幕，如果是，移除
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

# 敌方
class Basic_enemgy(pg.sprite.Sprite):
    def __init__(self, Map, pos = None, image_path = None):
        super().__init__()
        self.Map = Map  # 获取地图实例
        self.health = 20  # 血量
        self.attack = 10  # 攻击
        self.speed = self.Map.HEX_SIZE_In * 2  # 速度,每秒多少格
        self.image = pg.image.load(image_path) if image_path else None
        self.rect = self.image.get_rect(topleft=pos) if self.image else None
        self.create()  # 调用本体方法，生成初始位置
        self.xy = Map.hexagons[self.rc[0]][self.rc[1]]["xy"]

    def create(self):
        # 只在外圈生成敌人
        list = [_ for _ in range(1,self.Map.rows + 1)]
        row = random.choices(list, weights=[7,2,2,2,2,2,2,2,2,2,2,7])[0] # 随机行（1到13）
        if row != 1 or row != 13: # 非首尾行只取改行的首尾列
            col = random.choice([1, self.Map.cols_per_row[row-1]])
        else:
            col = random.randint(1,self.Map.cols_per_row[row-1])
        self.Map.hexagons[row][col]["e"] += 1
        self.rc = row, col

    def move(self):
        angle = math.degrees(math.atan2(self.rc[0], self.rc[1]))
        for i in range(6):
            if 90 - 60 * i <= angle < 30 - 60 * i:
                if i < 3:
                    if i != 1:
                        self.xy[0] += self.speed / 60 * abs(math.cos(60 - 60 * i))
                        self.xy[1] += self.speed / 60 * (i - 1) * abs(math.sin(60 - 60 * i))
                    else:
                        self.xy[0] += self.speed / 60 * 2 * abs(math.cos(60 - 60 * i))
                else:
                    if i != 4:
                        self.xy[0] -= self.speed / 60 * abs(math.cos(60 - 60 * i))
                        self.xy[1] -= self.speed / 60 * (i - 4) * abs(math.sin(60 - 60 * i))
                    else:
                        self.xy[0] -= self.speed / 60 * 2 * abs(math.cos(60 - 60 * i))
        if self.Map.get_closest_hexagon_rc(self.xy) != self.rc:
            self.Map.hexagons[self.rc[0]][self.rc[1]]["e"] -= 1 # 先删除之前格的标记
            self.rc = self.Map.get_closest_hexagon_rc(self.xy) # 根据xy坐标每次更新自己行列所在格
            self.Map.hexagons[self.rc[0]][self.rc[1]]["e"] += 1 # 后增加当前格的标记

    def attach(self):
        pass

    def die(self):
        if self.health <= 0:
            self.kill()
            self.Map.hexagons[self.rc[0]][self.rc[1]]['e'] -= 1

