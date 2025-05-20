import tkinter as tk
import random

# === Config ===
ROWS = 20
COLS = 10
CELL_SIZE = 30
DELAY = 500  # gravity delay in ms

# Rainbow colors
COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

# Tetrimino shapes (2D coordinates)
SHAPES = {
    'I': [[(0,0), (1,0), (2,0), (3,0)]],
    'O': [[(0,0), (1,0), (0,1), (1,1)]],
    'T': [[(0,0), (1,0), (2,0), (1,1)]],
    'L': [[(0,0), (0,1), (1,1), (2,1)]],
    'J': [[(2,0), (0,1), (1,1), (2,1)]],
    'S': [[(1,0), (2,0), (0,1), (1,1)]],
    'Z': [[(0,0), (1,0), (1,1), (2,1)]],
}

# === Game class ===
class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = None
        self.current_color = None
        self.current_coords = []
        self.offset_x = 3
        self.offset_y = 0
        self.running = True

        self.root.bind("<Key>", self.key_press)
        self.spawn_piece()
        self.update()

    def spawn_piece(self):
        shape_key = random.choice(list(SHAPES))
        shape = SHAPES[shape_key][0]
        color = random.choice(COLORS)
        self.current_piece = shape
        self.current_color = color
        self.offset_x = 3
        self.offset_y = 0
        self.current_coords = shape

    def draw(self):
        self.canvas.delete("all")
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.board[y][x])

        for dx, dy in self.current_coords:
            x = self.offset_x + dx
            y = self.offset_y + dy
            self.draw_cell(x, y, self.current_color)

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def move(self, dx, dy):
        if self.valid_position(dx, dy):
            self.offset_x += dx
            self.offset_y += dy

    def rotate(self):
        rotated = [(dy, -dx) for dx, dy in self.current_coords]
        if self.valid_position(0, 0, rotated):
            self.current_coords = rotated

    def valid_position(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_coords
        for sx, sy in shape:
            x = self.offset_x + sx + dx
            y = self.offset_y + sy + dy
            if x < 0 or x >= COLS or y < 0 or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x]:
                return False
        return True

    def lock_piece(self):
        for dx, dy in self.current_coords:
            x = self.offset_x + dx
            y = self.offset_y + dy
            if 0 <= x < COLS and 0 <= y < ROWS:
                self.board[y][x] = self.current_color
        self.spawn_piece()

    def update(self):
        if not self.running:
            return
        if self.valid_position(0, 1):
            self.offset_y += 1
        else:
            self.lock_piece()
        self.draw()
        self.root.after(DELAY, self.update)

    def key_press(self, event):
        key = event.keysym.lower()
        if key == 'a':
            self.move(-1, 0)
        elif key == 'd':
            self.move(1, 0)
        elif key == 's':
            self.move(0, 1)
        elif key == 'w':
            self.rotate()
        self.draw()

# === Main program ===
root = tk.Tk()
root.title("Rainbow Tetris (WASD Controls)")
game = Tetris(root)
root.mainloop()
