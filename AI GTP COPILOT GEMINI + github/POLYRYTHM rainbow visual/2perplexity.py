import tkinter as tk
import random

# Configuration
NUM_BARS = 12
BASE_SPEED = 2
RAINBOW = [
    '#ff0000', '#ff5500', '#ffaa00', 
    '#ffff00', '#aaff00', '#55ff00',
    '#00ff00', '#00ff55', '#00ffaa',
    '#00ffff', '#00aaff', '#0055ff',
    '#0000ff', '#5500ff', '#aa00ff',
    '#ff00ff'
]

# Global state
bars = []
directions = []
speeds = []

def create_visualizer():
    win = tk.Tk()
    win.title("Rainbow Polyrhythm")
    win.geometry("800x400")
    win.configure(bg='black')
    
    canvas = tk.Canvas(win, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create initial bars
    bar_height = win.winfo_height() / NUM_BARS
    for i in range(NUM_BARS):
        color = RAINBOW[i % len(RAINBOW)]
        y1 = i * bar_height
        y2 = (i + 1) * bar_height
        bar = canvas.create_rectangle(0, y1, win.winfo_width(), y2, fill=color, outline='')
        bars.append(bar)
        directions.append(1)
        speeds.append(BASE_SPEED * (i % 3 + 1))
    
    def update():
        canvas_width = canvas.winfo_width()
        for i, (bar, speed) in enumerate(zip(bars, speeds)):
            x1, y1, x2, y2 = canvas.coords(bar)
            new_x1 = (x1 + speed) % canvas_width
            canvas.coords(bar, new_x1, y1, new_x1 + (x2 - x1), y2)
        win.after(16, update)
    
    def on_resize(event):
        bar_height = event.height / NUM_BARS
        for i, bar in enumerate(bars):
            y1 = i * bar_height
            y2 = (i + 1) * bar_height
            canvas.coords(bar, 0, y1, event.width, y2)
    
    canvas.bind('<Configure>', on_resize)
    win.after(0, update)
    win.mainloop()

create_visualizer()
