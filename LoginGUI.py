import tkinter as tk
from tkinter import *

import customtkinter as ctk

from Config import *
from Database import *
from GUIHelperFunctions import *
from PIL import ImageTk, Image
import re

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
        self.background()
        # Enter all your buttons,Entries here
    def background(self):
        self.backgroundFrame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            width=1255,
            height=710,
        )
        self.backgroundFrame.place(anchor="nw", relx=0.01, rely=0.011)
        bgImage = ctk.CTkLabel(self.backgroundFrame,text="",image=ctk.CTkImage(Image.open("asset/login.jpg"),size=(1255,710)))
        bgImage.place(anchor="nw", relx=0, rely=0)
        self.subbg = ctk.CTkFrame(
            self.backgroundFrame,
            fg_color="#F0F0F0",
            width=1230,
            height=694,
        )
        self.subbg.place(anchor="nw", relx=0.008, rely=0.01)
        logoImage = ctk.CTkLabel(self,text="",image=ctk.CTkImage(Image.open("asset/Logo.png"),size=(80,80)))
        logoImage.place(anchor="nw", relx=0.018, rely=0.020)
        bgImage2 = ctk.CTkLabel(self.subbg,text="",image=ctk.CTkImage(Image.open("asset/login2.jpg"),size=(1230,694)))
        bgImage2.place(anchor="nw", relx=0, rely=0)
        self.loginFrame = ctk.CTkFrame(
            self.subbg,
            fg_color="#FFFAFA",
            width=1230,
            height=693,
        )
        self.loginFrame.place(anchor="nw", relx=0.5, rely=0)
        welcomeLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Welcome Back",
            text_color= "#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=40,weight='bold',slant='italic',family="Times New Roman")
        )
        welcomeLabel.place(anchor="nw", relx=0.06, rely=0.2)
        loginLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Login your account",
            text_color= "#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20,family="Times New Roman")
        )
        loginLabel.place(anchor="nw", relx=0.061, rely=0.268)
        usernameLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Username:",
            text_color= "#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20,weight="bold",family="Times New Roman")
        )
        usernameLabel.place(anchor="nw", relx=0.061, rely=0.4)
        self.usernameEntry = ctk.CTkEntry(
        self.loginFrame,
        placeholder_text="Your email...",
        fg_color="white",
        text_color="black",
        width=490,
        height=45,
        )
        self.usernameEntry.place(anchor="nw",relx=0.061,rely=0.46)
        passwordLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Password:",
            text_color= "#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20,weight="bold",family="Times New Roman")
        )
        passwordLabel.place(anchor="nw", relx=0.061, rely=0.59)
        self.passwordEntry = ctk.CTkEntry(
        self.loginFrame,
        placeholder_text="Your password...",
        fg_color="white",
        text_color="black",
        width=490,
        height=45,
        bg_color="transparent",
        show="*"
        )
        self.passwordEntry.place(anchor="nw",relx=0.061,rely=0.65)
        forgotpassLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Forgot Password?",
            text_color= "#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=15,family="Aerial 18",underline=True),
            cursor= "hand2",
        )
        forgotpassLabel.place(anchor="nw", relx=0.065, rely=0.725)



if __name__ == "__main__":
    app = Login()
    app.resizable(False, False)  # Disable resize for GUI
    center(app, 1280, 720)  # center window in your screen
    app.mainloop()