from raylib import *
from pyray import *
from os import path

WIDTH, HEIGHT = 832, 640
SIZE = 64
ROWS, COLS = 10, 13

LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
DOWN = Vector2(0, 1)
UP = Vector2(0, -1)

class Player:
    def __init__(self):
        self.right = load_image(path.join("09.Sokoban", "assets", "right.png"))
        self.left = load_image(path.join("09.Sokoban", "assets", "left.png"))
        self.up = load_image(path.join("09.Sokoban", "assets", "up.png"))
        self.down = load_image(path.join("09.Sokoban", "assets", "down.png"))

    def draw(self, image: Image, x, y):
        texture = load_texture_from_image(image)
        draw_texture(texture, x, y, WHITE)

class Sokoban:
    def __init__(self):
        init_window(WIDTH, HEIGHT, "Sokoban")
        set_target_fps(60)

        self.level = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 2, 2, 3, 1, 3, 2, 2, 2, 2, 4, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.wall_image = load_image(path.join("09.Sokoban", "assets", "wall.png"))
        self.floor_image = load_image(path.join("09.Sokoban", "assets", "floor.png"))
        self.box_image = load_image(path.join("09.Sokoban", "assets", "box.png"))
        self.target_image = load_image(path.join("09.Sokoban", "assets", "target.png"))

        self.wall_texture = load_texture_from_image(self.wall_image)
        self.floor_texture = load_texture_from_image(self.floor_image)
        self.box_texture = load_texture_from_image(self.box_image)
        self.target_texture = load_texture_from_image(self.target_image)

        self.player_direction = Vector2(0, 1)
        self.player = Player()
        self.game_won = False
        self.move_cooldown = 0
        self.targets = self.count_targets()

    def count_targets(self):
        return sum(row.count(4) for row in self.level)

    def find_player(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.level[row][col] == 1:
                    return Vector2(col, row)
        return Vector2(0, 0)

    def is_valid_move(self, pos: Vector2):
        return (0 <= pos.x < COLS and 0 <= pos.y < ROWS and 
                self.level[int(pos.y)][int(pos.x)] != 0)

    def can_push_box(self, box_pos: Vector2, direction: Vector2):
        next_pos = Vector2(box_pos.x + direction.x, box_pos.y + direction.y)
        return (self.is_valid_move(next_pos) and 
                self.level[int(next_pos.y)][int(next_pos.x)] not in [3, 0])

    def move_player(self, direction: Vector2):
        if self.move_cooldown > 0 or self.game_won:
            return

        player_pos = self.find_player()
        next_pos = Vector2(player_pos.x + direction.x, player_pos.y + direction.y)

        if not self.is_valid_move(next_pos):
            return

        next_cell = self.level[int(next_pos.y)][int(next_pos.x)]
        
        if next_cell == 3:  # Box
            box_pos = next_pos
            if self.can_push_box(box_pos, direction):
                # Move box
                new_box_pos = Vector2(box_pos.x + direction.x, box_pos.y + direction.y)
                self.level[int(new_box_pos.y)][int(new_box_pos.x)] = 3
                self.level[int(box_pos.y)][int(box_pos.x)] = 2
                # Move player
                self.level[int(player_pos.y)][int(player_pos.x)] = 2
                self.level[int(next_pos.y)][int(next_pos.x)] = 1
                self.move_cooldown = 10
        elif next_cell in [2, 4]:  # Floor or Target
            self.level[int(player_pos.y)][int(player_pos.x)] = 2
            self.level[int(next_pos.y)][int(next_pos.x)] = 1
            self.move_cooldown = 10

    def check_win(self):
        boxes_on_targets = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.level[row][col] == 3:
                    for target_row in range(ROWS):
                        for target_col in range(COLS):
                            if (self.level[target_row][target_col] == 4 and 
                                row == target_row and col == target_col):
                                boxes_on_targets += 1
        return boxes_on_targets == self.targets

    def draw_wall(self, x, y):
        draw_texture(self.wall_texture, x, y, WHITE)

    def draw_player(self, x, y):
        if self.player_direction == UP:
            image = self.player.up
        elif self.player_direction == DOWN:
            image = self.player.down
        elif self.player_direction == LEFT:
            image = self.player.left
        else:
            image = self.player.right
        self.player.draw(image, x, y)

    def draw_floor(self, x, y):
        draw_texture(self.floor_texture, x, y, WHITE)

    def draw_box(self, x, y):
        draw_texture(self.box_texture, x, y, WHITE)

    def draw_target(self, x, y):
        draw_texture(self.target_texture, x, y, WHITE)

    def draw_map(self):
        for row, els in enumerate(self.level):
            for col, el in enumerate(els):
                x, y = col * SIZE, row * SIZE
                if el == 4:
                    self.draw_floor(x, y)
                    self.draw_target(x, y)
                elif el == 2:
                    self.draw_floor(x, y)
                elif el == 3:
                    self.draw_floor(x, y)
                    self.draw_box(x, y)
                elif el == 1:
                    self.draw_floor(x, y)
                    self.draw_player(x, y)
                else:  # Wall (0)
                    self.draw_wall(x, y)

        if self.game_won:
            draw_text("You Won!", WIDTH//2 - 50, HEIGHT//2, 30, GREEN)

    def handle_player(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        if is_key_pressed(KEY_LEFT):
            self.player_direction = LEFT
            self.move_player(LEFT)
        elif is_key_pressed(KEY_RIGHT):
            self.player_direction = RIGHT
            self.move_player(RIGHT)
        elif is_key_pressed(KEY_DOWN):
            self.player_direction = DOWN
            self.move_player(DOWN)
        elif is_key_pressed(KEY_UP):
            self.player_direction = UP
            self.move_player(UP)

        if self.check_win():
            self.game_won = True

    def run(self):
        while not window_should_close():
            begin_drawing()
            clear_background(BLACK)
            self.handle_player()
            self.draw_map()
            end_drawing()

        close_window()

if __name__ == "__main__":
    game = Sokoban()
    game.run()