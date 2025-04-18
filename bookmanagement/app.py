from model import DatabaseAPI
import tkinter as tk
from tkinter import TclError, messagebox
from tkinter.ttk import Label, Entry, Button, Spinbox


class BookManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

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

        # vier Zeilen, vier Zeilen Rest 
        for i in range(4):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)
        
        # zwei Zeilen; zwei Spalten Buttons
        for i in range(2):
            self.btn_frame.rowconfigure(i, weight=1)
            self.btn_frame.columnconfigure(i, weight=1)

if __name__ == "__main__":
    app = BookManagementApp()
    app.mainloop()