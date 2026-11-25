from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random

# Main Window
root = Tk()
root.title("Arithmetic Quiz")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="black")

# Font
FONT = "Comic Sans MS"

# Background Image
background_image = Image.open(
    r"C:Frozen.jpg"
)
background_image = background_image.resize((700, 550), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=img, borderwidth=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()

# Colors for the boxes
CARD = "#111111"
WHITE = "#FFFFFF"
PURPLE = "#FFFFFF"
GREEN = "#FFFFFF"
RED = "#AAAAAA"
YELLOW = "#FFFFFF"
GRAY = "#CCCCCC"

# Quiz variables
score = 0
question = 0
attempt = 0
num1 = 0
num2 = 0
operation = ""
answer = 0
minimum = 0
maximum = 9

# Clear Screen
def clear():
    for widget in root.winfo_children():
        if widget != background_label:
            widget.destroy()
    background_label.lower()

# Title
def createTitle(subtitle):
    frame = Frame(root, bg=CARD)
    frame.pack(fill="x", padx=60, pady=(20, 5))
    Label(frame, text="✦ ARITHMETIC QUIZ ✦", font=(FONT, 25, "bold"), bg=CARD, fg=WHITE).pack(pady=(12, 5))
    Label(frame, text=subtitle, font=(FONT, 11), bg=CARD, fg=GRAY).pack(pady=(0, 12))

# Difficulty menu
def displayMenu():
    clear()
    createTitle("CHALLENGE YOUR MATHEMATICAL SKILLS")
    card = Frame(root, bg=CARD, padx=30, pady=15)
    card.pack(padx=100, pady=10)
    Label(card, text="SELECT DIFFICULTY", font=(FONT, 19, "bold"), bg=CARD, fg=WHITE).pack(pady=10)
    Label(card, text="Choose your level to begin!", font=(FONT, 11), bg=CARD, fg=GRAY).pack(pady=5)
    Button(card, text="1. EASY", font=(FONT, 14, "bold"), bg=WHITE, fg="black", width=22, height=2, relief="flat", cursor="hand2", command=lambda: startQuiz(1)).pack(pady=8)
    Button(card, text="2. MODERATE", font=(FONT, 14, "bold"), bg=WHITE, fg="black", width=22, height=2, relief="flat", cursor="hand2", command=lambda: startQuiz(2)).pack(pady=8)
    Button(card, text="3. ADVANCED", font=(FONT, 14, "bold"), bg=WHITE, fg="black", width=22, height=2, relief="flat", cursor="hand2", command=lambda: startQuiz(3)).pack(pady=8)
    Label(root, text="10 QUESTIONS  •  100 MAXIMUM POINTS", font=(FONT, 10, "bold"), bg=CARD, fg=WHITE).pack(pady=10)

# Start Quiz
def startQuiz(level):
    global minimum, maximum, score, question
    score = 0
    question = 0
    if level == 1:
        minimum = 0
        maximum = 9
    elif level == 2:
        minimum = 10
        maximum = 99
    else:
        minimum = 9999
        maximum = 999999
    nextQuestion()

# Random Number
def randomInt():
    return random.randint(minimum, maximum)

# Random operation
def decideOperation():
    return random.choice(["+", "-", "*"])

# Display the questions
def displayProblem():
    global num1, num2, operation, answer, attempt
    global answer_entry, feedback
    clear()
    attempt = 1
    num1 = randomInt()
    num2 = randomInt()
    operation = decideOperation()
    if operation == "+":
        answer = num1 + num2
    elif operation == "*":
        answer = num1 * num2
    else:
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
    createTitle("SOLVE THE FOLLOWING PROBLEM")

    # Information card
    info = Frame(root, bg=CARD)
    info.pack(fill="x", padx=60, pady=8)
    Label(info, text=f"QUESTION {question} / 10", font=(FONT, 13, "bold"), bg=CARD, fg=WHITE).pack(side="left", padx=20, pady=12)
    Label(info, text=f"SCORE: {score}", font=(FONT, 13, "bold"), bg=CARD, fg=YELLOW).pack(side="right", padx=20, pady=12)

    # Question card
    card = Frame(root, bg=CARD, padx=30, pady=10)
    card.pack(fill="x", padx=60, pady=10)
    Label(card, text="WHAT IS THE ANSWER?", font=(FONT, 12, "bold"), bg=CARD, fg=GRAY).pack(pady=5)
    Label(card, text=f"{num1}  {operation}  {num2} = ?", font=(FONT, 32, "bold"), bg=CARD, fg=WHITE).pack(pady=15)

    # Answer entry
    Label(root, text="ENTER YOUR ANSWER", font=(FONT, 11, "bold"), bg=CARD, fg=WHITE).pack(pady=5)
    answer_entry = Entry(root, font=(FONT, 19), justify="center", width=15, bg=WHITE, fg="black", relief="flat")
    answer_entry.pack(ipady=6, pady=5)
    answer_entry.focus()
    feedback = Label(root, text="You have 2 attempts!", font=(FONT, 12, "bold"), bg=CARD, fg=GRAY)
    feedback.pack(pady=5)
    Button(root, text="SUBMIT ANSWER", font=(FONT, 13, "bold"), bg=WHITE, fg="black", width=22, height=2, relief="flat", cursor="hand2", command=isCorrect).pack(pady=10)
    root.bind("<Return>", lambda event: isCorrect())

# Checks your answer
def isCorrect():
    global score, attempt
    user_answer = answer_entry.get().strip()
    if user_answer == "":
        messagebox.showwarning("Warning", "Please enter an answer!")
        return
    try:
        user_answer = int(user_answer)
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a whole number!")
        return
    if user_answer == answer:
        if attempt == 1:
            score += 10
            feedback.config(text="✓ CORRECT! +10 POINTS", fg=WHITE)
        else:
            score += 5
            feedback.config(text="✓ CORRECT! +5 POINTS", fg=WHITE)
        root.after(1000, nextQuestion)
    else:
        if attempt == 1:
            attempt = 2
            feedback.config(text="✗ WRONG! TRY ONE MORE TIME.", fg=GRAY)
            answer_entry.delete(0, END)
            answer_entry.focus()
        else:
            feedback.config(text=f"✗ WRONG! ANSWER: {answer}", fg=RED)
            root.after(1500, nextQuestion)

# Gives the next question
def nextQuestion():
    global question
    root.unbind("<Return>")
    question += 1
    if question <= 10:
        displayProblem()
    else:
        displayResults()

# For the results screen
def displayResults():
    clear()
    createTitle("YOU HAVE COMPLETED THE QUIZ!")
    card = Frame(root, bg=CARD, padx=40, pady=15)
    card.pack(padx=100, pady=5)
    Label(card, text="🏆", font=(FONT, 40), bg=CARD, fg=YELLOW).pack()
    Label(card, text="FINAL SCORE", font=(FONT, 14, "bold"), bg=CARD, fg=GRAY).pack(pady=5)
    Label(card, text=f"{score} / 100", font=(FONT, 35, "bold"), bg=CARD, fg=YELLOW).pack(pady=5)
    if score > 90:
        grade = "A+"
        comment = "Outstanding Performance!"
    elif score >= 80:
        grade = "A"
        comment = "Excellent Work!"
    elif score >= 70:
        grade = "B"
        comment = "Great Job!"
    elif score >= 60:
        grade = "C"
        comment = "Good Effort!"
    elif score >= 50:
        grade = "D"
        comment = "Keep Practicing!"
    else:
        grade = "F"
        comment = "Don't Give Up!"
    Label(card, text=f"GRADE: {grade}", font=(FONT, 23, "bold"), bg=CARD, fg=WHITE).pack(pady=5)
    Label(card, text=comment, font=(FONT, 12), bg=CARD, fg=GRAY).pack(pady=5)
    Label(root, text="Would you like to play again?", font=(FONT, 12, "bold"), bg=CARD, fg=WHITE).pack(pady=10)
    Button(root, text="PLAY AGAIN", font=(FONT, 12, "bold"), bg=WHITE, fg="black", width=20, height=2, relief="flat", cursor="hand2", command=displayMenu).pack(pady=5)
    Button(root, text="EXIT", font=(FONT, 12, "bold"), bg=WHITE, fg="black", width=20, height=2, relief="flat", cursor="hand2", command=root.destroy).pack(pady=5)

# Run Program
displayMenu()
root.mainloop()
