from User import *
import subprocess
from tkinter import filedialog
from datetime import date, timedelta
# from Model import *

class Patient(User):

    db = Database()  # Create connection with Database to access it

    BasePredictScanPrice = 75
    BaseChatPrice = 150

    def __init__(self, id):
        super().__init__(id)
        res= self.db.Select("SELECT * FROM patienthealthstatus WHERE Patient_ID= %s",[self.userid])
        (
            self.Heart_Diseases,
            self.Diabetes,
            self.Cancer,
            self.Obesity,
            self.Smoker,
            self.Hypertension,
            self.Allergies,
            self.Blood_Type,
            ) = self.fillindata(res[0], [0])

    def SaveData(self):
        super().SaveData()
        self.db.Insert(
            "INSERT INTO patienthealthstatus (Patient_ID, Heart_Diseases, Diabetes, Cancer, Obesity, Smoker, Hypertension, Allergies, Blood_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                self.Heart_Diseases,
                self.Diabetes,
                self.Cancer,
                self.Obesity,
                self.Smoker,
                self.Hypertension,
                self.Allergies,
                self.Blood_Type,
            ])
    
    @classmethod
    def CreatePatient(cls, name, Mail, Password, Utype, Phone, Age, Gender,HD = 0, diabetes = 0, cancer = 0, obesity = 0, smoker = 0, hypertension = 0, Allergies = 0, BloodType = "UNKNOWN"):
        cls.userid = cls.GetMaxID(cls) + 1 
        cls.userName = name
        cls.userMail = Mail
        cls.userPassword = Password
        cls.userType = Utype
        cls.userPhone = Phone
        cls.userAge = Age
        cls.userGender = Gender
        cls.userSystemApperanceMode = "Light"
        cls.userBalance = 0
        cls.userVIPLevel = 0
        cls.userVIPEnd = date(2001, 1, 1)
        cls.Heart_Diseases = HD
        cls.Diabetes = diabetes
        cls.Cancer = cancer
        cls.Obesity = obesity
        cls.Smoker = smoker
        cls.Hypertension = hypertension
        cls.Allergies = Allergies
        cls.Blood_Type = BloodType
        return cls

    def checkRequest(self):
        res = self.db.Select("SELECT * FROM requests WHERE Patient_ID= %s", [self.userid])
        return len(res) > 0

    def CreateRequest(
        self, ScanPath, prediction, symptoms, illnessTime, medications, extraInfo
    ):
        binaryimage = self.db.convertToBinaryData(ScanPath)
        RequestDate = date.today()
        self.db.Insert(
            "INSERT INTO requests (Patient_ID, Request_Date, Request_Status, Symptoms, X_ray_scan, Prediction, Medications, Extra_Info, Illness_Time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                RequestDate,
                "waiting",
                symptoms,
                binaryimage,
                prediction,
                medications,
                extraInfo,
                illnessTime,
            ],
        )
        self.db.Commit()

    def RequestData(self):
        res = self.db.Select(
            "SELECT Symptoms, X_ray_scan, Prediction, Medications, Extra_Info, Illness_Time FROM requests WHERE Patient_ID= %s",
            [self.userid],
        )
        return res[0]

    def PredictMyScan(self, ScanPath, SaveType):
        m = ResNetModel()
        prediction = m.PredictScan(ScanPath)
        self.max1 = 0
        if SaveType == "Two":
            self.max2 = 0
            self.p1=""
            self.p2=""
            for i in prediction:
                value = float(i[1].split("%")[0])
                if value > self.max1 or value > self.max2:
                    if self.max1 < self.max2:
                        self.max1 = value
                        self.p1 = i[0]
                    else:
                        self.max2 = value
                        self.p2 = i[0]

            Label1 = f"{self.p1} ➜ {self.max1}%"
            Label2 = f"{self.p2} ➜ {self.max2}%"
            return Label1, Label2
        elif SaveType == "One":
            for i in prediction:
                value = float(i[1].split("%")[0])
                if value > self.max1:
                    self.max1 = value
                    res= i[0]
            return res

    def SavePrediction(self, Scanpath):
        newpath = Scanpath.split(".")[0]
        newpath = f"{newpath}.txt"
        with open(newpath, "w") as f:
            f.write(f"Highest Class Percentage: {self.p1} --> {self.max1}% \n")
            f.write(f"Second Class Percentage: {self.p2} --> {self.max2}%")

    def PriceInfo(self, ContextType):
        if ContextType =="Chat":
            if self.userVIPLevel == 1:
                Credits = self.GetDiscount(self.BaseChatPrice, 15)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
            elif self.userVIPLevel == 2:
                Credits = self.GetDiscount(self.BaseChatPrice, 50)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
            elif self.userVIPLevel == 3:
                Credits = self.GetDiscount(self.BaseChatPrice, 100)
                Infotext = "Chat with our doctors is Free"
            else:
                self.Credits = self.GetDiscount(self.BaseChatPrice, 0)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
        else:
            if self.userVIPLevel == 1:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 15)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
            elif self.userVIPLevel == 2:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 50)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
            elif self.userVIPLevel == 3:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 100)
                Infotext = "X-ray Scan prediction is Free"
            else:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 0)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
        return Infotext, Credits

    def GetDiscount(self, value, percentage):
        return int(value - (value * (percentage/100)))

    def Subscribe(self, button, master, LeftSideBar):
        if button == "bronze":
            level = 1
            value = -100
        elif button == "silver":
            level = 2
            value = -190
        elif button == "gold":  
            level = 3
            value = -350
        res = self.updateBalance(master, value)
        if res != -1:
            if self.userVIPEnd < date.today():
                self.userVIPEnd = date.today() + timedelta(days=30)
            else:
                self.userVIPEnd += timedelta(days=30)
            self.userVIPLevel = level
            self.db.Update("UPDATE users SET Vip_Level= %s, Vip_End_Date= %s WHERE ID = %s",[self.userVIPLevel, self.userVIPEnd, self.userid])
            self.db.Commit()
            LeftSideBar() # Update Left Side bar in GUI passed as a function
            MessageBox(master,"info","Purchase Complete")

    def Purchase(self, button, master, LeftSideBar, CardChecked):
        if CardChecked == False:  #
            MessageBox(master, "error", "Credit Card is not checked")
        else:
            if button == "1":
                value = 100
            elif button == "2":
                value = 200
            elif button == "3":  
                value = 400
            res = self.updateBalance(master, value)
            if res != -1:
                LeftSideBar() # Update Left Side bar in GUI passed as a function
                MessageBox(master,"info","Balance Recharge Completed")

    def MyPrescriptionGenerated(self, id):
        res = self.db.Select(
            "SELECT prescriptions.prescriptionPDF FROM prescriptions, chatdata WHERE prescriptions.Patient_ID= %s AND prescriptions.Doc_ID= %s AND DATE(prescriptions.prescriptionDate) >= DATE(chatdata.StartDate)",
            [self.userid, id],
        )[0][0]
        return len(res) != 0

    def ShowPrescription(self, event, id, master):
        path = f"Data\Prescriptions\{self.userName}.pdf"
        if self.MyPrescriptionGenerated(id):
            return MessageBox(master, "info", "Prescription is not created yet")
        self.Prescription = self.db.Select("SELECT prescriptions.prescriptionPDF FROM prescriptions, chatdata WHERE prescriptions.Patient_ID= %s AND prescriptions.Doc_ID= %s AND DATE(prescriptions.prescriptionDate) >= DATE(chatdata.StartDate)",[self.userid, id])[0][0]
        self.db.write_file(self.Prescription, path)
        subprocess.Popen([path], shell=True)

    def MyPrescriptions(self):
        return self.db.Select("SELECT Doc_ID, prescriptionDate, prescriptionPDF FROM prescriptions WHERE Patient_ID = %s ORDER BY prescriptionDate DESC",[self.userid]) 

    def DownloadPrescription(self, event, presDate, presPDF, master):
        SavePath = filedialog.askdirectory(title="Select Where to Download Prescription")
        FullPathName = f"{SavePath}/Prescription_{presDate}.pdf"
        self.db.write_file(presPDF, FullPathName)
        subprocess.Popen([FullPathName], shell=True)  # Show the Prescription for the patient
        return MessageBox(master,"info","Prescription saved successfully")