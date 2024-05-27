import pygame as pg
import math
class HexagonMap():
    def __init__(self, center_xy, radius, level = 0):
        self.center_xy = center_xy
        self.radius = radius
        self.radius_inside  =radius * math.sqrt(3) * 2
        self.level = 0
        self.children = [None for _ in range(6)]
        self.date = {"c": None, "e": None}
    def add_child(self, index, xy):
        if 0 <= index < 6:
            self.children[index]

