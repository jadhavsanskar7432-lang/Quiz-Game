import tkinter as tk
from tkinter import messagebox
import json
import os

with open("questions.json", "r") as f:
    questions = json.load(f)

if os.path.exists("highscore.json"):
    with open("highscore.json", "r") as f:
        highscore = json.load(f).get("highscore", 0)
else:
    highscore = 0

score = 0
current_question = 0

def check_answer(option):
    global score, current_question
    if option == questions[current_question]["answer"]:
        score += 1
    current_question += 1
    if current_question < len(questions):
        show_question()
    else:
        show_result()

def show_question():
    q = questions[current_question]
    question_label.config(text=q["question"])
    for i, btn in enumerate(option_buttons):
        btn.config(text=q["options"][i])

def show_result():
    global highscore
    if score > highscore:
        highscore = score
        with open("highscore.json", "w") as f:
            json.dump({"highscore": highscore}, f)
        msg = f"🎉 {name_entry.get()}, New High Score!\nYour score: {score}/{len(questions)}"
    else:
        msg = f"{name_entry.get()}, your score: {score}/{len(questions)}\nHigh Score: {highscore}"
    messagebox.showinfo("Quiz Result", msg)
    root.destroy()

def start_quiz():
    global name
    name = name_entry.get()
    if not name.strip():
        messagebox.showwarning("Name Required", "Please enter your name to start!")
        return
    name_label.config(text=f"Welcome, {name}!")
    name_entry.pack_forget()
    start_button.pack_forget()
    question_label.pack(pady=20)
    for btn in option_buttons:
        btn.pack(pady=5)
    show_question()

root = tk.Tk()
root.title("Quiz App")
root.geometry("450x450")

name_label = tk.Label(root, text="Enter your name:", font=("Arial", 14))
name_label.pack(pady=10)

name_entry = tk.Entry(root, font=("Arial", 14))
name_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Quiz", font=("Arial", 14), command=start_quiz)
start_button.pack(pady=10)

question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=420)

option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 14), width=20,
                    command=lambda i=i: check_answer(option_buttons[i]['text']))
    option_buttons.append(btn)

root.mainloop()
