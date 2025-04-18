from model import DatabaseAPI
import tkinter as tk
from tkinter import TclError, messagebox
from tkinter.ttk import Label, Entry, Button, Spinbox, Treeview, Combobox


class AddBookWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseAPI()

        self.title = "Neues Buch hinzufügen"

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
        # Frame zur Kontrolle der Button
        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Hauptfenster Config
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)
        
        # zwei Zeilen; zwei Spalten Buttons
        for i in range(1):
            self.btn_frame.rowconfigure(i, weight=1)
            self.btn_frame.columnconfigure(i, weight=1)

        self.inAuthor = tk.StringVar()
        self.inTitle = tk.StringVar()

        self.lbl_title = Label(self.frame, text="Titel: ")
        self.lbl_title.grid(row=0, column=0)
        self.in_title = Entry(self.frame, textvariable=self.inTitle)
        self.in_title.grid(row=0, column=1)

        self.lbl_author = Label(self.frame, text="Autor: ")
        self.lbl_author.grid(row=1, column=0)
        self.in_author = Entry(self.frame, textvariable=self.inAuthor)
        self.in_author.grid(row=1, column=1)

        self.lbl_genre = Label(self.frame, text="Genre: ")
        self.lbl_genre.grid(row=2, column=0)
        self.cmb_genre = Combobox(self.frame)
        self.cmb_genre.grid(row=2, column=1)

        self.btn_check = Button(self.btn_frame, text="Hinzufügen", command=self.add_book_func)
        self.btn_check.grid(row=99, column=0, columnspan=2)


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

    def _clear_treeview(self):
        for i in self.data_tree.get_children():
            self.data_tree.delete(i)

    def all_books_func(self):
        self.data_tree['columns'] = ["Author", "Genre"]
        self.data_tree.heading('#0', text="Title")
        self.data_tree.heading('Author', text="Autor")
        self.data_tree.heading('Genre', text="Genre")
        all_books = self.db.get_all_books()
        if len(all_books) > 0:
            self._clear_treeview()
            for book in all_books:
                self.data_tree.insert(
                    "",
                    tk.END,
                    text=book.title,
                    values=(book.author.name, book.genre.name)
                )
        else:
            messagebox.showinfo("Hinweis", "Ich konnte keine Bücher finden!")

if __name__ == "__main__":
    app = BookManagementApp()
    app.mainloop()