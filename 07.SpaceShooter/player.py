from pyray import *
from raylib import *
from settings import *
import os


class Player:
    def __init__(self):
        self.image = load_image(os.path.join("07.SpaceShooter", "images", "player.png"))
        self.texture = load_texture_from_image(self.image)
        self.pos = Vector2(WIDTH / 2 - self.texture.width / 2, HEIGHT - 150)
        self.direction = Vector2()

    def movement(self):
        self.direction.x = is_key_down(KEY_RIGHT) - is_key_down(KEY_LEFT)
        self.direction.y = is_key_down(KEY_DOWN) - is_key_down(KEY_UP)

        dt = get_frame_time()

        self.pos.x += self.direction.x * dt * PLAYER_SPEED
        self.pos.y += self.direction.y * dt * PLAYER_SPEED

        # Window Overflow
        if self.pos.x <= 0:
            self.pos.x = 0
        if self.pos.x + self.texture.width >= WIDTH:
            self.pos.x = WIDTH - self.texture.width
        if self.pos.y <= 0:
            self.pos.y = 0
        if self.pos.y + self.texture.height >= HEIGHT:
            self.pos.y = HEIGHT - self.texture.height

    def update(self):
        self.movement()

    def draw(self):
        draw_texture(self.texture, int(self.pos.x), int(self.pos.y), WHITE)