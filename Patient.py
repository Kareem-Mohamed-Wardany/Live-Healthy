from User import *

class Patient(User):

    db = Database()  # Create connection with Database to access it

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

    def addRequest(
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