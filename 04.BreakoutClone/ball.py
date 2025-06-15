from pyray import *
from raylib import *
from settings import *
from random import choice

class Ball:
    def __init__(self):
        self.center = Vector2(WIDTH / 2, HEIGHT / 2)
        self.speed = Vector2(choice((-BALL_SPEED, BALL_SPEED)), -BALL_SPEED)

    def bounce(self):
        self.speed.y *= -1

    def update(self):
        dt = get_frame_time()

        self.center.x += dt * self.speed.x
        self.center.y += dt * self.speed.y

        if self.center.x - BALL_RADIUS <= 0 or self.center.x + BALL_RADIUS >= WIDTH:
            self.speed.x *= -1
        if self.center.y - BALL_RADIUS <= 0:
            self.speed.y *= -1

    def draw(self):
        draw_circle_v(self.center, BALL_RADIUS, BALL_COLOR)

