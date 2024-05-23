import pygame as pg
import math
import hexmap
import mask


class Control():
    def __init__(self):
        self.screen = pg.display.get_surface() # 获取当前显示的屏幕
        self.clock = pg.time.Clock() # 时钟
        self.fps = 60 # 帧率
        self.resource = 10 # 默认初始资源为10
        self.keys = None# 鼠标或键盘信号
        self.mouse_pos = None # 鼠标坐标
        # font = pg.font.SysFont("宋体", 12) # 加载系统字体(易bug，别人没有)
        # self.font = font.render(str(self.resource), True, (255,255,255))  # 为资源量的显示，需要blit()绘制
        self.mouse_click = [False, False]  # value:[left mouse click, right mouse click]
        self.current_time = 0.0
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)  # 定义灰色
        self.RED = (255, 0, 0)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed() # 获取键盘所有按键的状态
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()
                self.mouse_click[0], _, self.mouse_click[1] = pg.mouse.get_pressed()
                print('pos:', self.mouse_pos, ' mouse:', self.mouse_click)

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
        print('game over')

    def run(self):
        pg.init()
        # 设置窗口大小和标题 
        Map = hexmap.HexagonalMap()
        screen = pg.display.set_mode((Map.Screen_length, Map.Screen_width))
        pg.display.set_caption('Honeycomb Fighting')
        # 填充背景,在地图前使用，不然覆盖地图
        screen.fill(self.WHITE)
        # 创建实例对象：地图
        Map.star_map()
        running = True
        while running:
            # 绘制地图
            Map.draw(screen, self.GRAY)
            # 凸显中心点
            pg.draw.circle(screen, self.RED, (int(Map.Screen_length // 2), int(Map.Screen_width // 2)), 9, width=0)
            # 控制帧率
            self.clock.tick(self.fps)

            # 退出信号
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            # 更新显示
            pg.display.flip()
        pg.quit()