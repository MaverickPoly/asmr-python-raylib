from raylib import *
from pyray import *

from settings import *
import os
import random

class Cactus:
    def __init__(self):
        self.image = load_image(os.path.join("10.DinoGame", "assets", "cactus.png"))
        image_resize(self.image, CACTUS_W, CACTUS_H)
        self.texture = load_texture_from_image(self.image)
        self.pos = Vector2(random.randint(WIDTH + 20, WIDTH + 100), GROUND_Y - CACTUS_H)

    def update(self):
        dt = get_frame_time()
        # Move to right
        self.pos.x -= CACTUS_SPEED * dt

    def draw(self):
        draw_texture(self.texture, int(self.pos.x), int(self.pos.y), WHITE)
