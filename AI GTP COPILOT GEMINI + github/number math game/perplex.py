import tkinter as tk
import random
import time

# Game configuration
BASES = {'bin': 2, 'dec': 10, 'hex': 16}
COLORS = {'bg': '#0a0a0a', 'text': '#00ff00', 'input': '#ff00ff'}

# Initialize window
root = tk.Tk()
root.title("Base Converter Blitz")
root.geometry("600x400")
root.configure(bg=COLORS['bg'])

# Game variables
score = 0
start_time = time.time()
current_number = 0
source_base = 'dec'
target_base = 'bin'

# Game elements
timer_label = tk.Label(root, text="Time: 00:00", font=('Courier', 14), 
                      bg=COLORS['bg'], fg=COLORS['text'])
timer_label.pack(pady=10)

question_label = tk.Label(root, text="", font=('Courier', 24), 
                         bg=COLORS['bg'], fg=COLORS['text'])
question_label.pack(pady=20)

answer_entry = tk.Entry(root, font=('Courier', 18), bg=COLORS['bg'], 
                       fg=COLORS['input'], insertbackground=COLORS['text'])
answer_entry.pack()

feedback_label = tk.Label(root, text="", font=('Courier', 12), 
                         bg=COLORS['bg'], fg=COLORS['text'])
feedback_label.pack(pady=10)

score_label = tk.Label(root, text=f"Score: {score}", font=('Courier', 14), 
                      bg=COLORS['bg'], fg=COLORS['text'])
score_label.pack()

def generate_question():
    global current_number, source_base, target_base
    current_number = random.randint(0x100, 0xFFF)
    source_base, target_base = random.sample(list(BASES.keys()), 2)
    
    question_text = f"Convert {format_number(current_number, source_base)}"
    question_label.config(text=f"{question_text}\nto {target_base.upper()}")
    answer_entry.delete(0, tk.END)

def format_number(num, base):
    if base == 'bin':
        return bin(num)[2:]
    elif base == 'hex':
        return hex(num)[2:].upper()
    return str(num)

def check_answer(event):
    global score
    try:
        user_answer = int(answer_entry.get(), BASES[target_base])
        if user_answer == current_number:
            score += 10
            feedback_label.config(text="✓ Correct!", fg='#00ff00')
            generate_question()
        else:
            score -= 5
            feedback_label.config(text="✗ Wrong! Try again", fg='#ff0000')
    except:
        feedback_label.config(text="Invalid format!", fg='#ff0000')
    score_label.config(text=f"Score: {score}")

def update_timer():
    elapsed = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed//60:02}:{elapsed%60:02}")
    root.after(1000, update_timer)

def start_game():
    generate_question()
    update_timer()
    answer_entry.focus_set()

answer_entry.bind('<Return>', check_answer)
start_game()
root.mainloop()
