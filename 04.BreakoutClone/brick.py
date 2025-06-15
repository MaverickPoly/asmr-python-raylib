from pyray import *
from raylib import *
from settings import *

class Brick:
    def __init__(self, x, y, color):
        self.rect = Rectangle(x, y, BRICK_W - PADDING, BRICK_H - PADDING)
        self.color = color

    def draw(self):
        draw_rectangle_rec(self.rect, self.color)
