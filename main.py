import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

FILE_NAME = "birthdays.json"

# Load birthdays from JSON file
def load_birthdays():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

# Save birthdays to JSON file
def save_birthdays(birthdays):
    with open(FILE_NAME, "w") as f:
        json.dump(birthdays, f)

# Add birthday
def add_birthday():
    name = name_entry.get().strip()
    date = date_entry.get().strip()
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        messagebox.showwarning("Error", "Please enter date as DD-MM-YYYY")
        return

    if name and date:
        birthdays[name] = date
        save_birthdays(birthdays)
        messagebox.showinfo("Success", f"Birthday for {name} added!")
        name_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        refresh_table()
    else:
        messagebox.showwarning("Error", "Please enter both name and date")

# Exit app
def exit_app():
    root.destroy()

# Refresh table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    today = datetime.today().strftime("%d-%m")
    for name, date_str in birthdays.items():
        if date_str[:5] == today:
            message = f"It’s {name}’s birthday!!!! Wish them a very happy birthday 🎂🎈"
            tree.insert("", tk.END, values=(name, date_str, message), tags=('today',))
        else:
            tree.insert("", tk.END, values=(name, date_str, ""), tags=('normal',))

# Show upcoming birthdays in next 'days'
def highlight_upcoming(days=7):
    today = datetime.today()
    upcoming_list = []
    for name, date_str in birthdays.items():
        bday = datetime.strptime(date_str, "%d-%m-%Y").replace(year=today.year)
        delta = (bday - today).days
        if 0 <= delta <= days:
            upcoming_list.append(f"{name} on {bday.strftime('%d-%m-%Y')}")
        elif delta < 0:
            bday_next_year = bday.replace(year=today.year + 1)
            delta_next = (bday_next_year - today).days
            if 0 <= delta_next <= days:
                upcoming_list.append(f"{name} on {bday_next_year.strftime('%d-%m-%Y')}")
    if upcoming_list:
        messagebox.showinfo(f"Birthdays in next {days} days", "\n".join(upcoming_list))

# GUI Setup
root = tk.Tk()
root.title("🎂 Birthday Reminder App 🎉")
root.geometry("650x500")
root.configure(bg="#FFF0F5")

birthdays = load_birthdays()

# Title
title_label = tk.Label(root, text="Birthday Reminder", font=("Comic Sans MS", 22, "bold"), fg="#FF1493", bg="#FFF0F5")
title_label.pack(pady=10)

# Entry Frame
entry_frame = tk.Frame(root, bg="#FFF0F5")
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Name:", font=("Arial", 12), bg="#FFF0F5").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(entry_frame, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(entry_frame, text="Birthday (DD-MM-YYYY):", font=("Arial", 12), bg="#FFF0F5").grid(row=1, column=0, padx=5, pady=5)
date_entry = tk.Entry(entry_frame, font=("Arial", 12))
date_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons Frame
button_frame = tk.Frame(root, bg="#FFF0F5")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Birthday", command=add_birthday, bg="#FF69B4", fg="white", font=("Arial", 12), width=18).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Exit", command=exit_app, bg="#1E90FF", fg="white", font=("Arial", 12), width=18).grid(row=0, column=1, padx=10, pady=5)

# Treeview Table Frame
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

tree = ttk.Treeview(tree_frame, columns=("Name", "Birthday", "Message"), show="headings", height=10)
tree.heading("Name", text="Name")
tree.heading("Birthday", text="Birthday")
tree.heading("Message", text="Message")
tree.column("Name", width=150)
tree.column("Birthday", width=120)
tree.column("Message", width=350)
tree.pack()

# Style for today’s birthdays
tree.tag_configure('today', background="#FF4500", foreground="white", font=("Arial", 12, "bold"))  # Bright orange
tree.tag_configure('normal', background="white", foreground="black", font=("Arial", 12))

# Initial table refresh and upcoming birthdays
refresh_table()
highlight_upcoming(7)

root.mainloop()



