import pygame as pg
import math
import hexmap
import mask


class Control():
    def __init__(self):
        self.clock = pg.time.Clock() # 时钟
        self.fps = 60 # 帧率
        self.resource = 10 # 默认初始资源为10
        self.keys = None# 鼠标或键盘信号
        self.mouse_pos = None # 鼠标坐标
        font = pg.font.Font("fonts\my_font.ttf", 20) # 设置字体(易bug，别人没有)
        self.font = font.render(str(self.resource), True, (255,255,255))  # 为资源量的显示，需要blit()绘制
        self.mouse_click = [False, False]  # value:[left mouse click, right mouse click]
        self.current_time = 0.0
        self.done = False
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)  # 定义灰色
        self.RED = (255, 0, 0)

# pygame.key.get_pressed()
# 返回一个元组，表示当前所有键盘按键的状态（按下或未按下）,可以通过检查元组中的特定键位来确定哪个键被按下。
# 这种方法对于需要持续监听按键状态的情况很有用，比如实现角色的持续移动。

# pygame.event.MOUSEBUTTONDOWN
# 鼠标键按下事件
# event.pos
# 相对于窗口左上角，鼠标的当前坐标值(x, y)
# event.button
# 鼠标按下键编号（整数），左键为1，按下滚动轮2、右键为3，向前滚动滑轮4、向后滚动滑轮5

    def event_loop(self):#捕捉鼠标信息
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()

            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed() # 获取键盘所有按键的状态
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def menu_choose(self): # 菜单栏选择塔，默认在屏幕最下面居中，每个卡槽占据一个正方形，边长为屏幕高的15/100，共四个卡槽
        per_menu_side = self.Screen_width * 15/100
        if self.Screen_width - per_menu_side <= self.mouse_pos[1] <= self.Screen_width:
            if self.Screen_length // 2 - per_menu_side * 2 <= self.mouse_pos[0] <= self.Screen_length // 2 + per_menu_side * 2:
                for i in range(4):
                    if self.Screen_length // 2 + (i - 2) * per_menu_side <= self.mouse_pos[0] <= self.Screen_length // 2 + (i - 1) * per_menu_side:
                        pass

    def run(self):
        # 设置窗口大小和标题 
        Map = hexmap.HexagonalMap()
        self.screen = pg.display.set_mode((Map.Screen_length, Map.Screen_width))
        self.Screen_length = Map.Screen_length
        self.Screen_width = Map.Screen_width
        pg.display.set_caption('Honeycomb Fighting')
        # 加载背景音乐
        pg.mixer.music.load("music/my_like.mp3")
        pg.mixer.music.set_volume(0.5)
        # 循环播放 (重复次数:-1表示无限重复,开始时间)
        pg.mixer.music.play(-1, 0)
        # 暂停
        #pg.mixer.music.pause()
        # 停止
        #pg.mixer.music.stop()

        # 填充背景,在地图前使用，不然覆盖地图
        self.screen.fill(self.WHITE)
        # 凸显中心点
        pg.draw.circle(self.screen, self.RED, (int(Map.Screen_length // 2), int(Map.Screen_width // 2)), 9, width=0)
        # 创建实例对象：地图
        Map.star_map(self.screen, self.GRAY)
        # 总精灵组
        all_sprites = pg.sprite.Group()

        '''# 加载精灵
        my_sprite = my_sprite.MySprite(screen, 'path_to_your_image.png')
        all_sprites.add(my_sprite)'''

        while not self.done:
            self.event_loop()
            # 显示资源数量
            self.screen.blit(self.font, (0, 0))
            # 更新所有精灵的状态
            all_sprites.update()
            # 精灵的渲染和显示



            # 更新显示
            pg.display.update()
            # 控制帧率
            self.clock.tick(self.fps)
        pg.quit()