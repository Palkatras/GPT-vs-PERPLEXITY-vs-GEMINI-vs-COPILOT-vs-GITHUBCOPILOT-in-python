import tkinter as tk
import random

# Tetris shapes and their colors (rainbow order)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]
RAINBOW = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]

CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
DELAY = 300  # ms

class Tetrig:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLUMNS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.score = 0
        self.current_piece = None
        self.current_pos = (0, COLUMNS//2 - 2)
        self.running = True

        root.bind("<Key>", self.key_press)
        self.spawn_piece()
        self.draw_board()
        self.drop()

    def spawn_piece(self):
        idx = random.randint(0, len(SHAPES)-1)
        self.current_shape = SHAPES[idx]
        self.current_color = RAINBOW[random.randint(0, len(RAINBOW)-1)]
        self.current_pos = (0, COLUMNS//2 - len(self.current_shape[0])//2)
        if self.collision(self.current_shape, self.current_pos):
            self.running = False
            self.game_over()
        else:
            self.current_piece = (self.current_shape, self.current_color)

    def key_press(self, event):
        if not self.running:
            return
        key = event.char.lower()
        if key == 'a':  # Left
            self.move(-1)
        elif key == 'd':  # Right
            self.move(1)
        elif key == 's':  # Down
            self.drop(force=True)
        elif key == 'w':  # Rotate
            self.rotate()
        self.draw_board()

    def move(self, dx):
        shape, color = self.current_piece
        x, y = self.current_pos
        if not self.collision(shape, (x, y + dx)):
            self.current_pos = (x, y + dx)

    def rotate(self):
        shape, color = self.current_piece
        rotated = [list(row) for row in zip(*shape[::-1])]
        if not self.collision(rotated, self.current_pos):
            self.current_piece = (rotated, color)

    def collision(self, shape, pos):
        x, y = pos
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    xi = x + i
                    yj = y + j
                    if xi < 0 or xi >= ROWS or yj < 0 or yj >= COLUMNS:
                        return True
                    if self.board[xi][yj]:
                        return True
        return False

    def lock_piece(self):
        shape, color = self.current_piece
        x, y = self.current_pos
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[x + i][y + j] = color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(COLUMNS)])
        self.board = new_board
        self.score += lines_cleared

    def drop(self, force=False):
        if not self.running:
            return
        shape, color = self.current_piece
        x, y = self.current_pos
        if not self.collision(shape, (x + 1, y)):
            self.current_pos = (x + 1, y)
        else:
            self.lock_piece()
        self.draw_board()
        if self.running and not force:
            self.root.after(DELAY, self.drop)

    def draw_board(self):
        self.canvas.delete("all")
        # Draw locked pieces
        for i in range(ROWS):
            for j in range(COLUMNS):
                color = self.board[i][j]
                if color:
                    self.draw_cell(i, j, color)
        # Draw current piece
        if self.current_piece and self.running:
            shape, color = self.current_piece
            x, y = self.current_pos
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell:
                        self.draw_cell(x + i, y + j, color)
        # Draw score
        self.canvas.create_text(5, 5, anchor="nw", text=f"Score: {self.score}", fill="white", font=("Arial", 14, "bold"))

    def draw_cell(self, i, j, color):
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="grey")

    def game_over(self):
        self.canvas.create_text(COLUMNS*CELL_SIZE//2, ROWS*CELL_SIZE//2,
                               text="GAME OVER", fill="white", font=("Arial", 32, "bold"))
        self.canvas.create_text(COLUMNS*CELL_SIZE//2, ROWS*CELL_SIZE//2+40,
                               text=f"Score: {self.score}", fill="white", font=("Arial", 18, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rainbow Tetrig")
    game = Tetrig(root)
    root.mainloop()