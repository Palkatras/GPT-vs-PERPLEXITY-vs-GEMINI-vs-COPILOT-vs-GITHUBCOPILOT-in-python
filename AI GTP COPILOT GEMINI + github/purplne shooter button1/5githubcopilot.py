import tkinter as tk
import random

# Settings
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
TARGET_RADIUS = 25
TARGET_COLOR = "#FF00FF"   # Magenta
BG_COLOR = "#FFFF00"       # Yellow
TEXT_COLOR = "#FF00FF"     # Magenta

score = 0
target_id = None
target_pos = (0, 0)

def new_target(canvas):
    global target_id, target_pos
    if target_id:
        canvas.delete(target_id)
    x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS + 40, WINDOW_HEIGHT - TARGET_RADIUS)
    target_id = canvas.create_oval(
        x - TARGET_RADIUS, y - TARGET_RADIUS,
        x + TARGET_RADIUS, y + TARGET_RADIUS,
        fill=TARGET_COLOR, outline=TARGET_COLOR
    )
    target_pos = (x, y)

def check_shot(event, canvas, score_text):
    global score, target_id, target_pos
    x, y = event.x, event.y
    tx, ty = target_pos
    distance = ((x - tx) ** 2 + (y - ty) ** 2) ** 0.5
    if distance <= TARGET_RADIUS:
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}")
        new_target(canvas)

def main():
    root = tk.Tk()
    root.title("Yellow-Magenta Shooter")

    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR, highlightthickness=0)
    canvas.pack()

    score_text = canvas.create_text(
        WINDOW_WIDTH // 2, 20,
        text="Score: 0",
        fill=TEXT_COLOR,
        font=("Arial", 20, "bold")
    )

    new_target(canvas)

    canvas.bind("<Button-1>", lambda event: check_shot(event, canvas, score_text))

    root.mainloop()

if __name__ == '__main__':
    main()