from model import DatabaseAPI
import tkinter as tk
from tkinter import TclError, messagebox
from tkinter.ttk import Label, Entry, Button, Spinbox, Treeview


class BookManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseAPI()

        self.title("Bücherverwaltung")

        # Hauptcontainer 
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
        # Frame zur Kontrolle der Button
        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Hauptfenster Config
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        for i in range(1):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)
        
        # zwei Zeilen; zwei Spalten Buttons
        for i in range(1):
            self.btn_frame.rowconfigure(i, weight=1)
            self.btn_frame.columnconfigure(i, weight=1)

        self.data_tree = Treeview(self.frame)
        self.data_tree.grid(column=0, row=0)

        self.btn_all_books = Button(self.btn_frame, text="Alle Bücher", command=self.all_books_func)
        self.btn_all_books.grid(column=0, row=0)

        self.btn_quit = Button(self.btn_frame, text="Beenden", command=self.destroy)
        self.btn_quit.grid(column=0, row=99)

    def all_books_func(self):
        self.data_tree['columns'] = ["Author", "Genre"]
        self.data_tree.heading('#0', text="Title")
        self.data_tree.heading('Author', text="Autor")
        self.data_tree.heading('Genre', text="Genre")
        all_books = self.db.get_books_by_genre("Fantasy")
        if len(all_books) > 0:
            for book in all_books:
                self.data_tree.insert(
                    "",
                    tk.END,
                    text=book.title,
                    values=(book.author.name, book.genre.name)
                )

if __name__ == "__main__":
    app = BookManagementApp()
    app.mainloop()