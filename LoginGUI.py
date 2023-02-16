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
        self.logintitle()
        self.Loginfram()

        # Enter all your buttons,Entries here 
    def logintitle(self):
        framname = ctk.CTkLabel(
        self,
        text = "Login Page",
        width=100, height=100,
        font=ctk.CTkFont(size=30, weight="bold"),
        )
        
        framname.place(anchor="nw", relx=0.43, rely=0.01)
    def Loginfram(self):
        mainFrame = ctk.CTkFrame(
            self,
                #bg_color="#969696",
                width=700,
                height=580,
        )
        mainFrame.place(anchor="nw", relx=0.22, rely=0.17)
        FirstLabel = ctk.CTkLabel(
            mainFrame,
            text="Email Address",
            width=100,
            height=25,
            font=ctk.CTkFont(size=30),
        )
        FirstLabel.place(anchor="nw", relx=0.37, rely=0.06)
        firstEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Enter your email address",
        width=300,
        height=50
        )
        # n, ne, e, se, s, sw, w, nw, or center
        firstEntry.place(anchor="nw",relx=0.28,rely=0.17)
        MailLabel = ctk.CTkLabel(
            mainFrame,
            text="Password",
            width=65,
            height=20,
            font=ctk.CTkFont(size=30),
        )
        MailLabel.place(anchor="nw", relx=0.40, rely=0.35)
        MailEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Enter your password",
        width=300,
        height=50
        
        )
        # n, ne, e, se, s, sw, w, nw, or center
        MailEntry.place(anchor="nw",relx=0.28,rely=0.45)
if __name__ == "__main__":
    app = Login()
    app.resizable(False,False)
    center(app, 1280, 720)
    app.mainloop()

