from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox, simpledialog, font
import os

# Initialize root
root = Tk()
root.title("Untitled - Advanced Notepad")
root.geometry("800x600")

# Global Variables
current_file = None

# Functions
def new_file():
    global current_file
    current_file = None
    text_area.delete(1.0, END)
    root.title("Untitled - Advanced Notepad")

def open_file():
    global current_file
    file_path = fd.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        root.title(os.path.basename(file_path))
        with open(file_path, "r") as file:
            text_area.delete(1.0, END)
            text_area.insert(1.0, file.read())

def save_file():
    global current_file
    if not current_file:
        save_as_file()
    else:
        with open(current_file, "w") as file:
            file.write(text_area.get(1.0, END))
        messagebox.showinfo("Save", "File saved successfully!")

def save_as_file():
    global current_file
    file_path = fd.asksaveasfilename(defaultextension=".txt",
                                     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        root.title(os.path.basename(file_path))
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, END))
        messagebox.showinfo("Save As", "File saved successfully!")

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def undo_action():
    text_area.event_generate("<<Undo>>")

def redo_action():
    text_area.event_generate("<<Redo>>")

def search_text():
    find_word = simpledialog.askstring("Find", "Enter text to find:")
    if find_word:
        start_idx = text_area.search(find_word, "1.0", END)
        if start_idx:
            end_idx = f"{start_idx}+{len(find_word)}c"
            text_area.tag_add("highlight", start_idx, end_idx)
            text_area.tag_config("highlight", background="yellow", foreground="black")
            text_area.see(start_idx)
        else:
            messagebox.showinfo("Find", f"'{find_word}' not found.")

def replace_text():
    find_word = simpledialog.askstring("Find", "Enter text to find:")
    replace_word = simpledialog.askstring("Replace", "Enter replacement text:")
    if find_word and replace_word:
        content = text_area.get(1.0, END)
        new_content = content.replace(find_word, replace_word)
        text_area.delete(1.0, END)
        text_area.insert(1.0, new_content)

def word_count():
    content = text_area.get(1.0, END)
    words = len(content.split())
    messagebox.showinfo("Word Count", f"Total words: {words}")

def change_font():
    font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
    font_size = simpledialog.askinteger("Font Size", "Enter font size:")
    if font_family and font_size:
        new_font = font.Font(family=font_family, size=font_size)
        text_area.config(font=new_font)

def toggle_theme():
    current_bg = text_area.cget("background")
    if current_bg == "white":
        text_area.config(background="black", foreground="white", insertbackground="white")
    else:
        text_area.config(background="white", foreground="black", insertbackground="black")

# Menubar setup
menubar = Menu(root)

# File Menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=save_as_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Edit Menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=undo_action, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=redo_action, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Find", command=search_text, accelerator="Ctrl+F")
editmenu.add_command(label="Replace", command=replace_text, accelerator="Ctrl+H")
editmenu.add_command(label="Word Count", command=word_count)
menubar.add_cascade(label="Edit", menu=editmenu)

# Format Menu
formatmenu = Menu(menubar, tearoff=0)
formatmenu.add_command(label="Change Font", command=change_font)
menubar.add_cascade(label="Format", menu=formatmenu)

# View Menu
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Toggle Theme", command=toggle_theme)
menubar.add_cascade(label="View", menu=viewmenu)

# Status Bar
status_bar = Label(root, text="Line 1, Column 1", anchor=E)
status_bar.pack(side=BOTTOM, fill=X)

def update_status(event=None):
    row, col = text_area.index(INSERT).split(".")
    status_bar.config(text=f"Line {row}, Column {col}")

# Text Area
text_area = Text(root, wrap="word", undo=True)
text_area.pack(expand=True, fill=BOTH)
text_area.bind("<KeyRelease>", update_status)

# Configure Menubar
root.config(menu=menubar)

# Shortcuts
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-f>", lambda event: search_text())
root.bind("<Control-h>", lambda event: replace_text())
root.bind("<Control-z>", lambda event: undo_action())
root.bind("<Control-y>", lambda event: redo_action())

root.mainloop()

