import tkinter as tk
import random

# --- CONFIG ---
FORMATS = ['dec', 'bin', 'hex', 'oct']
SCORE = 0
QUESTION = {}

# --- GUI SETUP ---
root = tk.Tk()
root.title("Number Base Blaster!")
root.geometry("600x400")
root.configure(bg="black")

# Magenta-yellow theme
fg_color = "yellow"
bg_color = "black"
highlight_color = "magenta"

label_question = tk.Label(root, text="", font=("Courier", 20), fg=fg_color, bg=bg_color)
label_question.pack(pady=20)

entry_answer = tk.Entry(root, font=("Courier", 20), fg=highlight_color, bg="black", insertbackground="white")
entry_answer.pack()

label_feedback = tk.Label(root, text="", font=("Courier", 16), fg=fg_color, bg=bg_color)
label_feedback.pack(pady=10)

label_score = tk.Label(root, text="Score: 0", font=("Courier", 18), fg=highlight_color, bg=bg_color)
label_score.pack(pady=20)

# --- FUNCTIONS ---

def generate_question():
    global QUESTION
    number = random.randint(1, 255)
    from_format, to_format = random.sample(FORMATS, 2)

    # Convert number to the from_format
    if from_format == 'dec':
        displayed = str(number)
    elif from_format == 'bin':
        displayed = bin(number)
    elif from_format == 'hex':
        displayed = hex(number)
    elif from_format == 'oct':
        displayed = oct(number)

    QUESTION = {
        "number": number,
        "from": from_format,
        "to": to_format,
        "displayed": displayed
    }

    label_question.config(
        text=f"Convert {displayed} from {from_format.upper()} to {to_format.upper()}:"
    )
    entry_answer.delete(0, tk.END)
    label_feedback.config(text="")

def check_answer(event=None):
    global SCORE
    user_input = entry_answer.get().strip().lower()
    correct = ""

    number = QUESTION["number"]
    to_format = QUESTION["to"]

    if to_format == 'dec':
        correct = str(number)
    elif to_format == 'bin':
        correct = bin(number)[2:]
    elif to_format == 'hex':
        correct = hex(number)[2:]
    elif to_format == 'oct':
        correct = oct(number)[2:]

    if user_input == correct:
        SCORE += 1
        label_feedback.config(text="✅ Correct!", fg="lime")
    else:
        label_feedback.config(text=f"❌ Wrong! Correct: {correct}", fg="red")

    label_score.config(text=f"Score: {SCORE}")
    root.after(1000, generate_question)

# --- START ---
entry_answer.bind("<Return>", check_answer)
generate_question()

root.mainloop()
