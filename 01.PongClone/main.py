from pyray import *
from raylib import *
import random


WIDTH, HEIGHT = 1500, 850
TITLE = "Pong Game"

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 200
PADDLE_SPEED = 800
PADDLE_COLOR = GRAY

BALL_RADIUS = 20
BALL_COLOR = RED
BALL_SPEED = 700

SCORE_OFFSET = 20


class Paddle:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.direction = Vector2(0, 0)

    def move(self, down, up):
        self.direction.y = is_key_down(down) - is_key_down(up)

        dt = get_frame_time()

        self.rect.y += self.direction.y * PADDLE_SPEED * dt

        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + PADDLE_HEIGHT >= HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT

    def update(self, down, up):
        self.move(down, up)

    def draw(self):
        draw_rectangle_rec(self.rect, PADDLE_COLOR)


class Ball:
    def __init__(self):
        self.center = Vector2(WIDTH // 2, HEIGHT // 2)
        self.direction = Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def scored(self):
        if self.center.x - BALL_RADIUS <= 0:
            return -1 # WENT TO LEFT
        if self.center.x + BALL_RADIUS >= WIDTH:
            return 1  # WENT TO RIGHT
        return 0
    
    def reset(self):
        self.center = Vector2(WIDTH // 2, HEIGHT // 2)
        self.direction = Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def move(self):
        dt = get_frame_time()

        self.center.x += self.direction.x * BALL_SPEED * dt
        self.center.y += self.direction.y * BALL_SPEED * dt

        if self.center.y - BALL_RADIUS <= 0 or self.center.y + BALL_RADIUS >= HEIGHT:
            self.direction.y *= -1

    def check_collision(self, paddle_left: Paddle, paddle_right: Paddle):
        if check_collision_circle_rec(self.center, BALL_RADIUS, paddle_left.rect):
            print("LEFT PADDLE")
            self.direction.x *= -1
        if check_collision_circle_rec(self.center, BALL_RADIUS, paddle_right.rect):
            print("RIGHT PADDLE")
            self.direction.x *= -1
        
    def update(self, paddle_left, paddle_right):
        self.move()
        self.check_collision(paddle_left, paddle_right)

    def draw(self):
        draw_circle_v(self.center, BALL_RADIUS, BALL_COLOR)
    

class Pong:
    def __init__(self):
        init_window(WIDTH, HEIGHT, TITLE)

        self.paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle_right = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        self.left_score = 0
        self.right_score = 0

    def handle_score(self):
        scored_status = self.ball.scored()
        if scored_status == -1: # Right Scored to Left
            self.right_score += 1
            self.ball.reset()
        if scored_status == 1: # Left Scored to Right
            self.left_score += 1
            self.ball.reset()

    def draw_texts(self):
        draw_text(f"Score: {self.left_score}", SCORE_OFFSET, SCORE_OFFSET, 40, WHITE)
        draw_text(f"Score: {self.right_score}", WIDTH - SCORE_OFFSET - 170, SCORE_OFFSET, 40, WHITE)

    def run(self):
        while not window_should_close():
            begin_drawing()
            clear_background(BLACK)

            self.paddle_left.update(KEY_S, KEY_W)
            self.paddle_left.draw()
            self.paddle_right.update(KEY_DOWN, KEY_UP)
            self.paddle_right.draw()

            self.ball.update(self.paddle_left, self.paddle_right)
            self.ball.draw()

            self.handle_score()
            self.draw_texts()


            end_drawing()
        close_window()


if __name__ == "__main__":
    pong = Pong()
    pong.run()
