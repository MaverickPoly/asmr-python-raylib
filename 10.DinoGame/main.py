from raylib import *
from pyray import *

from settings import *
from dino import Dino
from cactus import Cactus

import time


class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, "Google Dino")

        self.dino = Dino()
        self.cactuses: list[Cactus] = []

        self.spawn_duration = 3
        self.current = 0
        self.game_over = False
        self.start_time = time.time()
        self.end_time = 0

    def draw_ground(self):
        draw_line_bezier((0, 600), (WIDTH, 600), 3, BLACK)

    def handle_dino(self):
        self.dino.update()
        self.dino.draw()

    def handle_cactuses(self):
        # Spawn Cactus
        dt = get_frame_time()
        self.current += dt
        if self.current >= self.spawn_duration:
            # Spawn Cactus
            cactus = Cactus()
            self.cactuses.append(cactus)
            self.current = 0

        # Draw Cactuses
        for c in self.cactuses:
            c.update()
            c.draw()

        # Check collision with Dino
        dino_rect = Rectangle(self.dino.pos.x, self.dino.pos.y, self.dino.texture.width, self.dino.texture.height)
        for c in self.cactuses:
            c_rect = Rectangle(c.pos.x, c.pos.y, c.texture.width, c.texture.height)
            if check_collision_recs(dino_rect, c_rect):
                self.game_over = True
                self.end_time = time.time()
        
        # Check if too far left -> Delete
        cactuses = []
        for c in self.cactuses:
            if not c.pos.x <= -100:
                cactuses.append(c)
        self.cactuses = cactuses[:]

    def draw_texts(self):
        score = int((time.time() - self.start_time) * 10)
        draw_text(f"Score: {score}", 10, 10, 48, BLACK)

    def draw_end_screen(self):
        score = int((self.end_time - self.start_time) * 10)
        draw_text("Game over! You lost!", int(WIDTH / 2 - 200), int(HEIGHT / 2 - 50), 48, BLACK)
        draw_text(f"Your score is: {score}!", int(WIDTH / 2 - 200), int(HEIGHT / 2 + 50), 48, BLACK)

    def run(self):
        while not window_should_close():
            begin_drawing()
            clear_background(WHITE)

            if not self.game_over:
                self.draw_ground()
                self.handle_dino()
                self.handle_cactuses()
                self.draw_texts()
            else:
                self.draw_end_screen()

            end_drawing()

        close_window()


if __name__ == "__main__":
    game = Game()
    game.run()