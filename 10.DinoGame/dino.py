from raylib import *
from pyray import *

from settings import *
import os


class Dino:
    def __init__(self):
        self.image = load_image(os.path.join("10.DinoGame", "assets", "dino.png"))
        image_resize(self.image, PLAYER_W, PLAYER_H)
        self.texture = load_texture_from_image(self.image)

        self.velocity_y = 0
        self.pos = Vector2(200, 400)
        self.on_ground = False

    def update(self):
        dt = get_frame_time()

        if is_key_pressed(KEY_SPACE) and self.on_ground:
            self.velocity_y = -JUMP_FORCE
            self.on_ground = False

        self.velocity_y += GRAVITY
        self.pos.y += self.velocity_y * dt

        if self.pos.y + PLAYER_H >= GROUND_Y:
            self.pos.y = GROUND_Y - PLAYER_H
            self.velocity_y = 0
            self.on_ground = True

    def draw(self):
        draw_texture(self.texture, int(self.pos.x), int(self.pos.y), WHITE)
