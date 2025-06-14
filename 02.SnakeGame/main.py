from pyray import *
from raylib import *
from settings import *
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, TITLE)

        self.snake = Snake()
        self.fruit = Fruit()

        self.score = 0

    def draw_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                x, y = row * GRID_SIZE, col * GRID_SIZE
                c = row + col
                color = color_brightness(GREEN, -0.2) if c % 2 == 0 else color_brightness(GREEN, -0.3)
                draw_rectangle(x, y, GRID_SIZE, GRID_SIZE, color)

    def check_eat(self):
        head = self.snake.body[0]
        if head.x == self.fruit.pos.x and head.y == self.fruit.pos.y:
            self.fruit = Fruit()
            self.score += 1
            self.snake.grow()
    
    def draw_texts(self):
        draw_text(f"Score: {self.score}", 10, HEIGHT - 40, 40, WHITE)

    def run(self):
        while not window_should_close():
            begin_drawing()

            clear_background(BLACK)

            self.draw_bg()

            self.snake.update()
            self.snake.draw()
            is_lost = self.snake.is_lost()
            if is_lost:
                close_window()

            self.fruit.draw()
            self.check_eat()

            self.draw_texts()

            end_drawing()
        close_window()


if __name__ == "__main__":
    Game().run()
