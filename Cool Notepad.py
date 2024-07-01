import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox


# Function to open a file
def open_file():
    if check_unsaved_changes():
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    text.delete(1.0, tk.END)
                    text.insert(tk.END, file.read())
                    root.title(f"Cool Notepad - {file_path}")
                    update_status_bar(f"Opened: {file_path}")
                    global current_file
                    current_file = file_path
                    global unsaved_changes
                    unsaved_changes = False
                messagebox.showinfo("Success", "Note opened successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open note: {e}")


# Function to save the current file
def save_file():
    global current_file
    if current_file:
        file_path = current_file
    else:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(text.get(1.0, tk.END))
                root.title(f"Cool Notepad - {file_path}")
                update_status_bar(f"Current File: {file_path}")
                current_file = file_path
                global unsaved_changes
                unsaved_changes = False
            messagebox.showinfo("Success", "Note saved successfully.")
        except Exception as e:
            messagebox.showerror(f"Error", "Failed to save note: {e}")


# Function to handle text modification event
def on_text_change(event=None):
    global unsaved_changes
    unsaved_changes = True


# Function to check for unsaved changes and prompt user
def check_unsaved_changes():
    if unsaved_changes:
        answer = messagebox.askyesnocancel(
            "Unsaved Changes", "You have unsaved changes. Do you want to save them?"
        )
        if answer is True:
            save_file()
            return True
        elif answer is False:
            return True
        else:
            return False
    return True


# Function to handle window closing event
def on_closing():
    if check_unsaved_changes():
        root.quit()


# Update status bar text dynamically with cursor position
def update_status_bar(event=None):
    line, column = map(str, text.index(tk.INSERT).split("."))
    status_bar_text.set(f"Line: {line}, Column: {column}")


# Create the main window
root = tk.Tk()
root.title("Cool Notepad")

# Create a scrolled text widget
text = scrolledtext.ScrolledText(root, font=("Courier New", 10))
text.pack(expand=True, fill="both")

# Track changes in the text widget
text.bind("<<Modified>>", on_text_change)

# Bind cursor movement and text insert events to update status bar
text.bind("<Motion>", update_status_bar)
text.bind("<Key>", update_status_bar)

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing)

# Bind keyboard shortcuts
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())

# Create a status bar
status_bar_text = tk.StringVar()
status_bar_text.set("Line: 1, Column: 0")
status_bar = tk.Label(
    root, textvariable=status_bar_text, bd=1, relief=tk.SUNKEN, anchor=tk.W
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Initialize state
current_file = None
unsaved_changes = False

# Override the window close button
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI main loop
root.mainloop()
