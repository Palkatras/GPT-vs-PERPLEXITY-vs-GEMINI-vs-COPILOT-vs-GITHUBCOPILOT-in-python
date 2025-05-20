import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Yellow-Magenta Minigame")
root.geometry("500x500")
root.configure(bg="yellow")

# Create a canvas for drawing
canvas = tk.Canvas(root, bg="yellow", width=500, height=500)
canvas.pack()

# Function to create a target
def create_target():
    canvas.delete("all")  # Clear previous targets
    x, y = random.randint(50, 450), random.randint(50, 450)
    canvas.create_oval(x-20, y-20, x+20, y+20, fill="magenta", tags="target")

# Function to handle shots
def shoot(event):
    x, y = event.x, event.y
    target = canvas.find_withtag("target")
    if target:
        coords = canvas.coords(target[0])
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            canvas.delete("target")  # Remove target if hit
            canvas.create_text(250, 250, text="Hit!", font=("Arial", 20), fill="magenta")
        else:
            canvas.create_text(250, 250, text="Miss!", font=("Arial", 20), fill="magenta")

# Bind mouse click event
canvas.bind("<Button-1>", shoot)
canvas.bind("<Button-1>", create_target)
# Create a button to generate a new target
button = tk.Button(root, text="New Target", command=create_target, bg="magenta", fg="yellow", font=("Arial", 15))
button.pack(pady=10)

# Start the game loop
root.mainloop()
