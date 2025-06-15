from pyray import *
from raylib import *
from settings import *


class Paddle:
    def __init__(self):
        self.rect = Rectangle(WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

    def movement(self):
        direction = is_key_down(KEY_RIGHT) - is_key_down(KEY_LEFT)
        dt = get_frame_time()

        self.rect.x += direction * dt * PADDLE_SPEED

        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x + PADDLE_WIDTH >= WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH

    def update(self):
        self.movement()

    def draw(self):
        draw_rectangle_rec(self.rect, PADDLE_COLOR)