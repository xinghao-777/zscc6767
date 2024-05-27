import pygame as pg
import math
# 地图格
class HexagonalMap(): # 类在使用时中心点在（7，7），内部储存时为（6，6）
    def __init__(self, screen_length, screen_width):  # rows,cols为奇数
        self.HEX_SIZE = 36  # 外接圆半径
        self.HEX_SIZE_In = self.HEX_SIZE * math.sqrt(3) / 2  # 内接圆半径
        self.Screen_length = screen_length
        self.Screen_width = screen_width
        self.card_exist = None
        self.enemgy_exist = None
        self.rows = 15  # 行数
        self.cols = 15  # 列数
        self.cols_per_row = [self.cols - abs(i - (self.rows - 1) //2 - 1) for i in range(1, self.rows + 1)] # 每行的列数
        self.hexagons = [[{} for _ in range(self.cols_per_row[i])] for i in range(self.rows)] # 创建二维列表，内含空字典

    def calculate_hex_xy(self, row, col):  # 用于计算给定行和列索引的六边形的中心坐标。
        hex_side = self.HEX_SIZE  # 六边形边长
        x = self.Screen_length // 2  # 防报错
        tar_x = ((row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        if row > 7:
            tar_x = ((16 - row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        x = self.Screen_length // 2 + (col - tar_x) * hex_side * math.sqrt(3)  # 计算六边形中心的x坐标
        y = self.Screen_width // 2 + (row - (self.rows - 1) //2 - 1) * hex_side * 1.5    # 计算六边形中心的y坐标
        return x, y

    def calculate_hex_rc(self, row, col): # 用于计算给定行和列索引的六边形的以中心点为（0，0）分布的坐标。
        r = row - (self.rows + 1) // 2
        c = ((col - 1/2) - ((self.rows - 1) // 2 + row) / 2) * 2
        return r, int(c)

    def is_valid_position(self, row, col):  # 检查给定的行和列是否在地图范围内
        return 1 <= row < self.rows + 1 and 1 <= col < row + (self.rows - 1) // 2 + 1

    def add_hexagon_data(self, row, col):  # 用字典储存所有格的信息(x,y:像素坐标；c:什么踏；e:什么敌人)
        if self.is_valid_position(row, col):
            x, y = self.calculate_hex_xy(row, col)
            r, c = self.calculate_hex_rc(row, col)
            self.hexagons[row - 1][col - 1] = {'xy': (x, y), 'rc': (r, c), 'c': None, 'e': None} # 默认初始地图格数据

    def get_hexagon_coord(self, row, col):  # 返回某行列的六边形的中心点坐标
        if self.is_valid_position(row, col):
            return self.hexagons[row - 1][col - 1]
        return None

    def get_hexagon_rc(self, x, y):  # 返回某中心点坐标的六边形的行列
        if self.hexagons:
            for row in range(1, self.rows + 1):
                if self.Screen_width // 2 - ((self.rows + 1) // 2 - row) * self.HEX_SIZE * 1.5 == y:
                    for col in range(1, self.cols_per_row[row] + 1):
                        tar_x =  ((row + (self.rows - 1) // 2) + 1) / 2
                        if self.Screen_length // 2 + (col - tar_x) * self.HEX_SIZE * math.sqrt(3) == x:
                            return row,col
        return None

    def get_closest_hexagon_rc(self, mouse_pos): # 返回离鼠标点最近的格子的行列
        hex_centers = []
        for i in range(1, (self.rows + 1) // 2 + 1):
            for j in range(1, self.cols_per_row[i] + 1):
                H = self.get_hexagon_coord(i, j)
                hex_centers.append(H["xy"])
        min_distance = float('inf')  # 表示无穷大
        closest_hex = None
        for hex_center in hex_centers:
            distance = ((hex_center[0] - mouse_pos[0]) ** 2 + (hex_center[1] - mouse_pos[1]) ** 2) ** 0.5  # 计算两点的欧几里得距离
            if distance < min_distance:
                min_distance = distance
                closest_hex = hex_center
        return closest_hex

    def draw_hexagon(self, surface, color, xy): # 绘制六边形函数
        for i in range(6):
            first = (xy[0] + math.sin(math.pi * i / 3) * self.HEX_SIZE, xy[1] + self.HEX_SIZE * math.cos(math.pi * i / 3))
            end = (xy[0] + math.sin(math.pi * (i + 1) / 3) * self.HEX_SIZE, xy[1] + self.HEX_SIZE * math.cos(math.pi * (i + 1) / 3))
            pg.draw.line(surface, color, first, end, 1)

    def star_map(self, screen, color):
        # 填充地图数据
        for row in range(self.rows):
            for col in range(self.cols_per_row[row]):
               self.add_hexagon_data(row + 1, col + 1)
        for row in range(self.rows):
            for col in range(self.cols_per_row[row]):
                coord = self.hexagons[row][col]["xy"]
                if coord:
                    self.draw_hexagon(screen, color, coord) # 绘制一个地图格