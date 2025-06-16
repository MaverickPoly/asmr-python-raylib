from raylib import *
from pyray import *

from settings import *


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rectangle(x, y, width, height)

    def draw(self):
        draw_rectangle_rec(self.rect, PLATFORM_COLOR)
