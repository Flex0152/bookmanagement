from model import DatabaseAPI
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label, Entry, Button, Combobox


class tmpApp(tk.Tk):
    """Nur zum Testen von EditBookWindow"""
    def __init__(self):
        super().__init__()
        self.lbl = Label(self, text="Test ausführen")
        self.lbl.grid(row=0, column=0)

        self.btn = Button(self, text="ausführen", command=self.action)
        self.btn.grid(row=1, column=0)

    def action(self):
        EditBookWindow(self, "Der Herr der Ringe: Die Gefährten")



class EditBookWindow:
    def __init__(self, parent_app, book_title):
        self.book_title = book_title
        self.parent_app = parent_app
        self.window = tk.Toplevel(self.parent_app)

        self.db = DatabaseAPI()
        self.book_obj = self.db.get_book_by_name(self.book_title)

        if not self.book_obj:
            messagebox.showerror(title="Es ist ein Fehler aufgetreten", 
                                 message="Buch nicht gefunden!")
            self.window.destroy()

        # Hauptfenster Config
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Hauptcontainer 
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(5):
            self.frame.rowconfigure(i, weight=1)
        
        for i in range(2):
            self.frame.columnconfigure(i, weight=1)

        self.title = "Buch bearbeiten"

        self.lbl_title = Label(self.frame, text="Titel: ")
        self.lbl_title.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        self.in_title = Entry(self.frame)
        self.in_title.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")

        self.lbl_isbn = Label(self.frame, text="ISBN: ")
        self.lbl_isbn.grid(row=1, column=0, padx=1, pady=1, sticky="nsew")
        self.in_isbn = Entry(self.frame)
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

        self.in_title.insert(0, self.book_obj.title)
        self.in_isbn.insert(0, (self.book_obj.isbn if self.book_obj.isbn != None else ""))
        self.cmb_author.insert(0, self.book_obj.author.name)
        self.cmb_genre.insert(0, self.book_obj.genre.name)

        self.btn_check = Button(self.frame, text="Anpassen", command=self.modify_book) 
        self.btn_check.grid(row=3, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

        self.btn_quit = Button(self.frame, text="Beenden", command=self.window.destroy)
        self.btn_quit.grid(row=4, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

    def modify_book(self):
        new_author = self.cmb_author.get().strip()
        new_title = self.in_title.get().strip()
        new_genre = self.cmb_genre.get().strip()
        new_isbn = self.in_isbn.get().strip()

        try:
            self.db.update_book(self.book_obj.id, new_title, new_author, new_genre, isbn=new_isbn)
            messagebox.showinfo(title="Buch anpassen", message="Das Buch wurde erfolgreich angepasst.")
            self.parent_app.all_books_func()
        except ValueError as e:
            messagebox.showerror(title="Buch nicht gefunden!", message=e)


if __name__ == "__main__":
    app = tmpApp()
    app.mainloop()