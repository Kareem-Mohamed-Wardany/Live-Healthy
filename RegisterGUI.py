import tkinter as tk
from tkinter import *
from tkcalendar import Calendar

import customtkinter as ctk

from Config import *
from Database import *
from GUIHelperFunctions import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import re
from datetime import datetime



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
        self.patient()
        self.Registerbutton()
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
        self.firstEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your First Name...",
        width=300,
        height=35,
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.firstEntry.place(anchor="nw",relx=0.015,rely=0.12)
        SecondLabel = ctk.CTkLabel(
            mainFrame,
            text="Second Name*",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        SecondLabel.place(anchor="nw", relx=0.55, rely=0.06)
        self.SecondEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Last Name...",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.SecondEntry.place(anchor="nw",relx=0.55,rely=0.12)
        MailLabel = ctk.CTkLabel(
            mainFrame,
            text="Email*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        MailLabel.place(anchor="nw", relx=0.015, rely=0.22)
        self.MailEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Email...",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.MailEntry.place(anchor="nw",relx=0.015,rely=0.27)
        PhoneLabel = ctk.CTkLabel(
            mainFrame,
            text="Phone Number*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PhoneLabel.place(anchor="nw",relx=0.55, rely=0.22)
        self.PhoneEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Phone Number...",
        width=300,
        height=35
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.PhoneEntry.place(anchor="nw",relx=0.55,rely=0.27)
        PassLabel = ctk.CTkLabel(
            mainFrame,
            text="Password*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PassLabel.place(anchor="nw",relx=0.015, rely=0.37)
        self.PassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Input Your Password...",
        width=300,
        height=35,
        show="*"
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.PassEntry.place(anchor="nw",relx=0.015,rely=0.43)
        ConfirmPassLabel = ctk.CTkLabel(
            mainFrame,
            text="Confirm Password*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        ConfirmPassLabel.place(anchor="nw",relx=0.55, rely=0.37)
        self.ConfirmPassEntry = ctk.CTkEntry(
        mainFrame,
        placeholder_text="Confirm Your Password...",
        width=300,
        height=35,
        show="*"
        )
        # n, ne, e, se, s, sw, w, nw, or center
        self.ConfirmPassEntry.place(anchor="nw",relx=0.55,rely=0.43)
        AgeLabel = ctk.CTkLabel(
            mainFrame,
            text="Date of Birth*",
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
        # cal.get_date()
        GenderLabel = ctk.CTkLabel(
            mainFrame,
            text="Gender*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        GenderLabel.place(anchor="nw",relx=0.55, rely=0.52)
        self.GenderVar = tk.IntVar(value = 0)
        MaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Male",
            variable=self.GenderVar,
            value=1
        )
        MaleRadio.place(anchor="nw",relx=0.57, rely=0.58)
        FemaleRadio = ctk.CTkRadioButton(
            mainFrame,
            text="Female",
            variable=self.GenderVar,
            value=2
        )
        FemaleRadio.place(anchor="nw",relx=0.57, rely=0.64)
        TypeLabel = ctk.CTkLabel(
            mainFrame,
            text="User Type*",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        TypeLabel.place(anchor="nw",relx=0.55, rely=0.7)
        self.TypeCombo = ctk.CTkOptionMenu(mainFrame,
        width=300,
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
        elif Utype=="Consultant" or Utype=="Specialist":
            self.doctor()
            self.Registerbutton()
        elif Utype=="Radiologist":
            self.radiologist()
            self.Registerbutton()
    def patient(self):
        PatientFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=600,
            height=580
        )
        PatientFrame.place(anchor="nw",relx=0.57, rely=0.17)
        HealthLabel = ctk.CTkLabel(
            PatientFrame,
            text="Patient's Health Status",
            width=65,
            height=20,
            font=ctk.CTkFont(size=30),
        )
        HealthLabel.place(anchor="nw",relx=0.2, rely=0.04)
        self.patientsHealthCheck()
    def patientsHealthCheck (self):
        PatientHealthFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=515,
            height=380
        )
        PatientHealthFrame.place(anchor="nw",relx=0.59, rely=0.3)
        self.Heart = IntVar()
        HeartCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Heart Diseases",
            variable=self.Heart,
            onvalue=1,
            offvalue=0
        )
        HeartCheck.place(anchor="nw",relx=0.15, rely=0.03)

        self.Diabetes = IntVar()
        DiabetesCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Diabetes",
            variable=self.Diabetes,
            onvalue=1,
            offvalue=0
        )
        DiabetesCheck.place(anchor="nw",relx=0.6, rely=0.03)

        
        self.Cancer = IntVar()
        CancerCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Cancer",
            variable=self.Cancer,
            onvalue=1,
            offvalue=0
        )
        CancerCheck.place(anchor="nw",relx=0.15, rely=0.17)

        self.Obesity = IntVar()
        ObesityCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Obesity",
            variable=self.Obesity,
            onvalue=1,
            offvalue=0
        )
        ObesityCheck.place(anchor="nw",relx=0.6, rely=0.17)


        self.Smoker = IntVar()
        SmokerCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Smoker",
            variable=self.Smoker,
            onvalue=1,
            offvalue=0
        )
        SmokerCheck.place(anchor="nw",relx=0.15, rely=0.31)

        self.Hypertension = IntVar()
        HypertensionCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Hypertension",
            variable=self.Hypertension,
            onvalue=1,
            offvalue=0
        )
        HypertensionCheck.place(anchor="nw",relx=0.6, rely=0.31)
        self.Allergies = IntVar()
        AllergiesCheck = ctk.CTkCheckBox(
            PatientHealthFrame,
            text="Allergies",
            variable=self.Allergies,
            onvalue=1,
            offvalue=0
        )
        AllergiesCheck.place(anchor="nw",relx=0.15, rely=0.45)
        BloodTypeLabel = ctk.CTkLabel(
            PatientHealthFrame,
            text="Blood Type:",
            width=100,
            height=25,
            font=ctk.CTkFont(size=14),
        )
        BloodTypeLabel.place(anchor="nw", relx=0.469, rely=0.45)
        self.BloodTypeCombo = ctk.CTkOptionMenu(
        PatientHealthFrame,
        width=100,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Unknown","O-","O+","B-","B+","A-","A+","AB-","AB+"],
        font = ctk.CTkFont(size =17)
        )
        self.BloodTypeCombo.place(anchor="nw",relx=0.66, rely=0.45)
    def doctor(self):
        self.DoctorFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=600,
            height=580
        )
        self.DoctorFrame.place(anchor="nw",relx=0.57, rely=0.17)
        self.ImageFrame = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="#969696",
            width=350,
            height=197
        )
        self.ImageFrame.place(anchor="nw",relx=0.05, rely=0.01)
        self.ImageFrame2 = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="#969696",
            width=350,
            height=197
        )
        self.ImageFrame2.place(anchor="nw",relx=0.05, rely=0.38)
        ImportIDButton = ctk.CTkButton(self.DoctorFrame,text="Import ID", command=self.ImportID)
        ImportIDButton.place(anchor="nw", relx=0.66, rely=0.08)
        ImportLicenseButton = ctk.CTkButton(self.DoctorFrame,text="Import Profession License", command=self.ImportLicense)
        ImportLicenseButton.place(anchor="nw", relx=0.641, rely=0.49)
        UniLabel = ctk.CTkLabel(
            self.DoctorFrame,
            text="University:",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        UniLabel.place(anchor="nw",relx=0.041, rely=0.75)
        self.UniEntry = ctk.CTkEntry(
        self.DoctorFrame,
        placeholder_text="Input The University You Graduated From...",
        width=300,
        height=30
        )
        self.UniEntry.place(anchor="nw",relx=0.21,rely=0.748)
    def ImportID(self):
        self.IDPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        ScanImage = ctk.CTkLabel(self.ImageFrame,text="",image=ctk.CTkImage(Image.open(self.IDPath),size=(350,197)))
        ScanImage.place(anchor="nw", relx=0, rely=0)
    def ImportLicense(self):
        self.LicensePath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        ScanImage = ctk.CTkLabel(self.ImageFrame2,text="",image=ctk.CTkImage(Image.open(self.LicensePath),size=(350,197)))
        ScanImage.place(anchor="nw", relx=0, rely=0)
    def radiologist(self):
        RadiologistFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=600,
            height=580
        )
        RadiologistFrame.place(anchor="nw",relx=0.57, rely=0.17)

        RadioCenterLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Radiology Center:",
            width=65,
            height=20,
            font=ctk.CTkFont(size=30),
        )
        RadioCenterLabel.place(anchor="nw",relx=0.27, rely=0.1)

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
        self.RadioCenterCombo.place(anchor="nw",relx=0.21, rely=0.189)
        RadioCenterCodeLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Center Verification Code:",
            width=65,
            height=20,
            font=ctk.CTkFont(size=28),
        )
        RadioCenterCodeLabel.place(anchor="nw",relx=0.21, rely=0.36)
        self.RadioCenterCodeEntry = ctk.CTkEntry(
        RadiologistFrame,
        placeholder_text="Input Your Center's Verification Code...",
        width=400,
        height=35
        )
        self.RadioCenterCodeEntry.place(anchor="nw",relx=0.15,rely=0.44)
    def Registerbutton(self):
        RegisterButtonFrame = ctk.CTkFrame(
            self,
            bg_color="#969696",
            width=200,
            height=80
        )
        RegisterButtonFrame.place(anchor="nw", relx=0.71, rely=0.84)

        RegisterButton = ctk.CTkButton(
        RegisterButtonFrame,
        text="Register",
        width= 200,
        height=80,
        font = ctk.CTkFont(size=23),
        command=self.fetchAllData
        )
        RegisterButton.place(anchor="nw", relx=0, rely=0)
    def fetchAllData(self):
        self.userName = f"{self.firstEntry.get()} {self.SecondEntry.get()}"
        self.Email = self.MailEntry.get()
        self.Phone = self.PhoneEntry.get()
        self.Password = self.PassEntry.get()
        self.ConfirmPassword = self.ConfirmPassEntry.get()
        self.DoB = datetime.strptime(self.cal.get_date(), '%m/%d/%y').date()
        self.Gender = self.gender()
        self.UserType = self.TypeCombo.get()
        self.dataValidator()
        self.fetchUserTypeData()
        self.emptyUserTypeFields()
        self.insertUserInfo()
        return messagebox.showinfo("✅Success", " You have successfully registered a new account ✅ ", icon="info", parent=self)

    def gender(self):
        return "Male" if self.GenderVar.get() == 1 else "Female"
    def dataValidator(self):
        if self.emptyMainFields():
            return MessageBox(self, "error", "Please fill all the fields!")
        if self.userNameChecker():
            return MessageBox(self, "error", "Names can't include numbers!")
        self.passwordChecker()
        if self.emailChecker():
            return MessageBox(self, "error", "Invalid email address!")
        self.phoneChecker()     
    def CheckRadioCenter(self):
        res = self.db.Select("SELECT Registercode, Center_Limit FROM radiologycenters WHERE Name=%s",[self.radioCenter])
        limit = res[0][1]
        code = res[0][0]
        if self.radioCenterCode == code and limit > 0:
            limit -= 1
            self.db.Update("UPDATE radiologycenters SET Center_Limit=%s WHERE Name=%s",[limit,self.radioCenter])
            self.db.Commit()
        if limit == 0:
            return MessageBox(self, "error", "Your radiology center has reached its maximum amount of users!")
        if self.radioCenterCode != code:
            return MessageBox(self, "error", "Invalid radiology center code!")
    def emptyMainFields(self):
        return (
            self.firstEntry.get() == ""
            or self.SecondEntry.get() == ""
            or self.Phone == ""
            or self.Email == ""
            or self.Password == ""
            or self.ConfirmPassword == ""
            or self.Gender == 0
        )
    def emptyUserTypeFields(self):
        if (
            self.TypeCombo.get() == "Specialist"
            or self.TypeCombo.get() == "Consultant"
        ) and (
            len(self.IDPath) == 0
            or len(self.LicensePath) == 0
            or len(self.uni) == 0
        ):
            return MessageBox(self, "error", "Please fill all the fields!")
    def passwordChecker(self):
        if self.Password != self.ConfirmPassword:
            return MessageBox(self, "error", "Password Mismatch!")
        if len(self.Password) < 8:
            return MessageBox(self, "error", "Password should be longer than 8 characters!")
    def userNameChecker(self):
        return any(char.isdigit() for char in self.userName)
    def emailChecker(self):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        return not re.match(pat,self.Email)
    def phoneChecker(self):
        if not self.Phone.isnumeric():
            return MessageBox(self, "error", "Invalid phone number!")
        if len(self.Phone) < 11 or len(self.Phone) > 15:
            return MessageBox(self, "error", "Invalid phone number!")
    def fetchUserTypeData(self):
        if self.TypeCombo.get() == "Patient":
            self.heart = self.Heart.get()
            self.diabetes = self.Diabetes.get()
            self.cancer = self.Cancer.get()
            self.obesity = self.Obesity.get()
            self.smoker = self.Smoker.get()
            self.hypertension = self.Hypertension.get()
            self.allergies = self.Allergies.get()
            self.Blood = self.BloodTypeCombo.get()
        #print(self.heart, self.diabetes, self.hypertension, self.allergies, self.cancer, self.obesity, self.smoker, self.Blood)
        if self.TypeCombo.get() == "Radiologist":
            self.radioCenter = self.RadioCenterCombo.get()
            self.radioCenterCode = self.RadioCenterCodeEntry.get()
            self.CheckRadioCenter()
        #print(self.radioCenterCode, self.radioCenter)
        if self.TypeCombo.get() == "Specialist" or self.TypeCombo.get() == "Consultant":
            if self.UniEntry.get() == "":
                return MessageBox(self, "error", "Please fill all the fields!")
            else:
                self.uni = self.UniEntry.get()
                self.IDbinary = self.db.convertToBinaryData(self.IDPath)
                self.LicenseBinary = self.db.convertToBinaryData(self.LicensePath)
    def insertUserInfo(self):
        appearence = "System"
        res = self.db.Select("SELECT ID FROM users")
        IDs = [i[0] for i in res]
        newID = len(IDs)
        if self.TypeCombo.get() == "Patient":
            self.db.Insert("INSERT INTO users (ID, Name, Mail, Password, Account_Type, Phone, Age, 	Apperance_Mode, Gender) VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s)",[newID, self.userName, self.Email, self.Password, self.TypeCombo.get(),self.Phone,self.DoB,appearence,self.Gender])
            self.db.Insert("INSERT INTO patienthealthstatus VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s)",[newID, self.heart, self.diabetes, self.cancer,self.obesity,self.smoker,self.hypertension,self.allergies,self.Blood])
            self.db.Commit()
        if self.TypeCombo.get() == "Radiologist":
            self.db.Insert("INSERT INTO users (ID, Name, Mail, Password, Account_Type, Phone, Age, 	Apperance_Mode, Gender) VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s)",[newID, self.userName, self.Email, self.Password, self.TypeCombo.get(),self.Phone,self.DoB,appearence,self.Gender])
            res = self.db.Select("SELECT ID FROM radiologycenters where Name=%s",[self.radioCenter])
            centerID = res[0][0]
            self.db.Insert("INSERT INTO radiologists VALUES (%s,%s)",[newID,centerID])
            self.db.Commit()
        if  self.TypeCombo.get() == "Consultant" or self.TypeCombo.get() == "Specialist":
            self.db.Insert("INSERT INTO users (ID, Name, Mail, Password, Account_Type, Phone, Age, 	Apperance_Mode, Gender) VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s)",[newID, self.userName, self.Email, self.Password, self.TypeCombo.get(),self.Phone,self.DoB,appearence,self.Gender])
            self.db.Insert("INSERT INTO doctordata VALUES (%s,%s,%s,%s,%s)",[newID, 0, self.uni,self.IDbinary, self.LicenseBinary])
            self.db.Commit()


if __name__ == "__main__":
    app = Register()
    app.resizable(False, False)  # Disable resize for GUI
    center(app, 1280, 720)  # center window in your screen
    app.mainloop()

