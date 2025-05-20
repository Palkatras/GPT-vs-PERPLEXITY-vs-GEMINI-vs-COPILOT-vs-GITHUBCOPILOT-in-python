import tkinter as tk
import random

def create_circle(canvas, x, y, r, color):
    """Creates a circle on the canvas."""
    return canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")

def create_rectangle(canvas, x, y, width, height, color):
    """Creates a rectangle on the canvas."""
    return canvas.create_rectangle(x, y, x + width, y + height, fill=color, outline="")

def move_object(canvas, obj_id, dx, dy):
    """Moves an object on the canvas by the given delta."""
    canvas.move(obj_id, dx, dy)

def get_coords(canvas, obj_id):
    """Gets the coordinates of the bounding box of an object."""
    return canvas.coords(obj_id)

def check_collision(obj1_coords, obj2_coords):
    """Checks if two rectangular objects are colliding.  Accounts for circles by using their bounding box."""
    x1_1, y1_1, x1_2, y1_2 = obj1_coords
    x2_1, y2_1, x2_2, y2_2 = obj2_coords
    return not (x1_2 < x2_1 or x1_1 > x2_2 or y1_2 < y2_1 or y1_1 > y2_2)

def fire_shot(event=None):
    """Fires a shot from the player's position."""
    global player, shots, canvas, score_label
    player_coords = get_coords(canvas, player)
    x = (player_coords[0] + player_coords[2]) / 2
    y = player_coords[1]
    shot = create_circle(canvas, x, y, 5, "magenta")
    shots.append(shot)
    shot_speed = -5  # Shots go upwards
    canvas.itemconfig(shot, tags=("shot",))  # Add a tag

def move_shots():
    """Moves all shots and removes them if they go off-screen."""
    global shots, canvas, enemies, score
    new_shots = []
    for shot in shots:
        move_object(canvas, shot, 0, -5)  # Move upwards
        shot_coords = get_coords(canvas, shot)
        if shot_coords[1] > 0:  # Check if still on screen
            new_shots.append(shot)
        else:
            canvas.delete(shot)
    shots = new_shots

    #check collision between shots and enemies.  If collision, delete both and increase score.
    new_enemies = []
    new_shots = []
    for shot in shots:
        shot_coords = get_coords(canvas, shot)
        for enemy in enemies:
            enemy_coords = get_coords(canvas, enemy)
            if check_collision(shot_coords, enemy_coords):
                canvas.delete(shot)
                canvas.delete(enemy)
                score += 10
                score_label.config(text=f"Score: {score}")
                break # important: break after handling collision with *one* enemy
        else:
            new_shots.append(shot) # only keep the shot if it didn't hit anything
    enemies = new_enemies
    shots = new_shots

def move_enemies():
    """Moves all enemies.  Basic movement, and removes if off-screen."""
    global enemies, canvas, player
    new_enemies = []
    for enemy in enemies:
        move_object(canvas, enemy, 0, 2)  # Move downwards
        enemy_coords = get_coords(canvas, enemy)
        if enemy_coords[3] < window_height:
            new_enemies.append(enemy)
        else:
            canvas.delete(enemy)
    enemies = new_enemies

    # Game over check (basic: if any enemy touches player)
    if enemies: # only check if there are enemies
        player_coords = get_coords(canvas, player)
        for enemy in enemies:
            if check_collision(player_coords, get_coords(canvas, enemy)):
                game_over()
                return # Stop moving enemies, game is over.

def add_enemy():
    """Adds a new enemy at the top of the screen."""
    global enemies, canvas, window_width
    x = random.randint(50, window_width - 50)
    enemy = create_circle(canvas, x, 0, 20, "magenta")
    enemies.append(enemy)

def game_over():
    """Handles game over state."""
    global running, canvas, root
    running = False # Stop the main loop
    # Display Game Over message
    game_over_text = canvas.create_text(window_width / 2, window_height / 2,
                                       text="Game Over", font=("Arial", 30), fill="magenta")
    restart_button = tk.Button(root, text="Restart", command=restart_game, bg="yellow", fg="magenta")
    restart_button.pack()
    #remove binding
    canvas.unbind("<Button-1>")

def restart_game():
    """Restarts the game."""
    global running, canvas, enemies, shots, score, score_label, root
    running = True
    # Clear all existing objects
    for enemy in enemies:
        canvas.delete(enemy)
    for shot in shots:
        canvas.delete(shot)
    enemies = []
    shots = []
    score = 0
    score_label.config(text=f"Score: {score}")
    # Remove the game over text and button.  Assumes only one text item.
    for item in canvas.find_all(): #Find all items
        if canvas.type(item) == "text": # Check if item is text
            canvas.delete(item)
    for widget in root.winfo_children(): #Find all the widgets.
        if isinstance(widget, tk.Button): #Check if it is a button
           widget.destroy()
    # Re-create player
    create_player()
    #restart binding
    canvas.bind("<Button-1>", fire_shot)
    # Restart the game loop.
    game_loop()

def create_player():
    """Creates the player rectangle."""
    global player, canvas, window_width, window_height
    player_width = 30
    player_height = 20
    player_x = window_width / 2 - player_width / 2
    player_y = window_height - player_height - 10
    player = create_rectangle(canvas, player_x, player_y, player_width, player_height, "yellow")

def game_loop():
    """Main game loop."""
    global running, canvas, root
    if running:
        move_shots()
        move_enemies()
        if random.random() < 0.05:  # Adjust probability as needed
            add_enemy()
        canvas.after(30, game_loop)  # Adjust speed as needed

# Initialize the game
root = tk.Tk()
root.title("Yellow vs. Magenta Minigame")
root.configure(bg="yellow")  # Set background color of the window

window_width = 600
window_height = 400
canvas = tk.Canvas(root, width=window_width, height=window_height, bg="yellow", highlightthickness=0)
canvas.pack()

score = 0
score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), bg="yellow", fg="magenta")
score_label.pack()

player = None # Will be created in create_player
create_player()

shots = []
enemies = []
running = True

canvas.bind("<Button-1>", fire_shot)  # Bind left mouse button to fire_shot

game_loop()  # Start the game loop
root.mainloop()
