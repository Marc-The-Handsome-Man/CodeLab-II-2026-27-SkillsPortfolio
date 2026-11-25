
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import os

# Main Window
root = tk.Tk()
root.title("Student Manager")
root.geometry("750x650")
root.resizable(False, False)

# Font
FONT = "Comic Sans MS"

# Background Image
background_image = Image.open(
    r"Frozen.jpg"
)
background_image = background_image.resize((750, 650), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=img, borderwidth=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()

# Colors for the boxes
CARD = "#111111"
BLACK = "#000000"
WHITE = "#FFFFFF"
GRAY = "#CCCCCC"

# Student variables
students = []

# File location
file_name = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

# Load the students from the txt file
def load():
    students.clear()
    try:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
        for line in lines[1:]:
            data = line.strip().split(",")
            students.append([
                data[0],
                data[1],
                int(data[2]),
                int(data[3]),
                int(data[4]),
                int(data[5])
            ])
    except:
        messagebox.showerror("Error", "Cannot open studentMarks.txt")

# Save students into the file
def save():
    file = open(file_name, "w")
    file.write(str(len(students)) + "\n")
    for s in students:
        file.write(
            s[0] + "," + s[1] + "," +
            str(s[2]) + "," +
            str(s[3]) + "," +
            str(s[4]) + "," +
            str(s[5]) + "\n"
        )
    file.close()

# Calculates percentage
def percentage(s):
    total = s[2] + s[3] + s[4] + s[5]
    return total / 160 * 100

# Calculate the grades of students
def grade(s):
    mark = percentage(s)
    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"

# Display students w/ grades etc
def display(s):
    coursework = s[2] + s[3] + s[4]
    output.insert("end", "Name: " + s[1] + "\n")
    output.insert("end", "Student Number: " + s[0] + "\n")
    output.insert("end", "Coursework: " + str(coursework) + "/60\n")
    output.insert("end", "Exam Mark: " + str(s[5]) + "/100\n")
    output.insert("end", "Overall Percentage: " + str(round(percentage(s), 2)) + "%\n")
    output.insert("end", "Grade: " + grade(s) + "\n")
    output.insert("end", "------------------------------\n\n")

# Clear output
def clear():
    output.delete("1.0", "end")

# View all students
def view_all():
    clear()
    average = 0
    for s in students:
        display(s)
        average = average + percentage(s)
    if len(students) > 0:
        average = average / len(students)
    output.insert("end", "\nCLASS SUMMARY\n")
    output.insert("end", "Number of students: " + str(len(students)) + "\n")
    output.insert("end", "Class average: " + str(round(average, 2)) + "%")

# View individual student
def view_one():
    code = simpledialog.askstring("Search", "Enter student number:")
    if code == None:
        return
    clear()
    found = False
    for s in students:
        if s[0] == code:
            display(s)
            found = True
    if found == False:
        messagebox.showinfo("Error", "Student not found!")

# Highest mark
def highest():
    if len(students) == 0:
        messagebox.showinfo("Error", "No students available!")
        return
    best = students[0]
    for s in students:
        if percentage(s) > percentage(best):
            best = s
    clear()
    output.insert("end", "HIGHEST STUDENT\n\n")
    display(best)

# Lowest mark
def lowest():
    if len(students) == 0:
        messagebox.showinfo("Error", "No students available!")
        return
    worst = students[0]
    for s in students:
        if percentage(s) < percentage(worst):
            worst = s
    clear()
    output.insert("end", "LOWEST STUDENT\n\n")
    display(worst)

# Sort students
def sort_students():
    if len(students) == 0:
        messagebox.showinfo("Error", "No students available!")
        return
    choice = simpledialog.askstring(
        "Sort Students",
        "Enter A for Ascending or D for Descending:"
    )
    if choice == None:
        return
    if choice.upper() != "A" and choice.upper() != "D":
        messagebox.showerror("Error", "Please enter A or D!")
        return
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            if choice.upper() == "A":
                if percentage(students[i]) > percentage(students[j]):
                    temp = students[i]
                    students[i] = students[j]
                    students[j] = temp
            else:
                if percentage(students[i]) < percentage(students[j]):
                    temp = students[i]
                    students[i] = students[j]
                    students[j] = temp
    view_all()

# Adds student
def add_student():
    code = simpledialog.askstring("Add Student", "Enter student number:")
    if code == None:
        return
    if len(code) != 4 or not code.isdigit():
        messagebox.showerror("Error", "Student number must be 4 digits!")
        return
    for s in students:
        if s[0] == code:
            messagebox.showerror("Error", "Student already exists!")
            return
    name = simpledialog.askstring("Add Student", "Enter student name:")
    if name == None or name.strip() == "":
        return
    mark1 = simpledialog.askinteger("Add Student", "Course mark 1 (0-20):")
    mark2 = simpledialog.askinteger("Add Student", "Course mark 2 (0-20):")
    mark3 = simpledialog.askinteger("Add Student", "Course mark 3 (0-20):")
    exam = simpledialog.askinteger("Add Student", "Exam mark (0-100):")
    if mark1 == None or mark2 == None or mark3 == None or exam == None:
        return
    if mark1 < 0 or mark1 > 20:
        messagebox.showerror("Error", "Invalid course mark!")
        return
    if mark2 < 0 or mark2 > 20:
        messagebox.showerror("Error", "Invalid course mark!")
        return
    if mark3 < 0 or mark3 > 20:
        messagebox.showerror("Error", "Invalid course mark!")
        return
    if exam < 0 or exam > 100:
        messagebox.showerror("Error", "Invalid exam mark!")
        return
    students.append([code, name, mark1, mark2, mark3, exam])
    save()
    messagebox.showinfo("Success", "Student added successfully!")

# Removes student
def delete_student():
    code = simpledialog.askstring("Delete Student", "Enter student number:")
    if code == None:
        return
    for s in students:
        if s[0] == code:
            students.remove(s)
            save()
            messagebox.showinfo("Success", "Student deleted!")
            return
    messagebox.showerror("Error", "Student not found!")

# Updates student
def update_student():
    code = simpledialog.askstring("Update Student", "Enter student number:")
    if code == None:
        return
    for s in students:
        if s[0] == code:
            name = simpledialog.askstring(
                "Update Student", "Enter new name:", initialvalue=s[1]
            )
            if name == None or name.strip() == "":
                return
            mark1 = simpledialog.askinteger(
                "Update Student", "Course mark 1:", initialvalue=s[2]
            )
            mark2 = simpledialog.askinteger(
                "Update Student", "Course mark 2:", initialvalue=s[3]
            )
            mark3 = simpledialog.askinteger(
                "Update Student", "Course mark 3:", initialvalue=s[4]
            )
            exam = simpledialog.askinteger(
                "Update Student", "Exam mark:", initialvalue=s[5]
            )
            if mark1 == None or mark2 == None or mark3 == None or exam == None:
                return
            if mark1 < 0 or mark1 > 20 or mark2 < 0 or mark2 > 20:
                messagebox.showerror("Error", "Invalid coursework marks!")
                return
            if mark3 < 0 or mark3 > 20 or exam < 0 or exam > 100:
                messagebox.showerror("Error", "Invalid marks!")
                return
            s[1] = name
            s[2] = mark1
            s[3] = mark2
            s[4] = mark3
            s[5] = exam
            save()
            messagebox.showinfo("Success", "Student updated!")
            return
    messagebox.showerror("Error", "Student not found!")

# Main window design
main_frame = tk.Frame(root, bg=CARD)
main_frame.pack(padx=35, pady=15, fill="both", expand=True)

# Title
title = tk.Label(
    main_frame,
    text="✦ STUDENT MANAGER ✦",
    font=(FONT, 22, "bold"),
    bg=CARD,
    fg=WHITE
)
title.pack(pady=10)

# Menu buttons
button_frame = tk.Frame(main_frame, bg=CARD)
button_frame.pack()

# Button design
def create_button(text, command):
    tk.Button(
        button_frame,
        text=text,
        font=(FONT, 11, "bold"),
        bg=WHITE,
        fg=BLACK,
        activebackground=GRAY,
        activeforeground=BLACK,
        width=27,
        relief="flat",
        cursor="hand2",
        command=command
    ).pack(pady=3)

create_button("1. View All Students", view_all)
create_button("2. View Individual Student", view_one)
create_button("3. Highest Mark", highest)
create_button("4. Lowest Mark", lowest)
create_button("5. Sort Students", sort_students)
create_button("6. Add Student", add_student)
create_button("7. Delete Student", delete_student)
create_button("8. Update Student", update_student)

# Output area
output_frame = tk.Frame(main_frame, bg=CARD)
output_frame.pack(pady=10)

output = tk.Text(
    output_frame,
    height=10,
    width=85,
    font=(FONT, 10),
    bg=WHITE,
    fg=BLACK,
    insertbackground=BLACK,
    relief="flat",
    wrap="word"
)
output.pack(side="left")

scrollbar = tk.Scrollbar(output_frame, command=output.yview)
scrollbar.pack(side="right", fill="y")
output.config(yscrollcommand=scrollbar.set)

# Load students
load()

# Run Program
root.mainloop()