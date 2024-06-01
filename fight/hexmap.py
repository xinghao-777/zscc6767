import pygame as pg
import math

import my_sprite


# 地图格
class HexagonalMap(): # 类在使用时中心点在（7，7），内部储存时为（6，6）
    def __init__(self, Screen_width, Screen_height):  # rows,cols为奇数
        self.HEX_SIZE = 36  # 外接圆半径
        self.HEX_SIZE_In = self.HEX_SIZE * math.sqrt(3) / 2  # 内接圆半径
        self.Screen_width = Screen_width
        self.Screen_height = Screen_height
        self.card_exist = None # 格上有多少塔
        self.enemgy_exist = None # 格上有多少敌人
        self.rows = 15  # 行数
        self.cols = 15  # 列数
        self.cols_per_row = [self.cols - abs(i - (self.rows - 1) //2 - 1) for i in range(1, self.rows + 1)] # 每行的列数
        self.hexagons = [[{} for _ in range(self.cols_per_row[i])] for i in range(self.rows)] # 创建二维列表，内含空字典
        self.vertexs = None  # 地图的近六边形形状的六个顶点，检测鼠标点是否在地图内所用
        self.create_vertexs()  # 更新self.vertexs

    def create_vertexs(self): # 创建地图的近六边形形状的六个顶点，用于判断地图的边界
        need_side = ((self.rows - 1) // 2 * 2 + 1 + 1 / 3) * self.HEX_SIZE_In
        vertex_list = []
        for i in range(6):
            angle = 30 + 60 * i
            x = self.Screen_width // 2 + math.sin(angle) * need_side
            y = self.Screen_height // 2 - math.cos(angle) * need_side
            vertex_list.append((x, y))
        self.vertexs = vertex_list

    def calculate_hex_xy(self, row, col):  # 用于计算给定行和列索引的六边形的中心坐标。
        hex_side = self.HEX_SIZE  # 六边形边长
        x = self.Screen_width // 2  # 防报错
        tar_x = ((row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        if row > 7:
            tar_x = ((16 - row + (self.rows - 1) // 2) + 1) / 2  # 每行的对称轴所在
        x = self.Screen_width // 2 + (col - tar_x) * hex_side * math.sqrt(3)  # 计算六边形中心的x坐标
        y = self.Screen_height // 2 + (row - (self.rows - 1) //2 - 1) * hex_side * 1.5    # 计算六边形中心的y坐标
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
                if self.Screen_height // 2 - ((self.rows + 1) // 2 - row) * self.HEX_SIZE * 1.5 == y:
                    for col in range(1, self.cols_per_row[row] + 1):
                        tar_x =  ((row + (self.rows - 1) // 2) + 1) / 2
                        if self.Screen_width // 2 + (col - tar_x) * self.HEX_SIZE * math.sqrt(3) == x:
                            return row,col
        return None

    def get_closest_hexagon_rc(self, mouse_pos): # 返回离鼠标点最近的格子的行列
        if self.check_in_map(mouse_pos):
            x1, x2 = self.Screen_width // 2, self.Screen_width // 2
            y1, y2 = self.Screen_height // 2, self.Screen_height // 2
            rc = self.get_hexagon_rc(x2, y2)
            while self.is_valid_position(rc[0], rc[1]):
                angle = math.degrees(math.atan2(mouse_pos[0] - x2, mouse_pos[1] - y2))
                for i in range(6):
                    if 90 - 60 * i <= angle < 30 - 60 * i:
                        if i < 3:
                            x2 += self.HEX_SIZE_In * (1 + i % 2)  # i=1时双倍
                            y2 += self.HEX_SIZE * 1.5 * (i - 1)
                        else:
                            x2 -= self.HEX_SIZE_In * (1 + (i % 2 + 1) % 2)  # i=4时双倍
                            y2 += self.HEX_SIZE * 1.5 * (i - 4)
                last_distance = ((mouse_pos[0] - x1) ** 2 + (mouse_pos[1] - y1) ** 2) ** 1 / 2
                distance = ((mouse_pos[0] - x2) ** 2 + (mouse_pos[1] - y2) ** 2) ** 1 / 2
                if last_distance <= distance:
                    return self.get_hexagon_rc(x1, y1)
                rc = self.get_hexagon_rc(x2, y2)
                if not rc:
                    return self.get_hexagon_rc(x1, y1)
                else:
                    x1, y1 = x2, y2

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

    def check_in_map(self, mouse_pos): # 检测鼠标点（x,y）是否在地图外
        px, py = mouse_pos
        is_in = False
        for i, corner in enumerate(self.vertexs): # 默认鼠标点击点向右发射射线，看与地图的六条边的交点数
            next_i = i + 1 if i + 1 < len(self.vertexs) else 0
            x1, y1 = corner
            x2, y2 = self.vertexs[next_i]
            if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
                is_in = True
                break
            if py == y1 and py == y2:
                if min(x1, x2) < px < max(x1, x2):
                    is_in = True
                    break
            if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
                x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                if x == px:  # if point is on edge
                    is_in = True
                    break
                elif x > px:  # if point is on left-side of line
                    is_in = not is_in
            return is_in
    def creat_menubar(self,surface):
        for i in range(4):
            surface.blit(self.munubar_image_address[i],(0,300+i*75))
