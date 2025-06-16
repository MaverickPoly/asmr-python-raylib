from raylib import *
from pyray import *

# Settings
WIDTH, HEIGHT = 1000, 1000


class Game:
    def __init__(self):
        init_window(WIDTH, HEIGHT, "Tic Tac Toe Game")
        
        self.generate_board()
        self.player = 'X'
        self.text = f"Current player: {self.player}"
        self.game_over = False

    def _is_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] not in ["X", "O"]:
                    return False
        return True

    def _check_win(self):
        # Horizontal
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '':
                return True
        
        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] != '':
            return True

        # Vertical
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '':
                return True
            
        return False

    def generate_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def draw_board(self):
        for i in range(3):
            for j in range(3):
                x, y = 200 + 200 * j, 200 + 200 * i
                draw_rectangle(x, y, 200, 200, WHITE)

        # Horizonstal Lines
        for i in range(1, 3):
            startx, y = 200, 200 + 200 * i
            endx = 200 + 200 * 3
            draw_line(startx, y, endx, y, BLACK)
        # Vertical Lines
        for i in range(1, 3):
            x, starty = 200 + 200 * i, 200
            endy = 200 + 200 * 3
            draw_line(x, starty, x, endy, BLACK)

        # Texts inside Boxes
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                x, y = 200 + 200 * j + 75, 200 + 200 * i + 70
                draw_text(val, x, y, 80, BLACK)

    def handle_click(self):
        pos = get_mouse_position()
        if not (200 <= pos.x <= 800 and 200 <= pos.y <= 800):
            return
        row = int((pos.y - 200) // 200)
        col = int((pos.x - 200) // 200)
        if self.board[row][col] in ["X", "O"]:
            return
        
        self.board[row][col] = self.player

        if self._check_win():
            self.text = f"Player {self.player} won!"
            self.game_over = True
        elif self._is_draw():
            self.text = "It is Draw!"
            self.game_over = True
        else:
            self.player = 'X' if self.player == 'O' else 'O'
            self.text = f"Current player: {self.player}"
    
    def display_texts(self):
        draw_text(self.text, 200, 850, 48, BLACK)

    def run(self):
        while not window_should_close():
            begin_drawing()
            clear_background((240, 240, 240))

            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not self.game_over:
                self.handle_click()

            self.draw_board()
            self.display_texts()

            end_drawing()
        close_window()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
