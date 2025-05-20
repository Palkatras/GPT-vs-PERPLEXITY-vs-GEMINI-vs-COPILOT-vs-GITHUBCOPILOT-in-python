import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 50
COLORS = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

# Initialize Tkinter
root = tk.Tk()
root.title("Rainbow Polyrhythm")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

def draw_pattern():
    """Draws a simple polyrhythm pattern using colored rectangles."""
    for i in range(HEIGHT // GRID_SIZE):
        for j in range(WIDTH // GRID_SIZE):
            color = random.choice(COLORS)
            canvas.create_rectangle(
                j * GRID_SIZE, i * GRID_SIZE, 
                (j + 1) * GRID_SIZE, (i + 1) * GRID_SIZE, 
                fill=color, outline="black"
            )

def update_pattern():
    """Updates the colors periodically to create an animated effect."""
    canvas.delete("all")
    draw_pattern()
    root.after(500, update_pattern)  # Update every 500ms

draw_pattern()  # Initial drawing
root.after(500, update_pattern)  # Start animation
root.mainloop()
