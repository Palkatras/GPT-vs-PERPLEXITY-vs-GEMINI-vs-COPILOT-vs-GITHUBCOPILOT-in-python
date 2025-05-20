import tkinter as tk
import random

# --- CONFIG ---
WIDTH = 800
HEIGHT = 600
BULLET_SPEED = -15
TARGET_SPEED = 2
NUM_TARGETS = 5

# --- SETUP ---
root = tk.Tk()
root.title("Magenta Shooter!")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# --- LISTS TO TRACK OBJECTS ---
bullets = []
targets = []

# --- FUNCTIONS ---

def spawn_targets():
    for _ in range(NUM_TARGETS):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(20, 150)
        r = 20
        target = canvas.create_oval(x - r, y - r, x + r, y + r, fill="yellow", outline="")
        targets.append(target)

def shoot_bullet(event):
    x = WIDTH // 2
    y = HEIGHT - 30
    r = 5
    bullet = canvas.create_oval(x - r, y - r, x + r, y + r, fill="magenta", outline="")
    bullets.append(bullet)

def move_objects():
    # Move bullets
    for bullet in bullets[:]:
        canvas.move(bullet, 0, BULLET_SPEED)
        bx1, by1, bx2, by2 = canvas.coords(bullet)
        if by2 < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    
    # Move targets
    for target in targets:
        dx = random.choice([-TARGET_SPEED, 0, TARGET_SPEED])
        canvas.move(target, dx, 0)
        tx1, ty1, tx2, ty2 = canvas.coords(target)
        # Keep targets within bounds
        if tx1 < 0 or tx2 > WIDTH:
            canvas.move(target, -dx * 2, 0)

def check_collisions():
    for bullet in bullets[:]:
        bx1, by1, bx2, by2 = canvas.coords(bullet)
        for target in targets[:]:
            tx1, ty1, tx2, ty2 = canvas.coords(target)
            overlap = not (bx2 < tx1 or bx1 > tx2 or by2 < ty1 or by1 > ty2)
            if overlap:
                canvas.delete(bullet)
                canvas.delete(target)
                bullets.remove(bullet)
                targets.remove(target)
                break

def game_loop():
    move_objects()
    check_collisions()
    root.after(30, game_loop)

# --- BINDINGS & START ---
canvas.bind("<Button-1>", shoot_bullet)
canvas.bind("9", shoot_bullet)
canvas.focus_set()
spawn_targets()
game_loop()

root.mainloop()
