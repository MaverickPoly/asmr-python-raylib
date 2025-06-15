from pyray import *
from raylib import *
from settings import *
import os


class Meteor:
    def __init__(self, x, y, direction, speed, rotation):
        self.image = load_image(os.path.join("07.SpaceShooter", "images", "meteor.png"))
        image_rotate(self.image, rotation)
        self.texture = load_texture_from_image(self.image)
        self.pos = Vector2(x, y)
        self.direction = direction
        self.speed = speed

    def update(self):
        dt = get_frame_time()
        self.pos.x += self.direction.x * dt * self.speed
        self.pos.y += self.direction.y * dt * self.speed

    def draw(self):
        draw_texture(self.texture, int(self.pos.x), int(self.pos.y), WHITE)
