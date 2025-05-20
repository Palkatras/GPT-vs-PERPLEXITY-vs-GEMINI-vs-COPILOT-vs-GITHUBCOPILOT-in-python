import tkinter as tk
import random

class Tetris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rainbow Tetris")
        self.geometry("300x600")
        self.canvas = tk.Canvas(self, width=300, height=600, bg='black')
        self.canvas.pack()
        
        self.cell_size = 30
        self.cols = 10
        self.rows = 20
        self.score = 0
        
        self.colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00",
                      "#0000FF", "#4B0082", "#8F00FF"]
        
        self.shapes = [
            [[1, 1, 1, 1]],          # I
            [[1, 1], [1, 1]],        # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ]
        
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = None
        self.current_pos = [0, 4]
        self.current_color = random.choice(self.colors)
        
        self.bind_all("<Key>", self.key_pressed)
        self.spawn_piece()
        self.update_clock()

    def spawn_piece(self):
        self.current_piece = random.choice(self.shapes)
        self.current_pos = [0, self.cols//2 - len(self.current_piece[0])//2]
        self.current_color = random.choice(self.colors)
        
        if not self.valid_position():
            self.game_over()

    def valid_position(self, pos=None, piece=None):
        pos = pos or self.current_pos
        piece = piece or self.current_piece
        for r, row in enumerate(piece):
            for c, cell in enumerate(row):
                if cell:
                    row_pos = pos[0] + r
                    col_pos = pos[1] + c
                    if (col_pos < 0 or col_pos >= self.cols or
                        row_pos >= self.rows or
                        (row_pos >= 0 and self.board[row_pos][col_pos])):
                        return False
        return True

    def rotate_piece(self):
        rotated = list(zip(*reversed(self.current_piece)))
        if self.valid_position(piece=rotated):
            self.current_piece = rotated

    def key_pressed(self, event):
        key = event.keysym.lower()
        if key == 'w':
            self.rotate_piece()
        elif key == 'a':
            self.move(0, -1)
        elif key == 's':
            self.move(1, 0)
        elif key == 'd':
            self.move(0, 1)
        self.draw_board()

    def move(self, dr, dc):
        new_pos = [self.current_pos[0] + dr, self.current_pos[1] + dc]
        if self.valid_position(new_pos):
            self.current_pos = new_pos
        elif dr == 1:
            self.merge_piece()
            self.clear_lines()
            self.spawn_piece()

    def merge_piece(self):
        for r, row in enumerate(self.current_piece):
            for c, cell in enumerate(row):
                if cell:
                    row_pos = self.current_pos[0] + r
                    col_pos = self.current_pos[1] + c
                    if row_pos >= 0:
                        self.board[row_pos][col_pos] = self.current_color

    def clear_lines(self):
        full_rows = []
        for r, row in enumerate(self.board):
            if all(cell is not None for cell in row):
                full_rows.append(r)
        
        for r in full_rows:
            del self.board[r]
            self.board.insert(0, [None]*self.cols)
            self.score += 100
        
        if full_rows:
            self.draw_board()

    def draw_cell(self, row, col, color):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw board cells
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]:
                    self.draw_cell(r, c, self.board[r][c])
        
        # Draw current piece
        if self.current_piece:
            for r, row in enumerate(self.current_piece):
                for c, cell in enumerate(row):
                    if cell:
                        row_pos = self.current_pos[0] + r
                        col_pos = self.current_pos[1] + c
                        if row_pos >= 0:
                            self.draw_cell(row_pos, col_pos, self.current_color)
        
        # Draw score
        self.canvas.create_text(150, 30, text=f"Score: {self.score}", fill="white")

    def update_clock(self):
        self.move(1, 0)
        self.after(1000, self.update_clock)

    def game_over(self):
        self.canvas.create_text(150, 300, text="GAME OVER", fill="red", font=("Arial", 24))
        self.unbind_all("<Key>")

if __name__ == "__main__":
    game = Tetris()
    game.mainloop()
