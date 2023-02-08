import tkinter as tk

import customtkinter as ctk

from Config import *
from Database import *
from GUIHelperFunctions import *


class Register(ctk.CTk):
    # load Config dict
    config = SystemConfig()

    # connect to DB
    db = Database()

    def __init__(self):
        super().__init__()
        Title = "Register"
        self.title(Title)
        # set Dimension of GUI
        self.geometry(self.config.get("FramesSize"))

        # Enter all your buttons,Entries here
        label = ctk.CTkLabel(
            self,
            text="Test Label",
            width=100,
            height=50,
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        label.place(anchor="nw", relx=0.01, rely=0.01)
        l = ctk.CTkEntry(self,placeholder_text="Test")
        # n, ne, e, se, s, sw, w, nw, or center
        l.place(anchor="nw",relx=0,rely=0)


if __name__ == "__main__":
    app = Register()
    app.resizable(False, False)  # Disable resize for GUI
    # center(app)  # center window in your screen
    app.mainloop()
