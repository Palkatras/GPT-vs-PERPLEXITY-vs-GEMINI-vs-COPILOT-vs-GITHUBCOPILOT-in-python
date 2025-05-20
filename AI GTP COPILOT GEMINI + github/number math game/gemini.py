import tkinter as tk
import random

def generate_question():
    """Generates a question with a number in a random base (decimal, binary, hex)."""
    global current_number, current_base, correct_answers
    current_number = random.randint(0, 255)  # Limit to a reasonable range
    current_base = random.choice(['decimal', 'binary', 'hex'])
    correct_answers = {
        'decimal': str(current_number),
        'binary': bin(current_number)[2:],
        'hex': hex(current_number)[2:].upper(),
    }
    if current_base == 'decimal':
        return f"Convert the following decimal number:\n {current_number} to binary and hexadecimal."
    elif current_base == 'binary':
        return f"Convert the following binary number:\n {bin(current_number)[2:]} to decimal and hexadecimal."
    else:
        return f"Convert the following hexadecimal number:\n {hex(current_number)[2:].upper()} to decimal and binary."

def check_answer():
    """Checks the user's answers and updates the score."""
    global score, question_label, decimal_entry, binary_entry, hex_entry, score_label, root

    user_decimal = decimal_entry.get().strip()
    user_binary = binary_entry.get().strip()
    user_hex = hex_entry.get().strip().upper()  # Ensure uppercase for comparison

    is_correct = True
    if current_base != 'decimal' and user_decimal != correct_answers['decimal']:
        is_correct = False
    if current_base != 'binary' and user_binary != correct_answers['binary']:
        is_correct = False
    if current_base != 'hex' and user_hex != correct_answers['hex']:
        is_correct = False

    if is_correct:
        score += 1
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Incorrect!", fg="red")

    score_label.config(text=f"Score: {score}")
    decimal_entry.delete(0, tk.END)
    binary_entry.delete(0, tk.END)
    hex_entry.delete(0, tk.END)
    question_label.config(text=generate_question())  # Generate the next question
    root.focus_set()

# Initialize the game
root = tk.Tk()
root.title("Number Conversion Game")
root.configure(bg="yellow")

question_label = tk.Label(root, text=generate_question(), font=("Arial", 16), bg="yellow", fg="magenta")
question_label.pack(pady=10)

# Create labels and entry fields for decimal, binary, and hex
decimal_label = tk.Label(root, text="Decimal:", bg="yellow", fg="magenta")
decimal_label.pack()
decimal_entry = tk.Entry(root)
decimal_entry.pack()

binary_label = tk.Label(root, text="Binary:", bg="yellow", fg="magenta")
binary_label.pack()
binary_entry = tk.Entry(root)
binary_entry.pack()

hex_label = tk.Label(root, text="Hexadecimal:", bg="yellow", fg="magenta")
hex_label.pack()
hex_entry = tk.Entry(root)
hex_entry.pack()

score = 0
score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), bg="yellow", fg="magenta")
score_label.pack(pady=10)

check_button = tk.Button(root, text="Check Answer", command=check_answer, bg="magenta", fg="yellow")
check_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 16), bg="yellow")
result_label.pack(pady=10)

root.mainloop()
