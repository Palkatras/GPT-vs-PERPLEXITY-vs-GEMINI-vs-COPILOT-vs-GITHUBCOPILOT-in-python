import tkinter as tk
import random
import math

# Polyrythm parameters
WIDTH = 800
HEIGHT = 400
N_TRACKS = 5
TRACK_HEIGHT = HEIGHT // N_TRACKS
STEP_COUNT = [5, 7, 9, 11, 14]  # Distinct steps for each track (polyrythm!)
STEP_SIZE = 48  # pixel width per step
BEAT_RADIUS = 12
RAINBOW = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
BG = "#181818"

root = tk.Tk()
root.title("Rainbow Polyrythm")

canvas = tk.Canvas(root, bg=BG, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()

# State (no OOP)
current_beat = [0] * N_TRACKS

def draw_polyrythm():
    canvas.delete("all")
    for t in range(N_TRACKS):
        steps = STEP_COUNT[t]
        y = t * TRACK_HEIGHT + TRACK_HEIGHT // 2
        color = RAINBOW[t % len(RAINBOW)]
        # Draw horizontal line
        canvas.create_line(0, y, WIDTH, y, fill="#333", width=3)
        # Draw steps
        for s in range(steps):
            x = 50 + s * STEP_SIZE
            r = BEAT_RADIUS
            fill = color if s == current_beat[t] else ""
            outline = color if s == current_beat[t] else "#444"
            canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=3)
        # Track label
        canvas.create_text(20, y, text=f"{steps}", fill="white", font=("Arial", 14, "bold"))

def tick():
    for t in range(N_TRACKS):
        current_beat[t] = (current_beat[t] + 1) % STEP_COUNT[t]
    draw_polyrythm()
    root.after(220, tick)

def randomize():
    for t in range(N_TRACKS):
        current_beat[t] = random.randint(0, STEP_COUNT[t]-1)
    draw_polyrythm()

def reset():
    for t in range(N_TRACKS):
        current_beat[t] = 0
    draw_polyrythm()

def key(event):
    if event.char == 'r':
        randomize()
    elif event.char == '0':
        reset()

root.bind("<Key>", key)

draw_polyrythm()
root.after(400, tick)
root.mainloop()