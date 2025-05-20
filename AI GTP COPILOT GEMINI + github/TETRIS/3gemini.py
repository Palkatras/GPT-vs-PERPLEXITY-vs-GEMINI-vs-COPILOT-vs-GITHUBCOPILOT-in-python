import tkinter as tk
import random

class RainbowTetris:
    def __init__(self, master):
        self.master = master
        self.master.title("Rainbow Tetris")

        self.CELL_SIZE = 30
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.GAME_SPEED = 500  # Milliseconds

        self.canvas = tk.Canvas(master, width=self.GRID_WIDTH * self.CELL_SIZE,
                                 height=self.GRID_HEIGHT * self.CELL_SIZE, bg="black")
        self.canvas.pack()

        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.current_piece_x = 0
        self.current_piece_y = 0

        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

        # Basic piece shapes (simplified - you'll need full Tetris shapes)
        self.shapes = {
            "O": [[1, 1],
                  [1, 1]],
            "I": [[1, 1, 1, 1]],
            "T": [[0, 1, 0],
                  [1, 1, 1]],
            # Add more Tetris shapes (L, J, S, Z)
        }

        self.spawn_new_piece()
        self.draw_grid()
        self.master.bind("<KeyPress>", self.key_press)

        self.game_loop()

    def spawn_new_piece(self):
        shape_name = random.choice(list(self.shapes.keys()))
        self.current_piece = self.shapes[shape_name]
        self.current_piece_color = random.choice(self.colors)
        self.current_piece_x = self.GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_piece_y = 0

        # Game Over condition (simplified)
        if not self.is_valid_position(self.current_piece, self.current_piece_x, self.current_piece_y):
            self.game_over()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.GRID_HEIGHT):
            for c in range(self.GRID_WIDTH):
                if self.grid[r][c] != 0:
                    self.draw_block(c, r, self.grid[r][c])

        if self.current_piece:
            for r_offset, row in enumerate(self.current_piece):
                for c_offset, cell in enumerate(row):
                    if cell:
                        self.draw_block(self.current_piece_x + c_offset,
                                        self.current_piece_y + r_offset,
                                        self.current_piece_color)

    def draw_block(self, x, y, color):
        x1 = x * self.CELL_SIZE
        y1 = y * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")

    def is_valid_position(self, piece, x, y):
        for r_offset, row in enumerate(piece):
            for c_offset, cell in enumerate(row):
                if cell:
                    grid_x = x + c_offset
                    grid_y = y + r_offset

                    if not (0 <= grid_x < self.GRID_WIDTH and 0 <= grid_y < self.GRID_HEIGHT):
                        return False  # Out of bounds

                    if self.grid[grid_y][grid_x] != 0:
                        return False  # Collision with existing block

        return True

    def merge_piece_to_grid(self):
        for r_offset, row in enumerate(self.current_piece):
            for c_offset, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece_y + r_offset][self.current_piece_x + c_offset] = self.current_piece_color
        self.current_piece = None

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row[:] for row in self.grid] # Make a copy to modify

        for r in range(self.GRID_HEIGHT):
            if all(cell != 0 for cell in self.grid[r]):
                lines_cleared += 1
                del new_grid[r]
                new_grid.insert(0, [0 for _ in range(self.GRID_WIDTH)]) # Add empty row at top

        self.grid = new_grid
        # You'd typically add score updates here
        return lines_cleared

    def game_loop(self):
        if self.current_piece:
            # Try to move down
            if self.is_valid_position(self.current_piece, self.current_piece_x, self.current_piece_y + 1):
                self.current_piece_y += 1
            else:
                self.merge_piece_to_grid()
                self.clear_lines()
                self.spawn_new_piece()
        else:
            self.spawn_new_piece()

        self.draw_grid()
        self.master.after(self.GAME_SPEED, self.game_loop)

    def key_press(self, event):
        if not self.current_piece:
            return

        dx, dy = 0, 0
        if event.keysym == "a":
            dx = -1
        elif event.keysym == "d":
            dx = 1
        elif event.keysym == "s":
            dy = 1
        elif event.keysym == "w":
            # For Tetris, 'w' typically rotates the piece.
            # This is a complex operation. For simplicity, we'll just drop it for now.
            # You'll need a proper rotation function.
            # Example (very basic - doesn't handle wall kicks, etc.):
            rotated_piece = [list(col) for col in zip(*self.current_piece[::-1])]
            if self.is_valid_position(rotated_piece, self.current_piece_x, self.current_piece_y):
                 self.current_piece = rotated_piece
            else:
                # If rotation isn't valid, try to nudge (wall kick logic is complex)
                # For now, just ignore invalid rotations
                pass
            self.draw_grid() # Redraw immediately after rotation attempt
            return

        if self.is_valid_position(self.current_piece, self.current_piece_x + dx, self.current_piece_y + dy):
            self.current_piece_x += dx
            self.current_piece_y += dy
            self.draw_grid()

    def game_over(self):
        # You'd display a "Game Over" message, stop the game loop, etc.
        print("Game Over!")
        self.master.after_cancel(self.game_loop) # Stop the game loop
        self.canvas.create_text(self.GRID_WIDTH * self.CELL_SIZE / 2,
                                self.GRID_HEIGHT * self.CELL_SIZE / 2,
                                text="GAME OVER", fill="white", font=("Arial", 24))


if __name__ == "__main__":
    root = tk.Tk()
    game = RainbowTetris(root)
    root.mainloop()