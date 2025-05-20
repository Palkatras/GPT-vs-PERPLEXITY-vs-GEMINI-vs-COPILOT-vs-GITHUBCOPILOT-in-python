import tkinter as tk
import random
import math

# === CONFIG ===
WIDTH = 800
HEIGHT = 400
ROWS = 7
COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
SPEEDS = [1, 2, 3, 4, 5, 6, 7]  # different rhythm speeds
RADIUS = 10

# === GLOBALS ===
positions = [0] * ROWS
canvas = None

def draw():
    canvas.delete("all")
    row_height = HEIGHT // ROWS
    for i in range(ROWS):
        y = row_height * i + row_height // 2
        speed = SPEEDS[i]
        x = (positions[i] % WIDTH)
        
        # Repeat pattern across screen
        for j in range(0, WIDTH, 100):
            cx = (x + j) % WIDTH
            canvas.create_oval(cx - RADIUS, y - RADIUS, cx + RADIUS, y + RADIUS, fill=COLORS[i], outline="")

def update():
    for i in range(ROWS):
        positions[i] += SPEEDS[i] * 2  # update each row at different speed
    draw()
    root.after(30, update)

# === MAIN ===
root = tk.Tk()
root.title("Rainbow Polyrhythm Visualizer")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

update()
root.mainloop()
