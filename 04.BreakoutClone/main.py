from pyray import *
from raylib import *
from settings import *
from paddle import Paddle
from brick import Brick
from ball import Ball

import math


class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, "Breakout")

        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks: list[Brick] = []
        self.generate_bricks()

        self.score = 0
        self.lives = 3
        self.game_over = False

    def generate_bricks(self):
        for row in range(BRICKS_ROWS):
            for col in range(BRICK_COLS):
                x, y = col * BRICK_W, row * BRICK_H + TOP_OFFSET
                color = COLORS[row % BRICKS_ROWS]
                self.bricks.append(Brick(x, y, color))

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw()

    def reset(self):
        self.ball = Ball()
        self.bricks = []
        self.generate_bricks()
        self.paddle = Paddle()
        self.score = 0
        self.lives = 3
        self.game_over = False

    def check_collisions(self):
        # Ball with Bricks
        bricks_copy: list[Brick] = []
        for brick in self.bricks:
            if check_collision_circle_rec(self.ball.center, BALL_RADIUS, brick.rect):
                self.ball.bounce()
                self.score += 1
            else:
                bricks_copy.append(brick)
        self.bricks = bricks_copy[:]

        # Ball with paddle
        if check_collision_circle_rec(self.ball.center, BALL_RADIUS, self.paddle.rect):
            relative_x = (self.ball.center.x - (self.paddle.rect.x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
            speed_magnitude = math.sqrt(self.ball.speed.x**2 + self.ball.speed.y**2)
            self.ball.speed.x = relative_x * speed_magnitude
            self.ball.bounce()

        # Ball Moves Downsides
        if self.ball.center.y + BALL_RADIUS >= HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.ball = Ball()
            self.paddle = Paddle()

        # Win state
        if len(self.bricks) == 0:
            self.game_over = True

    def draw_end_screen(self):
        if self.lives > 0:
            draw_text("Game over! Press Spacebar to restart!", WIDTH // 2 - 400, HEIGHT // 2 - 300, 32, WHITE)
        else:
            draw_text("You won! Press Spacebar to restart!", WIDTH // 2 - 400, HEIGHT // 2 - 300, 32, WHITE)
        if is_key_pressed(KEY_SPACE):
            self.game_over = False
            self.reset()

    def draw_texts(self):
        draw_text(f"Score: {self.score}", 10, 10, 40, WHITE)
        draw_text(f"Lives: {self.lives}", WIDTH - 200, 10, 40, WHITE)

    def run(self):
        while not window_should_close():
            begin_drawing()

            clear_background(BLACK)

            if self.game_over:
                self.draw_end_screen()
            else:
                self.paddle.update()
                self.paddle.draw()

                self.ball.update()
                self.ball.draw()
                
                self.draw_bricks()
                self.check_collisions()

                self.draw_texts()

            end_drawing()
        close_window()


if __name__ == "__main__":
    game = Game()
    game.run()
