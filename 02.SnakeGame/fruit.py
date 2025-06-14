from pyray import *
from raylib import *
from settings import *
from random import randint


class Fruit:
    def __init__(self):
        self.pos = Vector2(randint(0, COLS - 1), randint(0, ROWS - 1))

    def draw(self):
        v = Vector2(self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE)
        draw_rectangle_v(v, (GRID_SIZE, GRID_SIZE), RED)
