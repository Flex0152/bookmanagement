from model import DatabaseAPI
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label, Entry, Button, Spinbox, Treeview, Combobox
from edit_book_window import EditBookWindow


class AddBookWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel(self.parent_app)

        self.db = DatabaseAPI()

        # Hauptfenster Config
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Hauptcontainer 
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(6):
            self.frame.rowconfigure(i, weight=1)
        
        for i in range(2):
            self.frame.columnconfigure(i, weight=1)

        self.title = "Neues Buch hinzufügen"

        self.inTitle = tk.StringVar()
        self.lbl_title = Label(self.frame, text="Titel: ")
        self.lbl_title.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        self.in_title = Entry(self.frame, textvariable=self.inTitle)
        self.in_title.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")

        self.inIsbn = tk.StringVar()
        self.lbl_isbn = Label(self.frame, text="ISBN: ")
        self.lbl_isbn.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        self.in_isbn = Entry(self.frame, textvariable=self.inIsbn)
        self.in_isbn.grid(row=1, column=1, padx=1, pady=1, sticky="nsew")

        self.lbl_author = Label(self.frame, text="Autor: ")
        self.lbl_author.grid(row=2, column=0, padx=1, pady=1, sticky="nsew")
        self.cmb_author = Combobox(self.frame)
        self.cmb_author['values'] = [item.name for item in self.db.get_all_authors()]
        self.cmb_author.grid(row=2, column=1, padx=1, pady=1, sticky="nsew")

        self.lbl_genre = Label(self.frame, text="Genre: ")
        self.lbl_genre.grid(row=3, column=0, padx=1, pady=1, sticky="nsew")
        self.cmb_genre = Combobox(self.frame)
        self.cmb_genre['values'] = [item.name for item in self.db.get_all_genre()]
        self.cmb_genre.grid(row=3, column=1, padx=1, pady=1, sticky="nsew")

        self.btn_check = Button(self.frame, text="Hinzufügen", command=self.add_book_func)
        self.btn_check.grid(row=4, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

        self.btn_quit = Button(self.frame, text="Abbrechen", command=self.window.destroy)
        self.btn_quit.grid(row=5, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

    def add_book_func(self):
        title = self.in_title.get().strip()
        author = self.cmb_author.get().strip()
        genre = self.cmb_genre.get().strip()
        isbn = self.inIsbn.get().strip() if self.inIsbn.get() != "" else None

        if title and author and genre:
            self.parent_app.db.add_book(title, author, genre, isbn)
            self.parent_app.all_books_func()
            self.window.destroy()
        else:
            messagebox.showerror("Fehler", "Hier fehlen Werte!")


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
        
        for i in range(3):
            self.btn_frame.rowconfigure(i, weight=1)
            self.btn_frame.columnconfigure(i, weight=1)

        self.data_tree = Treeview(self.frame)
        self.data_tree.grid(column=0, row=0)

        self.btn_all_books = Button(self.btn_frame, text="Alle Bücher", command=self.all_books_func)
        self.btn_all_books.grid(column=0, columnspan=3, row=0, sticky="nsew")

        self.btn_add_book = Button(self.btn_frame, text="Buch hinzufügen", command=self.add_book_window)
        self.btn_add_book.grid(column=0, columnspan=3, row=1, sticky="nsew")

        self.btn_edit_book = Button(self.btn_frame, text="Buch bearbeiten", command=self.edit_book_window)
        self.btn_edit_book.grid(column=0, columnspan=3, row=2, sticky="nsew")

        self.btn_delete_book = Button(self.btn_frame, text="Buch löschen", command=self.delete_book)
        self.btn_delete_book.grid(column=0, columnspan=3, row=3, sticky="nsew")

        self.btn_quit = Button(self.btn_frame, text="Beenden", command=self.destroy)
        self.btn_quit.grid(column=0, columnspan=3, row=99, sticky="nsew")

        self.all_books_func()

    def _clear_treeview(self):
        for i in self.data_tree.get_children():
            self.data_tree.delete(i)

    def edit_book_window(self):
        curItem = self.data_tree.focus()
        if curItem != "":
            selected = self.data_tree.item(curItem)
            EditBookWindow(self, selected['text'])

    def delete_book(self):
        curItem = self.data_tree.focus()
        if curItem != "":
            selected = self.data_tree.item(curItem)
            result = self.db.delete_book_by_name(selected['text'])
            delete = messagebox.askyesnocancel(title="Title entfernen", message=f"Soll '{selected['text']}' wirklich entfernt werden?")
            if delete:
                if result > 1:
                    messagebox.showwarning(title="Title entfernt", message=f"Es wurden {result} Title entfernt!")
                elif result == 1:
                    messagebox.showinfo(title="Title entfnert", message="Das Buch wurde erfolgreich entfernt!")
                else:
                    messagebox.showerror(title="Title entfernt", message="Der Title konnte nicht entfernt werden!")


    def add_book_window(self):
        AddBookWindow(self)

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