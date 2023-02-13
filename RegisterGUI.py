import tkinter as tk
from tkinter import *
from tkcalendar import Calendar

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
        self.mainTitle()
        self.mainRegister()

        # Enter all your buttons,Entries here
    def mainTitle(self):
        infoFrame = ctk.CTkFrame(
            self,
            bg_color="#F0F0F0",
            width=650,
            height=100,
        )
        infoFrame.place(anchor="nw", relx=0.23, rely=0.02)

        mainLabel = ctk.CTkLabel(
            infoFrame,
            text="Your Profile",
            width=100,
            height=50,
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        mainLabel.place(anchor="nw", relx=0.35, rely=0.01)
        subLabel = ctk.CTkLabel(
            infoFrame,
            text="Enter the login information for your account",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        subLabel.place(anchor="nw", relx=0.2, rely=0.5)
    def mainRegister(self):
        mainFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=700,
            height=580,
        )
        mainFrame.place(anchor="nw", relx=0.02, rely=0.17)
        FirstLabel = ctk.CTkLabel(
            mainFrame,
            text="First Name*",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        FirstLabel.place(anchor="nw", relx=0.015, rely=0.06)
        firstEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your First Name",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        firstEntry.place(anchor="nw",relx=0.015,rely=0.12)
        SecondLabel = ctk.CTkLabel(
            mainFrame,
            text="Second Name*",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        SecondLabel.place(anchor="nw", relx=0.55, rely=0.06)
        SecondEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Second Name",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        SecondEntry.place(anchor="nw",relx=0.55,rely=0.12)
        MailLabel = ctk.CTkLabel(
            mainFrame,
            text="Email*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        MailLabel.place(anchor="nw", relx=0.015, rely=0.22)
        MailEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Email",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        MailEntry.place(anchor="nw",relx=0.015,rely=0.27)
        PhoneLabel = ctk.CTkLabel(
            mainFrame,
            text="Phone Number*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PhoneLabel.place(anchor="nw",relx=0.55, rely=0.22)
        PhoneEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Phone Number",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        PhoneEntry.place(anchor="nw",relx=0.55,rely=0.27)
        PassLabel = ctk.CTkLabel(
            mainFrame,
            text="Password*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PassLabel.place(anchor="nw",relx=0.015, rely=0.37)
        PassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Password",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        PassEntry.place(anchor="nw",relx=0.015,rely=0.43)
        ConfirmPassLabel = ctk.CTkLabel(
            mainFrame,
            text="Confirm Password*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        ConfirmPassLabel.place(anchor="nw",relx=0.55, rely=0.37)
        ConfirmPassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Confirm Your Password",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        ConfirmPassEntry.place(anchor="nw",relx=0.55,rely=0.43)
        AgeLabel = ctk.CTkLabel(
            mainFrame,
            text="Date of Birth*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        AgeLabel.place(anchor="nw",relx=0.015, rely=0.52)
        cal = Calendar(mainFrame,
        selectmode = 'day',
        year = 2001,
        month = 1,
        day = 1)
        cal.place(anchor="nw", relx=0.015,rely=0.58)
        # cal.get_date()
        GenderLabel = ctk.CTkLabel(
            mainFrame,
            text="Gender*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        GenderLabel.place(anchor="nw",relx=0.55, rely=0.52)
        var = IntVar();
        MaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Male",
            variable=var,
            value=1
        )
        MaleRadio.place(anchor="nw",relx=0.55, rely=0.58)
        FemaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Female",
            variable=var,
            value=2
        )
        FemaleRadio.place(anchor="nw",relx=0.55, rely=0.63)

        
        

if __name__ == "__main__":
    app = Register()
    app.resizable(False, False)  # Disable resize for GUI
    center(app, 1280, 720)  # center window in your screen
    app.mainloop()

