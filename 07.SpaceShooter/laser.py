from pyray import *
from raylib import *
from settings import *
import os


class Laser:
    def __init__(self, x, y):
        self.image = load_image(os.path.join("07.SpaceShooter", "images", "laser.png"))
        self.texture = load_texture_from_image(self.image)
        self.pos = Vector2(x, y)

    def update(self):
        dt = get_frame_time()
        self.pos.y -= dt * LASER_SPEED

    def draw(self):
        draw_texture(self.texture,int(self.pos.x), int(self.pos.y), WHITE)
