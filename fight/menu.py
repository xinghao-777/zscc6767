import pygame as pg
import my_sprite
class Menu:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.image_path = image_path
        self.image = pg.image.load(self.image_path)
        self.rect = self.image.get_rect()

class Goldbar(Menu):
    def __init__(self, screen):
        super().__init__(screen, image_path = 'images/bar/goldbar.png')
        self.rect.topleft = (0, 0)
        self.screen.blit(self.image, self.rect)
class Menubar_Tower(Menu):
    def __init__(self, screen):
        super().__init__(screen, image_path = 'images/bar/menubar.png')
        self.rect.topleft = (0, 100)
        self.screen.blit(self.image, self.rect)

class Card:
    def __init__(self, screen):
        self.screen = screen
        self.tower_card_address = ['images/Card_tower/shooter/menu_shooter.png',
                                   'images/Card_tower/golder/menu_golder.png']
        self.tower_card_down_address = ['images/Card_tower/shooter/menu_shooter_down.png',
                                        'images/Card_tower/golder/menu_golder_down.png']
        self.menubar_towers = [my_sprite.Shooter, my_sprite.Golder]

    def card_condition(self, click = None, condition=0):  # 0表示抬起，1表示按压
        if condition == 0:
            for i in range(2): # 图片暂时只有2个，增加后改为range（5）
                self.image = pg.image.load(self.tower_card_address[i])
                self.rect = self.image.get_rect()
                self.rect.topleft = 10, 110 + 100 * i
                self.screen.blit(self.image, self.rect)
        elif condition == 1:
            self.image = pg.image.load(self.tower_card_down_address[click])
            self.rect = self.image.get_rect()
            self.rect.topleft = 10, 110 + 100 * click
            self.screen.blit(self.image, self.rect)

