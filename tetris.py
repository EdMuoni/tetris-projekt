import tkinter as tk
import random
import tkinter.messagebox

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
DELAY = 300
FAST_DELAY = 50

TETROMINOES = {
    'O': [[1, 1], [1, 1]],
    'I': [[1, 1, 1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}

COLORS = {
    0: "black",
    1: "blue"
}

class TetrisGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")

        self.canvas = tk.Canvas(self.root, width=BOARD_WIDTH * CELL_SIZE, height=BOARD_HEIGHT * CELL_SIZE, bg="black")
        self.canvas.pack()

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        self.start_button = tk.Button(self.root, text="START", font=("Arial", 14), command=self.start_game)
        # Place button on top of the canvas, centered
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

        self.root.mainloop()

    def start_game(self):
        self.start_button.destroy()
        self.restart()

    def restart(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.shape = self.new_shape()
        self.pos = [BOARD_WIDTH // 2 - len(self.shape[0]) // 2, 0]
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.running = True
        self.fast = False
        self.root.bind("<Key>", self.key_press)
        self.game_loop()

    def new_shape(self):
        return random.choice(list(TETROMINOES.values()))

    def draw(self):
        self.canvas.delete("all")
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.draw_cell(x, y, self.board[y][x])
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(self.pos[0] + x, self.pos[1] + y, 1)

    def draw_cell(self, x, y, value):
        color = COLORS.get(value, "gray")
        x0 = x * CELL_SIZE
        y0 = y * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def key_press(self, event):
        if not self.running:
            return
        key = event.keysym.lower()
        if key == 'a':
            self.move(-1, 0)
        elif key == 'd':
            self.move(1, 0)
        elif key == 's':
            self.move(0, 1)
        elif key == 'w':
            self.rotate()
        elif key == 'space':
            self.fast = True

    def game_loop(self):
        if not self.running:
            return
        self.update()
        self.draw()
        delay = FAST_DELAY if self.fast else DELAY
        self.fast = False
        self.root.after(delay, self.game_loop)

    def update(self):
        if self.valid_move(0, 1):
            self.pos[1] += 1
        else:
            self.merge()
            self.clear_lines()
            self.shape = self.new_shape()
            self.pos = [BOARD_WIDTH // 2 - len(self.shape[0]) // 2, 0]
            if not self.valid_move(0, 0):
                self.game_over()

    def move(self, dx, dy):
        if self.valid_move(dx, dy):
            self.pos[0] += dx
            self.pos[1] += dy

    def rotate(self):
        rotated = [list(row)[::-1] for row in zip(*self.shape)]
        old_shape = self.shape
        self.shape = rotated
        if not self.valid_move(0, 0):
            self.shape = old_shape

    def valid_move(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.pos[0] + x + dx
                    ny = self.pos[1] + y + dy
                    if nx < 0 or nx >= BOARD_WIDTH or ny < 0 or ny >= BOARD_HEIGHT:
                        return False
                    if self.board[ny][nx]:
                        return False
        return True

    def merge(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.pos[1] + y][self.pos[0] + x] = 1

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [0] * BOARD_WIDTH)
        self.board = new_board
        self.score += cleared * 100
        self.score_label.config(text=f"Score: {self.score}")

    def game_over(self):
        self.running = False
        if tk.messagebox.askyesno("Game Over", f"Your score: {self.score}\nPlay again?"):
            self.restart()
        else:
            self.root.destroy()

if __name__ == "__main__":
    TetrisGame()