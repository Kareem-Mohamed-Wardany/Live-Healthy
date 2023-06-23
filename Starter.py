import contextlib
import re
import smtplib
import ssl
import tkinter as tk
from datetime import datetime
from email.message import EmailMessage
from tkinter import *
from tkinter.filedialog import askopenfilename

import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import Calendar

from AdministratorGUI import *
from Config import *
from Database import *
from DoctorGUI import *
from Error import *
from GUIHelperFunctions import *
from Images import *
from PatientGUI import *
from RadiologistGUI import *


class Starter(ctk.CTk):
    # load Config dict
    config = SystemConfig()
    MovetoReg = False
    Moveto = False
    systemError = SystemErrors()
    def __init__(self):
        super().__init__()
        self.WindowSettings()
        self.login_gui()
        # Enter all your buttons,Entries here

    def WindowSettings(self):
        Title = "Welcome to Live Healthy"
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
            logo, size=(65, 65)), bg_color='#f0fafb', fg_color="#f0fafb")
        logoImage.place(anchor="nw", relx=0.018, rely=0.020)
        bgImage2 = ctk.CTkLabel(self.subbg, text="", image=ctk.CTkImage(
            LoginBG2, size=(1230, 694)))
        bgImage2.place(anchor="nw", relx=0, rely=0)


        self.SelectionFrame = ctk.CTkFrame(
            self.subbg,
            fg_color="#FFFAFA",
            width=1230,
            height=650,
        )
        self.SelectionFrame.place(anchor="nw", relx=0.5, rely=0.05)

        self.segbutton = ctk.CTkSegmentedButton(self.subbg,values=["Login","Sign Up"], command=self.ShowFrame)
        self.segbutton.place(anchor="nw", relx=0.7, rely=0.03)
        self.segbutton.set("Login")
        self.ShowLoginFrame()

    def ShowFrame(self, selection):
        with contextlib.suppress(Exception):
            for widget in self.SelectionFrame.winfo_children():
                widget.destroy()
        if selection == "Login":
            loginTimer= Timer(0.2, self.ShowLoginFrame) 
            loginTimer.start()
        else:
            RegisterTimer= Timer(0.2, self.mainRegister) 
            RegisterTimer.start()

    def ShowLoginFrame(self):
        welcomeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Welcome Back",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=40, weight='bold', slant='italic', family="Times New Roman")
        )
        welcomeLabel.place(anchor="nw", relx=0.06, rely=0.2)
        loginLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Login your account",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, family="Times New Roman")
        )
        loginLabel.place(anchor="nw", relx=0.061, rely=0.268)
        emailLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Email:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
        )
        emailLabel.place(anchor="nw", relx=0.045, rely=0.4)
        self.emailEntry = ctk.CTkEntry(
            self.SelectionFrame,
            placeholder_text="Your email...",
            fg_color="white",
            text_color="black",
            width=490,
            height=45,
        )
        self.emailEntry.place(anchor="nw", relx=0.061, rely=0.46)
        passwordLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Password:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
        )
        passwordLabel.place(anchor="nw", relx=0.061, rely=0.59)
        self.passwordEntry = ctk.CTkEntry(
            self.SelectionFrame,
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
            self.SelectionFrame,
            text="Forgot Password?",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=15, family="Aerial 18", underline=True),
            cursor="hand2",
        )
        forgotpassLabel.bind('<Button-1>', self.forgot_password)
        forgotpassLabel.place(anchor="nw", relx=0.065, rely=0.725)
        self.LoginButton = ctk.CTkButton(self.SelectionFrame,text="Login", width= 170, height=50,corner_radius=30,font=ctk.CTkFont(size=18, family="Aerial 18",weight='bold'), command=self.login_verify)
        self.LoginButton.place(anchor="nw", relx=0.061, rely=0.8)

    def login_verify(self):
        from User import User
        self.email = self.emailEntry.get()
        self.password = self.passwordEntry.get()
        if len(self.email) == 0 or len(self.password) == 0:
            return messagebox.showerror("Error", self.systemError.get(1), icon="error", parent=self.SelectionFrame)
        userinfo = User.Login(self.email, self.password)
        suspended = self.suspended(userinfo[0])
        if suspended != -1:
            return messagebox.showerror("Error", self.systemError.get(suspended), icon="error", parent=self.SelectionFrame)
        if userinfo != "ok":
            if userinfo[1] in ["Specialist","Consultant"]:
                res = SelectQuery("SELECT Verified FROM doctordata WHERE Doctor_ID=%s",[userinfo[0]])[0][0]
                if res == 0:
                    return messagebox.showerror("Error", self.systemError.get(15), icon="error", parent=self.SelectionFrame)
            self.MoveTo(userinfo)

    def forgot_password(self, event):
        mail = self.emailEntry.get()
        if len(mail) == 0:
            return messagebox.showerror("Error", self.systemError.get(14), icon="error", parent=self.SelectionFrame)

        password = SelectQuery("SELECT Password FROM users WHERE Mail LIKE %s",[mail])
        if len(password) == 0:
            return messagebox.showerror("Error", self.systemError.get(3), icon="error", parent=self.SelectionFrame)
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

    def suspended(self, id):
        res = SelectQuery("SELECT COUNT(*) FROM suspended WHERE User_ID = %s",[id])[0][0]
        return 26 if res == 1 else -1

    # Start of Register Part 
    def mainRegister(self):
        FullNameLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Full Name*",
            fg_color="transparent",
            bg_color="transparent",
            text_color="black",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        FullNameLabel.place(anchor="nw", relx=0.015, rely=0.06)

        self.FullNameEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Full Name...",
        border_color="black",
        text_color="black",
        placeholder_text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        width=250,
        height=35,
        )
        self.FullNameEntry.place(anchor="nw",relx=0.015,rely=0.10)

        MailLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Email*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        MailLabel.place(anchor="nw", relx=0.25, rely=0.06)

        self.MailEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Email...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.MailEntry.place(anchor="nw",relx=0.25,rely=0.10)



        PassLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PassLabel.place(anchor="nw",relx=0.015, rely=0.17)

        self.PassEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Password...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.PassEntry.place(anchor="nw",relx=0.015,rely=0.21)

        ConfirmPassLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Confirm Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        ConfirmPassLabel.place(anchor="nw",relx=0.25, rely=0.17)

        self.ConfirmPassEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Confirm Your Password...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.ConfirmPassEntry.place(anchor="nw",relx=0.25,rely=0.21)

        PhoneLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Phone Number*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PhoneLabel.place(anchor="nw",relx=0.015, rely=0.28)

        self.PhoneEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Phone Number...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.PhoneEntry.place(anchor="nw",relx=0.015,rely=0.32)

        

        AgeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Date of Birth*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        AgeLabel.place(anchor="nw",relx=0.25, rely=0.28)
        self.cal = Calendar(self.SelectionFrame,
        selectmode = 'day',
        year = 2001,
        month = 1,
        day = 1)
        self.cal.place(anchor="nw", relx=0.25,rely=0.32)


        GenderLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Gender*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        GenderLabel.place(anchor="nw",relx=0.015, rely=0.39)

        self.GenderVar = tk.IntVar(value = -1)
        MaleRadio = ctk.CTkRadioButton(
            self.SelectionFrame,
            text="Male",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=1
        )
        MaleRadio.place(anchor="nw",relx=0.015, rely=0.45)
        FemaleRadio = ctk.CTkRadioButton(
            self.SelectionFrame,
            text="Female",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=2
        )
        FemaleRadio.place(anchor="nw",relx=0.1, rely=0.45)



        TypeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="User Type*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        TypeLabel.place(anchor="nw",relx=0.015, rely=0.5)

        self.TypeCombo = ctk.CTkOptionMenu(self.SelectionFrame,
        width=250,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Patient", "Radiologist", "Consultant", "Specialist"],
        command=self.UserType
        )
        self.TypeCombo.place(anchor="nw",relx=0.015, rely=0.55)
        self.patient()
        self.Registerbutton()

    def UserType(self, Utype):
        if Utype=="Patient":
            self.patient()
            self.Registerbutton()
        elif Utype in ["Consultant", "Specialist"]:
            self.doctor()
            self.Registerbutton()
        elif Utype=="Radiologist":
            self.radiologist()
            self.Registerbutton()

    def HoldFrame(self):
        with contextlib.suppress(Exception):
            self.Secondframe.destroy()

        self.Secondframe = ctk.CTkFrame(
            self.SelectionFrame,
            fg_color="transparent",
            width=520,
            height=300
        )
        self.Secondframe.place(anchor="nw",relx=0.015, rely=0.61)

    def patient(self):
        self.HoldFrame()
        HealthLabel = ctk.CTkLabel(
            self.Secondframe,
            text="Patient's Health Status",
            text_color="black",
            font=ctk.CTkFont(size=30),
        )
        HealthLabel.place(anchor="nw",relx=0.2, rely=0.04)
        self.patientsHealthCheck()

    def patientsHealthCheck (self):
        self.PatientHealthFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=520,
            height=300
        )
        self.PatientHealthFrame.place(anchor="nw",relx=0, rely=0.2)

        self.Heart = IntVar()
        HeartCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Heart Diseases",
            text_color="black",
            width=260,
            variable=self.Heart,
            onvalue=1,
            offvalue=0
        )
        HeartCheck.grid(row=1,column=0, pady=5)

        self.Diabetes = IntVar()
        DiabetesCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Diabetes",
            text_color="black",
            width=260,
            variable=self.Diabetes,
            onvalue=1,
            offvalue=0
        )
        DiabetesCheck.grid(row=1,column=1, pady=5)

        
        self.Cancer = IntVar()
        CancerCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Cancer",
            text_color="black",
            width=260,
            variable=self.Cancer,
            onvalue=1,
            offvalue=0
        )
        CancerCheck.grid(row=2,column=0, pady=5)

        self.Obesity = IntVar()
        ObesityCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Obesity",
            text_color="black",
            width=260,
            variable=self.Obesity,
            onvalue=1,
            offvalue=0
        )
        ObesityCheck.grid(row=2,column=1, pady=5)


        self.Smoker = IntVar()
        SmokerCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Smoker",
            text_color="black",
            width=260,
            variable=self.Smoker,
            onvalue=1,
            offvalue=0
        )
        SmokerCheck.grid(row=3,column=0, pady=5)

        self.Hypertension = IntVar()
        HypertensionCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Hypertension",
            text_color="black",
            width=260,
            variable=self.Hypertension,
            onvalue=1,
            offvalue=0
        )
        HypertensionCheck.grid(row=3,column=1, pady=5)

        self.Allergies = IntVar()
        AllergiesCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Allergies",
            text_color="black",
            width=260,
            variable=self.Allergies,
            onvalue=1,
            offvalue=0
        )
        AllergiesCheck.grid(row=4,column=0, pady=5)

        BloodTypeLabel = ctk.CTkLabel(
            self.Secondframe,
            text="Blood Type:",
            text_color="black",
            height=25,
            font=ctk.CTkFont(size=14),
        )
        BloodTypeLabel.place(anchor="nw", relx=0.01, rely=0.7)

        self.BloodTypeCombo = ctk.CTkOptionMenu(
        self.Secondframe,
        width=100,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Unknown","O-","O+","B-","B+","A-","A+","AB-","AB+"],
        font = ctk.CTkFont(size =17)
        )
        self.BloodTypeCombo.place(anchor="nw", relx=0.186, rely=0.7)

    def doctor(self):
        self.HoldFrame()
        self.DoctorFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=600,
            height=580
        )
        self.DoctorFrame.place(anchor="nw",relx=0, rely=0)

        self.ImageFrame = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="transparent",
            fg_color="transparent",
            border_color="black",
            width=150,
            height=100
        )
        self.ImageFrame.place(anchor="nw",relx=0, rely=0.01)

        self.ImageFrame2 = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="transparent",
            fg_color="transparent",
            width=150,
            height=100
        )
        self.ImageFrame2.place(anchor="nw",relx=0.4, rely=0.01)

        ImportIDButton = ctk.CTkButton(self.DoctorFrame,text="Import ID", command=self.ImportID,width=50)
        ImportIDButton.place(anchor="nw", relx=0.26, rely=0.08)

        ImportLicenseButton = ctk.CTkButton(self.DoctorFrame,text="Import Prof. License", command=self.ImportLicense,width=100)
        ImportLicenseButton.place(anchor="nw", relx=0.653, rely=0.08)

        UniLabel = ctk.CTkLabel(
            self.DoctorFrame,
            text="University:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        UniLabel.place(anchor="nw",relx=0, rely=0.2)
        self.UniEntry = ctk.CTkEntry(
        self.DoctorFrame,
        placeholder_text="Input The University You Graduated From...",
        placeholder_text_color="black",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        width=300,
        height=30
        )
        self.UniEntry.place(anchor="nw",relx=0.2,rely=0.2)

    IDPath = ""
    def ImportID(self):
        self.IDPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        IDImage = ctk.CTkLabel(self.ImageFrame,text="",image=ctk.CTkImage(Image.open(self.IDPath),size=(150,100)))
        IDImage.place(anchor="nw", relx=0, rely=0)

    LicensePath = ""
    def ImportLicense(self):
        self.LicensePath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        LicenseImage = ctk.CTkLabel(self.ImageFrame2,text="",image=ctk.CTkImage(Image.open(self.LicensePath),size=(150,100)))
        LicenseImage.place(anchor="nw", relx=0, rely=0)

    def radiologist(self):
        self.HoldFrame()
        RadiologistFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=600,
            height=580
        )
        RadiologistFrame.place(anchor="nw",relx=0, rely=0)

        RadioCenterLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Radiology Center:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        RadioCenterLabel.place(anchor="nw",relx=0, rely=0.05)

        res = SelectQuery("SELECT Name FROM radiologycenters")
        RadioCenters = [i[0] for i in res]
        self.RadioCenterCombo = ctk.CTkOptionMenu(
        RadiologistFrame,
        width=330,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=RadioCenters,
        font=ctk.CTkFont(size = 20),
        )
        self.RadioCenterCombo.place(anchor="nw",relx=0.3, rely=0.05)

        RadioCenterCodeLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Center Verification Code:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        RadioCenterCodeLabel.place(anchor="nw",relx=0, rely=0.12)

        self.RadioCenterCodeEntry = ctk.CTkEntry(
        RadiologistFrame,
        placeholder_text="Input Your Center's Verification Code...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        width=400,
        height=35
        )
        self.RadioCenterCodeEntry.place(anchor="nw",relx=0.2,rely=0.17)

    def Registerbutton(self,):
        RegisterButton = ctk.CTkButton(
        self.SelectionFrame,
        bg_color="#b3c7e5",
        text="Register",
        width= 150,
        height=80,
        font = ctk.CTkFont(size=23),
        command=self.fetchAllData
        )
        RegisterButton.place(anchor="nw", relx=0.35, rely=0.87)

    def fetchAllData(self):
        self.userName = self.FullNameEntry.get()
        self.Email = self.MailEntry.get()
        self.Phone = self.PhoneEntry.get()
        self.Password = self.PassEntry.get()
        self.ConfirmPassword = self.ConfirmPassEntry.get()
        self.DoB = datetime.strptime(self.cal.get_date(), '%m/%d/%y').date()
        self.Gender = "Male" if self.GenderVar.get() == 1 else "Female"
        self.UsType = self.TypeCombo.get()
        CheckData = self.dataValidator()
        
        if CheckData != -1:
            return messagebox.showerror("Error", self.systemError.get(CheckData), icon="error", parent=self.backgroundFrame)
        else:
            self.insertUserInfo()

    def dataValidator(self):  
        EmptyFields = self.emptyMainFields()
        if EmptyFields != -1:
            return EmptyFields
        
        ValidName = self.userNameChecker()
        
        if ValidName != -1:
            return ValidName
        
        if self.emailChecker():
            return 3
        
        PasswordValid = self.passwordChecker()
        if PasswordValid != -1:
            return PasswordValid
        
        PhoneValid = self.phoneChecker()
        if PhoneValid != -1:
            return PhoneValid
        
        genvalid = self.genderValid()
        if genvalid != -1:
            return genvalid
        
        AllVaild = self.fetchUserTypeData()
        if AllVaild != -1:
            return AllVaild
        
        return -1

    def emptyMainFields(self):
        if self.FullNameEntry.get() == "" or self.Phone == "" or self.Email == "" or self.Password == "" or self.ConfirmPassword == "" or self.Gender == 0:
            return 1
        else:
            return -1

    def userNameChecker(self):
        pattern = re.compile("^[a-zA-Z ]*$")
        return -1 if pattern.fullmatch(self.userName) is not None else 2
    
    def emailChecker(self):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        return not re.match(pat,self.Email)
    
    def passwordChecker(self):
        if self.Password != self.ConfirmPassword:
            return 6
        elif len(self.Password) < 8:
            return 7
        else:
            return -1
    
    def phoneChecker(self):
        if (not self.Phone.isnumeric()) or (len(self.Phone) < 11 or len(self.Phone) > 15):
            return 8
        else:
            return -1

    def genderValid(self):
        return 9 if self.GenderVar.get() == -1 else -1

    def CheckRadioCenter(self):
        res = SelectQuery("SELECT Registercode, Center_Limit FROM radiologycenters WHERE Name=%s",[self.radioCenter])
        limit = res[0][1]
        code = res[0][0]
        if self.radioCenterCode == code and limit > 0:
            limit -= 1
            UpdateQuery("UPDATE radiologycenters SET Center_Limit=%s WHERE Name=%s",[limit,self.radioCenter])
        if limit == 0:
            self.Valid = False
            return 4
        if self.radioCenterCode != code:
            self.Valid = False
            return 5
        return -1

    def fetchUserTypeData(self):
        # Function that fetches the user type data in SecondFrame
        if self.TypeCombo.get() == "Patient":
            self.heart = self.Heart.get()
            self.diabetes = self.Diabetes.get()
            self.cancer = self.Cancer.get()
            self.obesity = self.Obesity.get()
            self.smoker = self.Smoker.get()
            self.hypertension = self.Hypertension.get()
            self.allergies = self.Allergies.get()
            self.Blood = self.BloodTypeCombo.get()

        if self.TypeCombo.get() == "Radiologist":
            self.radioCenter = self.RadioCenterCombo.get()
            self.radioCenterCode = self.RadioCenterCodeEntry.get()
            RadiologyCenterVaild = self.CheckRadioCenter()
            if RadiologyCenterVaild != -1:
                return RadiologyCenterVaild

        if self.TypeCombo.get() in ["Specialist", "Consultant"]:
            if len(self.IDPath) == 0 and len(self.LicensePath) == 0: 
                return 13
            if len(self.IDPath) == 0:
                return 11
            if len(self.LicensePath) == 0:
                return 12
                
            if self.UniEntry.get() == "" :
                return 10
            self.uni = self.UniEntry.get()
            self.IDbinary = convertToBinaryData(self.IDPath)
            self.LicenseBinary = convertToBinaryData(self.LicensePath)
        return -1

    def insertUserInfo(self):
        # Function That calls abstract method to insert user info into database 
        if self.UsType == "Patient":
            pp = Patient.CreatePatient(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.heart, self.diabetes, self.cancer, self.obesity, self.smoker, self.hypertension, self.allergies, self.Blood)
            pp.SaveData()
        if self.UsType == "Radiologist":
            radiologistdata = Radiologist.CreateRadiologist(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.radioCenter)
            radiologistdata.SaveData()
        if self.UsType in ["Consultant", "Specialist"]:
            doctordata = Doctor.CreateDoctor(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.uni, self.IDbinary, self.LicenseBinary)
            doctordata.SaveData()
        messagebox.showinfo("✅ Success", " You have successfully registered a new account ✅ ", icon="info", parent=self.backgroundFrame)

    def MoveTo(self, UserInfo):
        self.destroy()
        id = int(UserInfo[0])
        user_type = UserInfo[1].lower()

        if user_type == "patient":
            # from PatientGUI import PatGUI
            patient = PatGUI(id)
            patient.mainloop()
        elif user_type == "radiologist":
            from RadiologistGUI import RadioloGUI
            radiologist = RadioloGUI(id)
            radiologist.mainloop()
        elif user_type == "administrator":
            from AdministratorGUI import AdminGUI
            admin = AdminGUI(id)
            admin.mainloop()
        elif user_type in ["specialist", "consultant"]:
            from DoctorGUI import DocGUI
            doctor = DocGUI(id)
            doctor.mainloop()



if __name__ == "__main__":
    app = Starter()
    app.mainloop()
