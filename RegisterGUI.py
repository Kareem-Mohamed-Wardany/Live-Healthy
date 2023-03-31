import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
import contextlib

import subprocess
import customtkinter as ctk
from Images import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from tkinter.filedialog import askopenfilename
from Patient import *
from Doctor import *
from Radiologist import *
from PIL import Image
import re
from datetime import datetime
from Error import *


# from Runner import *


class Register(ctk.CTk):
    # load Config dict
    config = SystemConfig()
    systemError = SystemErrors()

    # connect to DB
    db = Database()

    def __init__(self):
        super().__init__()
        self.WindowSettings()
        self.Register_gui()
        # set Dimension of GUI
        self.mainTitle()
        self.mainRegister()
        self.patient()
        self.Registerbutton()

        
        # Enter all your buttons,Entries here
    
    def WindowSettings(self):
        # let title be 'Welcome Specialist|Consultant UserName'
        Title = "Register"
        self.title(Title)
        # self.attributes('-alpha', 0.5)
        # self.attributes('-alpha', 0.5)
        # set Dimension of GUI
        center(
            self,
            self.config.get("FramesSizeWidth"),
            self.config.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

    def Register_gui(self):
        self.backgroundFrame = ctk.CTkFrame(
            self,
            width=1280,
            height=720,
        )
        self.backgroundFrame.place(anchor="nw", relx=0, rely=0)
        bgImage = ctk.CTkLabel(self.backgroundFrame, text="", image=ctk.CTkImage(RegisterBG, size=(1280, 720)))
        bgImage.place(anchor="nw", relx=0, rely=0)

    def mainTitle(self):
        mainLabel = ctk.CTkLabel(
            self.backgroundFrame,
            text="Register Your Account",
            width=200,
            bg_color="#b3c7e5",
            text_color="black",
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        mainLabel.place(anchor="nw", relx=0.35, rely=0.05)

    def mainRegister(self):
        mainFrame = ctk.CTkFrame(
            self.backgroundFrame,
            fg_color="#b3c7e5",
            bg_color="#b3c7e5",
            width=650,
            height=580
        )
        mainFrame.place(anchor="nw", relx=0.01, rely=0.17)

        FirstLabel = ctk.CTkLabel(
            mainFrame,
            text="First Name*",
            text_color="black",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        FirstLabel.place(anchor="nw", relx=0.015, rely=0.06)

        self.firstEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your First Name...",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        text_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        )
        self.firstEntry.place(anchor="nw",relx=0.015,rely=0.12)

        SecondLabel = ctk.CTkLabel(
            mainFrame,
            text="Second Name*",
            text_color="black",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        SecondLabel.place(anchor="nw", relx=0.55, rely=0.06)

        self.SecondEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Last Name...",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        text_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.SecondEntry.place(anchor="nw",relx=0.55,rely=0.12)

        MailLabel = ctk.CTkLabel(
            mainFrame,
            text="Email*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        MailLabel.place(anchor="nw", relx=0.015, rely=0.22)

        self.MailEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Email...",
        text_color="black",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.MailEntry.place(anchor="nw",relx=0.015,rely=0.27)

        PhoneLabel = ctk.CTkLabel(
            mainFrame,
            text="Phone Number*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PhoneLabel.place(anchor="nw",relx=0.55, rely=0.22)

        self.PhoneEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Phone Number...",
        text_color="black",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.PhoneEntry.place(anchor="nw",relx=0.55,rely=0.27)

        PassLabel = ctk.CTkLabel(
            mainFrame,
            text="Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PassLabel.place(anchor="nw",relx=0.015, rely=0.37)

        self.PassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Password...",
        text_color="black",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.PassEntry.place(anchor="nw",relx=0.015,rely=0.43)

        ConfirmPassLabel = ctk.CTkLabel(
            mainFrame,
            text="Confirm Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        ConfirmPassLabel.place(anchor="nw",relx=0.55, rely=0.37)

        self.ConfirmPassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Confirm Your Password...",
        text_color="black",
        fg_color="#b3c7e5",
        bg_color="#b3c7e5",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.ConfirmPassEntry.place(anchor="nw",relx=0.55,rely=0.43)

        AgeLabel = ctk.CTkLabel(
            mainFrame,
            text="Date of Birth*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        AgeLabel.place(anchor="nw",relx=0.015, rely=0.52)
        self.cal = Calendar(mainFrame,
        selectmode = 'day',
        year = 2001,
        month = 1,
        day = 1)
        self.cal.place(anchor="nw", relx=0.015,rely=0.58)


        GenderLabel = ctk.CTkLabel(
            mainFrame,
            text="Gender*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        GenderLabel.place(anchor="nw",relx=0.55, rely=0.52)

        self.GenderVar = tk.IntVar(value = -1)
        MaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Male",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=1
        )
        MaleRadio.place(anchor="nw",relx=0.57, rely=0.58)
        FemaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Female",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=2
        )
        FemaleRadio.place(anchor="nw",relx=0.57, rely=0.64)



        TypeLabel = ctk.CTkLabel(
            mainFrame,
            text="User Type*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        TypeLabel.place(anchor="nw",relx=0.55, rely=0.7)

        self.TypeCombo = ctk.CTkOptionMenu(mainFrame,
        width=250,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Patient", "Radiologist", "Consultant", "Specialist"],
        command=self.UserType
        )
        self.TypeCombo.place(anchor="nw",relx=0.55, rely=0.76)

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
            self.backgroundFrame,
            bg_color="#b3c7e5",#"#b3c7e5"
            fg_color="#b3c7e5",
            width=520,
            height=300
        )
        self.Secondframe.place(anchor="nw",relx=0.57, rely=0.17)

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
            bg_color="#b3c7e5",#"#b3c7e5"
            fg_color="#b3c7e5",
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
            bg_color="#b3c7e5",
            fg_color="#b3c7e5",
            width=600,
            height=580
        )
        self.DoctorFrame.place(anchor="nw",relx=0, rely=0)

        self.ImageFrame = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="#b3c7e5",
            fg_color="#b3c7e5",
            border_color="black",
            width=350,
            height=100
        )
        self.ImageFrame.place(anchor="nw",relx=0, rely=0.01)

        self.ImageFrame2 = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="#b3c7e5",
            fg_color="#b3c7e5",
            width=350,
            height=100
        )
        self.ImageFrame2.place(anchor="nw",relx=0, rely=0.2)

        ImportIDButton = ctk.CTkButton(self.DoctorFrame,text="Import ID", command=self.ImportID,width=50)
        ImportIDButton.place(anchor="nw", relx=0.66, rely=0.08)

        ImportLicenseButton = ctk.CTkButton(self.DoctorFrame,text="Import Profession License", command=self.ImportLicense,width=100)
        ImportLicenseButton.place(anchor="nw", relx=0.59, rely=0.3)

        UniLabel = ctk.CTkLabel(
            self.DoctorFrame,
            text="University:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        UniLabel.place(anchor="nw",relx=0, rely=0.4)
        self.UniEntry = ctk.CTkEntry(
        self.DoctorFrame,
        placeholder_text="Input The University You Graduated From...",
        placeholder_text_color="black",
        text_color="black",
        fg_color="#b3c7e5",
        border_color="black",
        width=300,
        height=30
        )
        self.UniEntry.place(anchor="nw",relx=0.2,rely=0.4)

    IDPath = ""
    def ImportID(self):
        self.IDPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        IDImage = ctk.CTkLabel(self.ImageFrame,text="",image=ctk.CTkImage(Image.open(self.IDPath),size=(350,100)))
        IDImage.place(anchor="nw", relx=0, rely=0)

    LicensePath = ""
    def ImportLicense(self):
        self.LicensePath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        LicenseImage = ctk.CTkLabel(self.ImageFrame2,text="",image=ctk.CTkImage(Image.open(self.LicensePath),size=(350,100)))
        LicenseImage.place(anchor="nw", relx=0, rely=0)

    def radiologist(self):
        self.HoldFrame()
        RadiologistFrame = ctk.CTkFrame(
            self.Secondframe,
            bg_color="#b3c7e5",
            fg_color="#b3c7e5",
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
            font=ctk.CTkFont(size=30),
        )
        RadioCenterLabel.place(anchor="nw",relx=0, rely=0.05)

        res = self.db.Select("SELECT Name FROM radiologycenters")
        RadioCenters = [i[0] for i in res]
        self.RadioCenterCombo = ctk.CTkOptionMenu(
        RadiologistFrame,
        width=330,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=RadioCenters,
        font=ctk.CTkFont(size = 25),
        )
        self.RadioCenterCombo.place(anchor="nw",relx=0, rely=0.13)

        RadioCenterCodeLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Center Verification Code:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=28),
        )
        RadioCenterCodeLabel.place(anchor="nw",relx=0, rely=0.25)

        self.RadioCenterCodeEntry = ctk.CTkEntry(
        RadiologistFrame,
        placeholder_text="Input Your Center's Verification Code...",
        text_color="black",
        fg_color="#b3c7e5",
        border_color="black",
        width=400,
        height=35
        )
        self.RadioCenterCodeEntry.place(anchor="nw",relx=0,rely=0.33)

    def Registerbutton(self):
        RegisterButton = ctk.CTkButton(
        self,
        bg_color="#b3c7e5",
        text="Register",
        width= 150,
        height=80,
        font = ctk.CTkFont(size=23),
        command=self.fetchAllData
        )
        RegisterButton.place(anchor="nw", relx=0.535, rely=0.83)

    def fetchAllData(self):
        self.userName = f"{self.firstEntry.get()} {self.SecondEntry.get()}"
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
        if self.firstEntry.get() == "" or self.SecondEntry.get() == "" or self.Phone == "" or self.Email == "" or self.Password == "" or self.ConfirmPassword == "" or self.Gender == 0:
            return 1
        else:
            return -1

    def userNameChecker(self):
        pattern = re.compile("^[a-zA-Z ]*$")
        if pattern.fullmatch(self.userName) is not None:
            return -1
        else:
            return 2
    
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
        res = self.db.Select("SELECT Registercode, Center_Limit FROM radiologycenters WHERE Name=%s",[self.radioCenter])
        limit = res[0][1]
        code = res[0][0]
        if self.radioCenterCode == code and limit > 0:
            limit -= 1
            self.db.Update("UPDATE radiologycenters SET Center_Limit=%s WHERE Name=%s",[limit,self.radioCenter])
            self.db.Commit()
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
            self.IDbinary = self.db.convertToBinaryData(self.IDPath)
            self.LicenseBinary = self.db.convertToBinaryData(self.LicensePath)
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
        return messagebox.showinfo("✅Success", " You have successfully registered a new account ✅ ", icon="info", parent=self.backgroundFrame)

if __name__ == "__main__":
    app = Register()
    app.mainloop()

# Sami
# Ali
# 01526512341
# s_ali@gmail.com