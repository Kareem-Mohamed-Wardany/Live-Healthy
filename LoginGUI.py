import re
import tkinter as tk
from tkinter import *

import customtkinter as ctk
from PIL import Image, ImageTk

from Config import *
from Database import *
from GUIHelperFunctions import *
from Images import *
from User import *
from RegisterGUI import *
from PatientGUI import *
from RadiologistGUI import *
from AdministratorGUI import *
from DoctorGUI import *
import smtplib
import ssl
from email.message import EmailMessage

class Login(ctk.CTk):
    # load Config dict
    config = SystemConfig()
    MovetoReg = False
    Moveto = False

    # connect to DB
    db = Database()

    def __init__(self):
        super().__init__()
        self.WindowSettings()
        self.login_gui()
        # Enter all your buttons,Entries here

    def WindowSettings(self):
        # let title be 'Welcome Specialist|Consultant UserName'
        Title = "Login"
        self.title(Title)

        # set Dimension of GUI
        center(
            self,
            self.config.get("FramesSizeWidth"),
            self.config.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

    def login_gui(self):
        self.backgroundFrame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            width=1255,
            height=710,
        )
        self.backgroundFrame.place(anchor="nw", relx=0.01, rely=0.011)
        bgImage = ctk.CTkLabel(self.backgroundFrame, text="", image=ctk.CTkImage(LoginBG, size=(1255, 710)))
        bgImage.place(anchor="nw", relx=0, rely=0)
        self.subbg = ctk.CTkFrame(
            self.backgroundFrame,
            fg_color="#F0F0F0",
            width=1230,
            height=694,
        )
        self.subbg.place(anchor="nw", relx=0.008, rely=0.01)
        logoImage = ctk.CTkLabel(self.backgroundFrame, text="", image=ctk.CTkImage(
            logo, size=(80, 80)), bg_color='transparent')
        logoImage.place(anchor="nw", relx=0.018, rely=0.020)
        bgImage2 = ctk.CTkLabel(self.subbg, text="", image=ctk.CTkImage(
            LoginBG2, size=(1230, 694)))
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
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=40, weight='bold',
                             slant='italic', family="Times New Roman")
        )
        welcomeLabel.place(anchor="nw", relx=0.06, rely=0.2)
        loginLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Login your account",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, family="Times New Roman")
        )
        loginLabel.place(anchor="nw", relx=0.061, rely=0.268)
        usernameLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Username:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
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
        self.usernameEntry.place(anchor="nw", relx=0.061, rely=0.46)
        passwordLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Password:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
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
        self.passwordEntry.place(anchor="nw", relx=0.061, rely=0.65)
        forgotpassLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Forgot Password?",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=15, family="Aerial 18", underline=True),
            cursor="hand2",
        )
        forgotpassLabel.bind('<Button-1>', self.forgot_password)
        forgotpassLabel.place(anchor="nw", relx=0.065, rely=0.725)
        self.LoginButton = ctk.CTkButton(self.loginFrame,text="Login", width= 170, height=50,corner_radius=30,font=ctk.CTkFont(size=18, family="Aerial 18",weight='bold'), command=self.login_verify)
        self.LoginButton.place(anchor="nw", relx=0.061, rely=0.8)
        AskAccountLabel = ctk.CTkLabel(
            self.loginFrame,
            text="Don't you have an account?",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, family="Times New Roman")
        )
        AskAccountLabel.place(anchor="nw", relx=0.21, rely=0.02)
        self.SignUpButton = ctk.CTkButton(self.loginFrame,text="SIGN UP", width= 40, height=30,corner_radius=30,font=ctk.CTkFont(size=15, family="Aerial 18"),fg_color="#808080", command=self.Goto_Register)
        self.SignUpButton.place(anchor="nw", relx=0.4, rely=0.018)

    def login_verify(self):
        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        if len(self.username) == 0 or len(self.password) == 0:
            return messagebox.showerror("Empty fields","Please fill in all fields")
        userinfo = User.Login(self.username, self.password)
        if userinfo != "ok":
            if userinfo[1] in ["Specialist","Consultant"]:
                res = self.db.Select("SELECT Verified FROM doctordata WHERE Doctor_ID=%s",[userinfo[0]])[0][0]
                if res == 0:
                    return messagebox.showerror("Error","Please wait until you are verified")
            self.Moveto = True
            self.destroy()

    

    def forgot_password(self, event):
        mail = self.usernameEntry.get()
        if len(mail) == 0:
            return messagebox.showerror("Empty Mail","Please fill in mail field")

        password = self.db.Select("SELECT Password FROM users WHERE Mail LIKE %s",[mail])
        if len(password) == 0:
            return messagebox.showerror("Error","Please Enter a valid Email")
        password = password[0][0]

        # Define email sender and receiver
        email_sender = 'livehealthy171@gmail.com'
        email_password = 'gowdfobqansntowb'
        email_receiver = mail

        # Set the subject and body of the email
        subject = 'Your Account Password'
        body = f"Here is your account password: {password}"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        messagebox.showinfo("Success", "Email Sent")


    def Goto_Register(self):
        self.MovetoReg = True
        self.destroy()
        
