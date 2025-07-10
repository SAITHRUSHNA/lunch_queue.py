import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# === Force database to save in script's folder ===
db_path = os.path.join(os.path.dirname(__file__), "lunch_queue.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === Create table if it doesn't exist ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
conn.commit()

# === Functions ===

# Add a name to the queue and store in database
def add_to_queue():
    name = name_entry.get().strip()
    if name:
        cursor.execute("INSERT INTO queue (name) VALUES (?)", (name,))
        conn.commit()
        name_entry.delete(0, tk.END)
        update_queue_display()
    else:
        messagebox.showwarning("Input Error", "Please enter a name")

# Serve the first person (dequeue)
def serve_lunch():
    cursor.execute("SELECT id, name FROM queue ORDER BY id ASC LIMIT 1")
    first = cursor.fetchone()
    if first:
        cursor.execute("DELETE FROM queue WHERE id = ?", (first[0],))
        conn.commit()
        messagebox.showinfo("Served", f"{first[1]} has been served lunch.")
        update_queue_display()
    else:
        messagebox.showinfo("Queue Empty", "No one is in the queue.")

# Display the current queue
def update_queue_display():
    queue_listbox.delete(0, tk.END)
    cursor.execute("SELECT name FROM queue ORDER BY id ASC")
    for row in cursor.fetchall():
        queue_listbox.insert(tk.END, row[0])

# Print the queue to the terminal (debug feature)
def print_queue_to_console():
    cursor.execute("SELECT * FROM queue")
    all_rows = cursor.fetchall()
    print("Current Queue:")
    for row in all_rows:
        print(row)

# === GUI Setup ===
root = tk.Tk()
root.title("Lunch Queue")
root.geometry("300x350")

tk.Label(root, text="Enter Name:").pack(pady=5)
name_entry = tk.Entry(root, width=25)
name_entry.pack(pady=5)

tk.Button(root, text="Add to Queue", command=add_to_queue).pack(pady=5)
tk.Button(root, text="Serve Lunch", command=serve_lunch).pack(pady=5)
tk.Button(root, text="Print Queue in Console", command=print_queue_to_console).pack(pady=5)

tk.Label(root, text="Current Queue:").pack(pady=5)
queue_listbox = tk.Listbox(root, width=30, height=10)
queue_listbox.pack(pady=5)

update_queue_display()  # Load initial data

# Close DB when window closes
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()