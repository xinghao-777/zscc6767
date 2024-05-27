import pygame as pg
import math
import numpy
import sys

# 常用数据
Q = math.sqrt(3) / 2
HEX_SIZE = 36 # 六边形边长
HEX_SIZE_In = HEX_SIZE * Q # 内接圆半径

# 绘制六边形函数
def draw_hexagon(surface, color, x, y):
    for i in range(6):
        first = (x+math.sin(math.pi*i/3)*HEX_SIZE,y+HEX_SIZE*math.cos(math.pi*i/3))
        end = (x+math.sin(math.pi*(i+1)/3)*HEX_SIZE,y+HEX_SIZE*math.cos(math.pi*(i+1)/3))
        pg.draw.line(surface,color,first,end,1)
# 处理图片,只显示六边形框内内容
def mask_surface(image_address):
    image = pg.image.load(image_address).convert_alpha() # convert_alpha()转化像素格式
    # 图片六边形中心与顶点
    center_x, center_y = image.get_width() // 2, image.get_height() // 2
    vertices = [(center_x + HEX_SIZE * math.sin(i * math.pi / 3),
                 center_y - HEX_SIZE * math.cos(i * math.pi / 3))
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

# 防御设施
class Cards(pg.sprite.Sprite): # 继承父类
    def __init__(self, name, cost, health, damage, production=0, kind=None, image_path=None):
        super().__init__()
        self.name = name
        self.cost = cost
        self.health = health
        self.damage = damage
        self.levelpoint = 1
        self.production = max(production, 0)
        self.image_path = image_path
        self.is_placed = False
        self.kind = kind
    def place(self, game_state, pos, hexagon): # pos为鼠标的位置（元组）
        if game_state >= self.cost:
            self.is_placed = True
            game_state -= self.cost
            target_image = mask_surface(self.image_path) # 返回处理后的图片
            hexagon.card = self.name
            return target_image
        else:
            print("没有足够的资源来放置这个卡牌。")
    def shoot(self, target, bullet):
        if self.damage > 0:
            if target.survive:
                print(f"{self.name} 攻击了 {target.name}，造成了 {self.damage} 点伤害。")
    def hurted(self, damage, hexagon):
        self.health -= damage
        if self.health <= 0:
            self.is_placed = False
            if self.is_placed and self.kind == 'unit':
        # 单位死亡后的逻辑，从Hexagon中移除卡牌
                hexagon.card = None
            print(f"{self.name} 被摧毁了。")
    def up_level(self):
        self.health += 5
        self.damage += 1
        print(f"{self.name} 升级了！")
# 卡牌列表
my_cards = [
    Cards("golder", 10, 10, 0, 5, "A","images/golder.png"),
    Cards("basic_arrow", 20, 10, 2, 0, "B", "images/basic_arrow.png"),
    # ... 添加其他卡牌
]
# 子弹模型
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pg.Surface([5, 10])  # 子弹图像
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.change_x = dx
        self.change_y = dy
    def flying(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
# 敌方
class Enemgy(pg.sprite.Sprite):
    def __init__(self, health, attack, kind = None):
        super().__init__()
        self.health  =health # 血量
        self.attack = attack # 攻击
        self.kind = kind # 类型
        self.survive = 1 # 存活
    def _move_(self):
        if self.kind == 'BOSS':
            pass

# 地图格
class HexagonalMap: # 类在使用时中心点在（7，7），内部储存时为（6，6）
    def __init__(self, hex_size, center_x, center_y, rows, cols, position=None):  # rows,cols为奇数
        self.hex_size = hex_size  # 边长
        self.center_x = center_x  # 中心点坐标
        self.center_y = center_y
        self.card = None
        self.rows = rows  # 行数
        self.cols = cols  # 列数
        self.cols_per_row = [cols - abs(i - (rows - 1) //2 - 1) for i in range(1, self.rows + 1)] # 每行的列数
        self.hexagons = [[{} for _ in range(self.cols_per_row[i])] for i in range(rows)] # 创建二维列表，内含空字典
    def calculate_hex_coords(self, row, col):  # 用于计算给定行和列索引的六边形的中心坐标。
        hex_side = self.hex_size  # 六边形边长
        x = self.center_x  # 防报错
        tar_x = ((row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        if row > 7:
            tar_x = ((14 - row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        x = self.center_x + (col - tar_x) * hex_side * math.sqrt(3)  # 计算六边形中心的x坐标
        y = self.center_y + (row - (self.rows - 1) //2 - 1) * hex_side * 1.5    # 计算六边形中心的y坐标
        return x, y
    def is_valid_position(self, row, col):  # 检查给定的行和列是否在地图范围内
        return 1 <= row < self.rows + 1 and 1 <= col < row + (self.rows - 1) // 2 + 1
    def add_hexagon_data(self, row, col):  # 用字典储存所有格的信息
        if self.is_valid_position(row, col):
            x, y = self.calculate_hex_coords(row, col)
            self.hexagons[row - 1][col - 1] = {'x': x, 'y': y, 'c': self.card}
            if self.card:
                # 假设你有一个集合来跟踪哪些六边形有卡牌
                if not hasattr(self, 'hexagons_with_cards'):
                    self.hexagons_with_cards = set()
                    # 使用行、列或六边形ID作为键（取决于你的需求）
                self.hexagons_with_cards.add((row, col))
    def get_hexagon_coord(self, row, col):  # 返回某行列的六边形的中心点坐标
        if self.is_valid_position(row, col):
            return self.hexagons[row - 1][col - 1]
        return None
    def get_hexagon_rc(self, x, y):  # 返回某中心点坐标的六边形的行列
        if self.hexagons:
            for row in range(1, 8):
                if center_width - (7 - row) * HEX_SIZE * 1.5 == y:
                    for col in range(1, row + 7):
                        tar_x =  ((row + (self.rows - 1) // 2) + 1) / 2
                        if self.center_x + (col - tar_x) * HEX_SIZE * math.sqrt(3) == x:
                            return row,col
            for row in range(6, 0, -1):
                if center_width + (7 - row) * HEX_SIZE * 1.5 == y:
                    for col in range(1, row + 7):
                        tar_x =  ((row + (self.rows - 1) // 2) + 1) / 2
                        if self.center_x + (col - tar_x) * HEX_SIZE * math.sqrt(3) == x:
                            return 14 - row,col
        return None
    def get_hexagons_with_cards(self):
        if not hasattr(self, 'hexagons_with_cards'):
            # 如果 hexagons_with_cards 属性不存在，则返回一个空列表
            return []
            # 如果属性存在，则返回它
        return list(self.hexagons_with_cards)
    def draw(self, surface, color): # 一键绘制地图
        for row in range(self.rows):
            for col in range(self.cols_per_row[row]):
                hexagon = self.get_hexagon_coord(row + 1, col + 1)
                if hexagon:
                    draw_hexagon(surface, color, hexagon['x'], hexagon['y']) # 绘制一个地图格

def find_mouse_position(mouse_pos,map):
    hex_centers = []
    for i in range(1,8):
        for j in range(1, i + 7):
            H = map.get_hexagon_coord(i, j)
            hex_centers.append((H["x"], H["y"]))
    for i in range(6, 0, -1):
        for j in range(1, i + 7):
            H = map.get_hexagon_coord(14 - i, j)
            hex_centers.append((H["x"], H["y"]))
    min_distance = float('inf') # 表示无穷大
    closest_hex = None
    for hex_center in hex_centers:
        distance = ((hex_center[0] - mouse_pos[0]) ** 2 + (hex_center[1] - mouse_pos[1]) ** 2) ** 0.5 # 计算两点的欧几里得距离
        if distance < min_distance:
            min_distance = distance
            closest_hex = hex_center
    return closest_hex

# 初始化pygame
pg.init()
Screen_length = 1400
Screen_width = 800

# 中心点坐标
center_length = Screen_length // 2
center_width = Screen_width // 2

# 设置窗口大小和标题
screen = pg.display.set_mode((Screen_length, Screen_width))
pg.display.set_caption('Honeycomb Fighting')

# 设置颜色
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)  # 定义灰色
RED = (255, 0, 0)

# 创建时钟对象
clock = pg.time.Clock()

# 创建精灵组
image_group = pg.sprite.Group()

game_state = 100 # 资源量

# 游戏主进程
running = True
# 填充背景,在地图前使用，不然覆盖地图
screen.fill(WHITE)
# 初始化地图
hex_map = HexagonalMap(HEX_SIZE, center_length, center_width, 13, 13)
# 填充地图数据
for row in range(hex_map.rows):
    for col in range(hex_map.cols_per_row[row]):
        hex_map.add_hexagon_data(row + 1, col + 1)

while running:
    # 绘制地图
    hex_map.draw(screen, GRAY)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            closest_hex = find_mouse_position(mouse_pos, hex_map)
            print(closest_hex, mouse_pos)
            if closest_hex and game_state >= my_cards[0].cost:
                print(f"{my_cards[0].name}卡牌已放置在{hex_map.get_hexagon_rc(closest_hex[0], closest_hex[1])}")

                # 根据鼠标位置来决定是否放置卡牌
                screen.blit(my_cards[0].place(game_state, mouse_pos, hex_map), (closest_hex[0] - HEX_SIZE * Q, closest_hex[1] - HEX_SIZE)) # 已调用蒙版
                game_state = game_state - my_cards[0].cost
        elif event.type == pg.MOUSEBUTTONUP:
            # 鼠标抬起事件
            pass

    # 凸显中心点
    pg.draw.circle(screen, RED, (int(center_length), int(center_width)), 9, width=0)

    # 控制游戏帧率
    clock.tick(60)

    # 更新显示
    pg.display.flip()

# 退出pygame，循坏外执行
pg.quit()

'''def get_neighbors(grid, pos):
    neighbors = []
    dx, dy = pos
    for nx, ny in [(dx - 1, dy), (dx + 1, dy), (dx - 1, dy - 1), (dx + 1, dy - 1), (dx, dy - 1), (dx, dy + 1)]:
        if (nx, ny) in grid:
            neighbors.append((nx, ny))
    return neighbors

# Dijkstra算法
def dijkstra(grid, start, end):
    distances = {pos: float('infinity') for pos in grid}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_pos = heapq.heappop(queue)

        if current_distance > distances[current_pos]:
            continue

        for neighbor in get_neighbors(grid, current_pos):
            distance = current_distance + 1  # 假设每次移动一个六边形格的距离为1  
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

        if current_pos == end:
            break

            # 构造最短路径（如果需要的话）
    path = []
    current = end
    while current != start:
        path.append(current)
        current = min(get_neighbors(grid, current), key=lambda x: distances.get(x, float('infinity')))
    path.append(start)
    path.reverse()

    return distances[end], path

# 示例地图（使用坐标表示六边形，这里仅示意）
# 注意：实际的六边形网格可能需要一个更复杂的模型来准确表示其连接性  
grid = {
    (0, 0): None,  # 假设这是X的位置  
    (2, 2): None,  # 假设这是A的位置  
    # 其他六边形...  
}

# 设置X和A的位置  
X = (0, 0)
A = (2, 2)

# 调用Dijkstra算法找到最短路径  
distance, path = dijkstra(grid, A, X)

print(f"The shortest distance from A to X is: {distance}")
print(f"The path is: {path}")'''