import pygame as pg
import hexmap
import menu
import my_sprite
import time
class Control():
    def __init__(self):
        self.clock = pg.time.Clock() # 时钟
        self.fps = 60 # 帧率
        self.resource = 10 # 默认初始资源为10
        self.keys = None# 鼠标或键盘信号
        self.mouse_pos = 0,0 # 左键按下时鼠标坐标
        self.font = pg.font.Font("fonts\my_font.ttf", 32) # 设置字体
        self.Screen_width = 1600
        self.Screen_height = 1000
        self.current_time = time.time() # 初始时间
        self.done = False # 主循环的控制
        # 颜色
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)  # 定义灰色
        # 创建实例对象：地图
        self.Map = hexmap.HexagonalMap(self.Screen_width, self.Screen_height)
        # 窗口属性
        self.screen = pg.display.set_mode((self.Screen_width, self.Screen_height))
        # 填充背景,在地图前使用，不然覆盖地图
        self.screen.fill(self.WHITE)
        # 绘制地图边界并为每一个格添加数据并绘制图像
        self.Map.star_map(self.screen, self.GRAY)
        self.list_of_tower=[]
        self.number_of_tower=-1

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

    def menu_choose(self): # 菜单栏选择塔，默认在屏幕最左面居中，每个卡槽占据一个矩形，高为屏幕高的3/20，宽是屏幕高的1/10，共五个卡槽
        card_height = self.Screen_height * 3/20
        card_width = self.Screen_height / 10
        if 0 <= self.mouse_pos[0] <= card_width: # 先判断鼠标的x是否在菜单的宽度内
            for i in range(5): # 从上往下依次确定哪张card
                if self.Screen_height / 10 + card_height * i <= self.mouse_pos[1] < self.Screen_height / 10 + card_height * (i + 1):
                    click = i  # 记录点击区域
                    cards = menu.Card(self.screen)
                    cards.card_condition(click, 1) # 改变卡片状态

    def creat_tower(self):
        i=self.menu_choose()
        tower=self.Map.munubar_tower_list[i](self.Map,self.mouse_pos)
        self.list_of_tower.append(tower)
        self.number_of_tower += 1
        tower.place(self, self.resource,self.mouse_pos,self.screen,self.number_of_tower)


    def run(self):
        #self.Map.create_menubar(self, self.screen)
        # 屏幕名
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
        # 凸显中心点
        pg.draw.circle(self.screen, (255, 0, 0), (int(self.Map.Screen_width // 2), int(self.Map.Screen_height // 2)), 9, width=0)
        # 总精灵组
        all_sprites = pg.sprite.Group()
        '''# 加载精灵
        my_sprite = my_sprite.MySprite(screen, 'path_to_your_image.png')
        all_sprites.add(my_sprite)'''
        while not self.done:
            # 获取时间
            self.current_time = time.time()
            # 绘制屏幕左边
            menu.Goldbar(self.screen)
            menu.Menubar_Tower(self.screen)
            menu.Card(self.screen).card_condition()
            # 显示资源数量
            self.text = self.font.render(str(self.resource), True, (0, 0, 0))  # 为资源量的显示，需要blit()绘制，文本不会随时变化，需要在循环里
            self.screen.blit(self.text, (90, 22)) # goldbar里的白板左顶点为（85，10），考虑白板的阴影，dest为（90，20）
            # 屏幕事件获取
            self.event_loop()
            self.menu_choose()
            # 更新所有精灵的状态
            all_sprites.update()
            # 精灵的渲染和显示
            all_sprites.draw(self.screen)
            # 更新显示
            pg.display.update()
            # 控制帧率
            self.clock.tick(self.fps)
        pg.quit()
