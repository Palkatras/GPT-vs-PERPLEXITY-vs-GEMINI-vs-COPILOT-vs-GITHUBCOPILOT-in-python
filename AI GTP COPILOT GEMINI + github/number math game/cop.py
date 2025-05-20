import tkinter as tk
import random

# Initialize the window
root = tk.Tk()
root.title("Algorithmic Math Game")
root.geometry("500x300")
root.configure(bg="black")

# Available number bases
BASES = {
    "Decimal": lambda x: str(x),
    "Hexadecimal": lambda x: hex(x)[2:].upper(),
    "Binary": lambda x: bin(x)[2:],
    "Octal": lambda x: oct(x)[2:]
}

# Generate a new problem
def generate_problem():
    global number, correct_answer, chosen_base
    
    number = random.randint(10, 500)  # Random number
    chosen_base = random.choice(list(BASES.keys()))  # Pick a random format
    correct_answer = BASES[chosen_base](number)  # Convert to selected format

    prompt_label.config(text=f"Convert this {chosen_base} number to Decimal:\n{correct_answer}")
    entry.delete(0, tk.END)
    feedback_label.config(text="")

# Check the answer
def check_answer():
    user_input = entry.get().strip()
    if user_input.isdigit() and int(user_input) == number:
        feedback_label.config(text="Correct!", fg="lime")
    else:
        feedback_label.config(text="Wrong! Try again.", fg="red")

# UI Elements
prompt_label = tk.Label(root, text="", font=("Arial", 16), bg="black", fg="yellow")
prompt_label.pack(pady=20)

entry = tk.Entry(root, font=("Arial", 14), bg="magenta", fg="black")
entry.pack(pady=10)

check_button = tk.Button(root, text="Check Answer", command=check_answer, bg="yellow", fg="black", font=("Arial", 12))
check_button.pack()

new_problem_button = tk.Button(root, text="New Problem", command=generate_problem, bg="magenta", fg="black", font=("Arial", 12))
new_problem_button.pack()

feedback_label = tk.Label(root, text="", font=("Arial", 14), bg="black")
feedback_label.pack(pady=10)

# Start the first problem
generate_problem()

root.mainloop()
