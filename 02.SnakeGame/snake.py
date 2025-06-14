from pyray import *
from raylib import *
from settings import *
import time


RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)

class Snake:
    def __init__(self):
        self.body = [Vector2(11, 10), Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(1, 0)
        self.count = time.time()

    def grow(self):
        last = self.body[-1]
        val = Vector2(last.x + self.direction.x, last.y + self.direction.y)
        self.body.append(val)

    def move(self):
        current = time.time()
        if current - self.count >= SNAKE_MOVE_DELAY:
            new_body = self.body[:-1]
            head = Vector2(self.body[0].x + self.direction.x, self.body[0].y + self.direction.y)
            new_body.insert(0, head)
            self.body = new_body[:]
            self.count = current
    
    def handle_input(self):
        if is_key_pressed(KEY_RIGHT) and self.direction != LEFT:
            self.direction = RIGHT
        if is_key_pressed(KEY_LEFT) and self.direction != RIGHT:
            self.direction = LEFT
        if is_key_pressed(KEY_UP) and self.direction != DOWN:
            self.direction = UP
        if is_key_pressed(KEY_DOWN) and self.direction != UP:
            self.direction = DOWN

    def is_lost(self):
        head = self.body[0]
        if head.x < 0 or head.x >= COLS \
            or head.y < 0 or head.y >= ROWS:
            return True
        
        for part in self.body[1:]:
            if part.x == head.x and part.y == head.y:
                return True

        return False

    def update(self):
        self.move()
        self.handle_input()

    def draw(self):
        for part in self.body:
            v = Vector2(part.x * GRID_SIZE, part.y * GRID_SIZE)
            draw_rectangle_v(v, (GRID_SIZE, GRID_SIZE), BLUE)
