import tkinter as tk
import random

# Initialize main window
root = tk.Tk()
root.title("Shooting Minigame")
root.geometry("500x500")
root.configure(bg='yellow')

# Game variables
shots = 0
hits = 0
target_radius =150

# Score display
score_label = tk.Label(root, text="Shots: 0  Hits: 0", font=('Arial', 16), bg='yellow', fg='magenta')
score_label.pack(pady=15)

# Game canvas
game_area = tk.Canvas(root, width=400, height=400, bg='magenta')
game_area.pack()

# Create initial target
target_x = random.randint(target_radius, 400-target_radius)
target_y = random.randint(target_radius, 400-target_radius)
target = game_area.create_oval(
    target_x - target_radius,
    target_y - target_radius,
    target_x + target_radius,
    target_y + target_radius,
    fill='yellow'
)

def update_target():
    global target_x, target_y
    target_x = random.randint(target_radius, 400-target_radius)
    target_y = random.randint(target_radius, 400-target_radius)
    game_area.coords(
        target,
        target_x - target_radius,
        target_y - target_radius,
        target_x + target_radius,
        target_y + target_radius
    )

def handle_click(event):
    global shots, hits
    shots += 1
    x, y = event.x, event.y
    
    if (target_x - target_radius <= x <= target_x + target_radius and 
        target_y - target_radius <= y <= target_y + target_radius):
        hits += 1
        update_target()
    
    score_label.config(text=f"Shots: {shots}  Hits: {hits}")

game_area.bind('<Button-1>', handle_click)
root.mainloop()
