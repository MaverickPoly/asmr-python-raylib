from raylib import *
from pyray import *
from settings import *
from player import Player
from platform_ import Platform

class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, TITLE)
        set_target_fps(60)

        self.player = Player()
        self.platforms = []
        self.create_platforms()

    def create_platforms(self):
        # Ground
        self.platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))

        # Platforms
        self.platforms.append(Platform(200, 500, 400, 20))
        self.platforms.append(Platform(700, 400, 200, 20))
        self.platforms.append(Platform(300, 300, 300, 20))
        self.platforms.append(Platform(800, 200, 400, 20))

    def handle_input(self):
        if is_key_pressed(KEY_SPACE) and self.player.on_ground:
            self.player.jump()

        if is_key_down(KEY_LEFT):
            self.player.move_left()
        if is_key_down(KEY_RIGHT):
            self.player.move_right()

    def run(self):
        while not window_should_close():
            self.handle_input()
            self.player.update(self.platforms)

            begin_drawing()
            clear_background(BLACK)
            
            for platform in self.platforms:
                platform.draw()
            
            self.player.draw()
            
            # Display controls
            draw_text("Arrow keys to move, Space to jump", 10, 10, 20, WHITE)
            draw_text(f"Velocity Y: {self.player.velocity_y:.1f}", 10, 40, 20, WHITE)
            draw_text(f"On Ground: {self.player.on_ground}", 10, 70, 20, WHITE)
            
            end_drawing()

        close_window()

if __name__ == "__main__":
    game = Game()
    game.run()