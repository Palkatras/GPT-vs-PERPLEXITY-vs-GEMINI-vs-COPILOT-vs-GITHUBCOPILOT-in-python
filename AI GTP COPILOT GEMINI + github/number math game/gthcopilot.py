import tkinter as tk
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 350
BG_COLOR = "#FFFF00"       # Yellow
FG_COLOR = "#FF00FF"       # Magenta
ENTRY_BG = "white"
ENTRY_FG = "#FF00FF"

FORMATS = ['Decimal', 'Hexadecimal', 'Binary']
TO_FUNC = {
    'Decimal': lambda n: str(n),
    'Hexadecimal': lambda n: hex(n)[2:].upper(),
    'Binary': lambda n: bin(n)[2:]
}

score = 0
current_number = 0
question_format = ""
answer_format = ""
question_text_id = None
info_text_id = None

def pick_formats():
    qf, af = random.sample(FORMATS, 2)
    return qf, af

def new_question(canvas, entry, score_label):
    global current_number, question_format, answer_format, question_text_id, info_text_id
    current_number = random.randint(10, 255)
    question_format, answer_format = pick_formats()

    display = TO_FUNC[question_format](current_number)
    question_str = f"Convert {display} ({question_format}) to {answer_format}:"
    canvas.delete("question")
    question_text_id = canvas.create_text(
        WINDOW_WIDTH//2, 80, text=question_str,
        fill=FG_COLOR, font=("Arial", 18, "bold"), tags="question"
    )
    canvas.delete("info")
    info_text_id = canvas.create_text(
        WINDOW_WIDTH//2, 180, text="", fill=FG_COLOR,
        font=("Arial", 14, "bold"), tags="info"
    )
    entry.delete(0, tk.END)
    score_label.config(text=f"Score: {score}")

def check_answer(entry, canvas, score_label):
    global score
    user = entry.get().strip().lower()
    correct = TO_FUNC[answer_format](current_number).lower()
    if user == correct:
        res = "Correct!"
        score += 1
        color = FG_COLOR
    else:
        res = f"Wrong! Correct answer: {correct.upper()}"
        color = "red"
        score = 0  # Reset score on wrong answer
    canvas.delete("info")
    canvas.create_text(
        WINDOW_WIDTH//2, 180, text=res,
        fill=color, font=("Arial", 14, "bold"), tags="info"
    )
    score_label.config(text=f"Score: {score}")
    canvas.after(1200, lambda: new_question(canvas, entry, score_label))

def main():
    root = tk.Tk()
    root.title("Super Math Converter Game")

    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR, highlightthickness=0)
    canvas.pack()

    score_label = tk.Label(root, text="Score: 0", fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 16, "bold"))
    score_label.place(x=WINDOW_WIDTH//2-50, y=20)

    entry = tk.Entry(root, font=("Arial", 16), bg=ENTRY_BG, fg=ENTRY_FG, justify='center')
    entry.place(x=WINDOW_WIDTH//2-75, y=120, width=150, height=35)

    submit_btn = tk.Button(root, text="Submit", font=("Arial", 14, "bold"),
                           bg=FG_COLOR, fg=BG_COLOR, activebackground=BG_COLOR,
                           command=lambda: check_answer(entry, canvas, score_label))
    submit_btn.place(x=WINDOW_WIDTH//2-50, y=170, width=100, height=35)

    root.bind("<Return>", lambda event: check_answer(entry, canvas, score_label))

    new_question(canvas, entry, score_label)
    root.mainloop()

if __name__ == '__main__':
    main()