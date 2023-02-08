import tkinter as tk

import customtkinter as ctk

from Config import *
from Database import *
from GUIHelperFunctions import *

class Login(ctk.CTk):
    # load Config dict
    config = SystemConfig()
    
    # connect to DB
    db = Database()

    def __init__(self):
        super().__init__()
        Title = "Login" 
        self.title(Title)
        # set Dimension of GUI
        self.geometry(self.config.get("FramesSize"))

        # Enter all your buttons,Entries here 
        label = ctk.CTkLabel(self, text = "Test Label", width=100, height=50,font=ctk.CTkFont(size=30, weight="bold"))
        label.place(anchor="nw", relx=0.01, rely= 0.01)

if __name__ == "__main__":
    app = Login()
    app.resizable(False,False)
    center(app, 1280, 720)
    app.mainloop()

