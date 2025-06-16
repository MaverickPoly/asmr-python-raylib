from raylib import *
from pyray import *
from settings import *
from platform_ import Platform

class Player:
    def __init__(self):
        self.rect = Rectangle(WIDTH // 4, HEIGHT // 2, PLAYER_W, PLAYER_H)
        self.on_ground = False
        self.velocity_y = 0

    def update(self, platforms):
        dt = get_frame_time()
        
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        self.rect.y += self.velocity_y
        
        self.on_ground = False
        for platform in platforms:
            if check_collision_recs(self.rect, platform.rect):
                # Landing on platform
                if self.velocity_y > 0 and self.rect.y + self.rect.height - self.velocity_y <= platform.rect.y:
                    self.rect.y = platform.rect.y - self.rect.height
                    self.on_ground = True
                    self.velocity_y = 0
                # Hitting platform from below
                elif self.velocity_y < 0 and self.rect.y - self.velocity_y >= platform.rect.y + platform.rect.height:
                    self.rect.y = platform.rect.y + platform.rect.height
                    self.velocity_y = 0
        
        # Keep player on screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity_y = 0
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.on_ground = True
            self.velocity_y = 0

    def jump(self):
        self.velocity_y = -JUMP_STRENGTH
        self.on_ground = False

    def move_left(self):
        self.rect.x -= PLAYER_SPEED * get_frame_time()

    def move_right(self):
        self.rect.x += PLAYER_SPEED * get_frame_time()

    def draw(self):
        draw_rectangle_rec(self.rect, PLAYER_COLOR)