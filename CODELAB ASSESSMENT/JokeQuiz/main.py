import tkinter as tk
import random
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Joke Telling Assistant")
root.geometry("500x400")
root.attributes("-fullscreen", False)
root.resizable(False, False)

# Background Image
bg_image = Image.open("Frozen.jpg")
bg_image = bg_image.resize((500, 400))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Read Jokes From File
file = open("JokeQuiz/randomJokes.txt", "r")
jokes = file.readlines()
file.close()

# Variables
current_joke = ""
current_punchline = ""
FONT = "Comic Sans MS"

# Tells Jokes
def tellJoke():
    global current_joke, current_punchline

    current_joke = random.choice(jokes)
    parts = current_joke.split("?")
    setup = parts[0] + "?"
    current_punchline = parts[1].strip()

    setup_label.config(text=setup)
    punchline_label.pack_forget()

# Shows the punchline
def showPunchline():
    punchline_label.config(text=current_punchline)
    punchline_label.pack(pady=10, before=button_frame)

# Next joke
def nextJoke():
    tellJoke()

# Title
tk.Label(
    root,
    text="JOKE TELLING ASSISTANT",
    font=(FONT, 20, "bold"),
    bg="black",
    fg="white"
).pack(pady=25)

# Jokes Setup
setup_label = tk.Label(
    root,
    text="Click the button to get a joke!",
    font=(FONT, 14),
    bg="black",
    fg="white",
    wraplength=450
)
setup_label.pack(pady=20)

# Punchlines
punchline_label = tk.Label(
    root,
    text="",
    font=(FONT, 14),
    bg="black",
    fg="white",
    wraplength=450
)

# Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack()

tk.Button(
    button_frame,
    text="Alexa tell me a Joke",
    font=(FONT, 12),
    bg="white",
    fg="black",
    command=tellJoke
).pack(pady=5)

tk.Button(
    button_frame,
    text="Show Punchline",
    font=(FONT, 12),
    bg="white",
    fg="black",
    command=showPunchline
).pack(pady=5)

tk.Button(
    button_frame,
    text="Next Joke",
    font=(FONT, 12),
    bg="white",
    fg="black",
    command=nextJoke
).pack(pady=5)

tk.Button(
    button_frame,
    text="Quit",
    font=(FONT, 12),
    bg="white",
    fg="black",
    command=root.destroy
).pack(pady=5)

root.mainloop()
