import subprocess

from User import *

class Doctor(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        super().__init__(id)
        res = self.db.Select(
            "SELECT * FROM doctordata WHERE Doctor_ID= %s", [self.userid]
        )
        (
            self.Verified,
            self.University,
            self.ID_Card,
            self.Prof_License,
        ) = self.fillindata(res[0], [0])

    def SaveData(self):
        super().SaveData()
        self.db.Insert(
            "INSERT INTO doctordata (Doctor_ID, Verified, University, ID_Card, Prof_License) VALUES (%s, %s, %s, %s, %s)",
            [
                self.userid,
                self.Verified,
                self.University,
                self.ID_Card,
                self.Prof_License,
            ],
        )

    @classmethod
    def CreateDoctor(
        cls,
        name,
        Mail,
        Password,
        Utype,
        Phone,
        Age,
        Gender,
        University,
        ID_Card,
        Prof_License,
        Verified=0,
    ):
        cls.userid = cls.GetMaxID(cls) + 1
        cls.userName = name
        cls.userMail = Mail
        cls.userPassword = Password
        cls.userType = Utype
        cls.userPhone = Phone
        cls.userAge = Age
        cls.userGender = Gender
        cls.userSystemApperanceMode = "System"
        cls.userBalance = 0
        cls.userVIPLevel = 0
        cls.userVIPEnd = date(2001, 1, 1)
        cls.Verified = Verified
        cls.University = University
        cls.ID_Card = ID_Card
        cls.Prof_License = Prof_License
        return cls

    def ReportUser(self, userID, Reason):
        ReportDate = date.today()
        self.db.Insert(
            "INSERT INTO reports (Issuer_ID, Reporter_ID, Reason, ReportDate) VALUES (%s, %s, %s, %s)",
            [userID, self.userid, Reason, ReportDate],
        )
        self.db.Insert(
            "INSERT INTO suspended (User_ID, Suspention_Type, Suspention_Date, Reason) VALUES (%s, %s, %s, %s)",
            [userID, "temp", ReportDate, Reason],
        )
        self.db.Commit()

    def GetMyChatMembers(self):
        return self.db.Select(
            "SELECT Patient_ID FROM chatdata WHERE Chat_Status = %s and Doc_ID = %s",
            ["ongoing", self.userid],
        )

    def HandlePrescription(self, event, id, FillMedication):
        patient = User(id)
        path = f"Data\Prescriptions\{patient.userName}.pdf"
        if not self.PrescriptionGenerated(id):
            subprocess.Popen([path], shell=True)  # Show the Prescription for the Doctor
        else:
            FillMedication

    def MakePrescription(self, id, Medicine, MedicineComment):
        patient = User(id)
        res = self.db.Select(
            "SELECT X_ray_scan, Prediction FROM requests WHERE Patient_ID= %s",
            [id],
        )
        # self.db.write_file(res[0][0], patient.userName)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=15)

        # Add MainPage Style
        pdf.image("asset\\report.png", x=0, y=0, w=219, h=300, type="PNG")

        # Add Doctor information
        pdf.set_xy(20, 45)
        DoctorName = f"Doctor {self.userName}"
        pdf.cell(180, 10, txt=DoctorName, ln=1, align="C")
        Doctortitle = (
            f"{self.userType} in Department of Respiratory Diseases at Live Healthy"
        )
        pdf.set_xy(20, 55)
        pdf.cell(180, 10, txt=Doctortitle, ln=0, align="C")

        # Add Patient information
        Name = f"Name: {patient.userName}"
        pdf.set_xy(10, 70)
        pdf.cell(200, 10, txt=Name, ln=1, align="L")

        Age = f"Age: {str(patient.CalcAge(patient.userAge))}"
        pdf.set_xy(10, 80)
        pdf.cell(200, 10, txt=Age, ln=2, align="L")

        Gender = f"Gender: {patient.userGender}"
        pdf.set_xy(40, 80)
        pdf.cell(200, 10, txt=Gender, ln=2, align="L")

        Date = f"Date: {date.today().day}/{date.today().month}/{date.today().year}"
        pdf.set_xy(85, 80)
        pdf.cell(180, 10, txt=Date, ln=2, align="L")

        Prediction = f"Prediction: {res[0][1]}"
        pdf.set_xy(130, 80)
        pdf.cell(180, 10, txt=Prediction, ln=1, align="L")

        pdf.set_xy(15, 85)
        pdf.cell(
            180,
            10,
            txt="_________________________________________________________________",
            ln=1,
            align="L",
        )

        pdf.set_xy(10, 100)
        # Medicine Section
        for pos, item in enumerate(Medicine):
            pdf.set_font("Times", size=14)
            Med = f"R/ {item}"
            pdf.cell(180, 10, txt=Med, ln=2, align="L")
            pdf.cell(180, 10, txt=MedicineComment[pos], ln=2, align="C")
        file = f"Data\Prescriptions\{patient.userName}.pdf"
        pdf.output(file)
        binaryFile = self.db.convertToBinaryData(file)
        self.db.Update(
            "UPDATE prescriptions SET prescriptionPDF= %s, prescriptionDate = %s Where Patient_ID= %s",
            [binaryFile, date.today(), patient.userid],
        )
        self.db.Commit()

    def PrescriptionGenerated(self, id):
        res = self.db.Select("SELECT prescriptions.prescriptionPDF FROM prescriptions, chatdata WHERE prescriptions.Patient_ID= %s AND prescriptions.Doc_ID= %s AND DATE(prescriptions.prescriptionDate) >= DATE(chatdata.StartDate)",[id, self.userid])
        return len(res) != 0

    def EndChat(self, id, EndType):
        EndDate = date.today() 
        res = self.db.Select("SELECT Chat_Logs, StartDate FROM chatdata WHERE Patient_ID= %s",[id])
        self.db.Insert("INSERT INTO oldchat (Patient_ID, Doc_ID, ChatLOGS, StartDate, EndDate, EndType) VALUES (%s, %s, %s, %s, %s, %s)",[id, self.userid, res[0][0], res[0][1], EndDate, EndType])
        self.db.Delete("DELETE FROM chatdata WHERE Patient_ID= %s",[id])
        self.db.Delete("DELETE FROM requests WHERE Patient_ID= %s",[id])
        self.db.Commit()

    def LoadWaitingPatientRequests(self):
        return self.db.Select(
            "SELECT requests.Patient_ID, requests.Request_Date, users.Name, users.Gender, users.DateOfBirth, users.Vip_Level FROM users, requests where users.ID = requests.Patient_ID and requests.Request_Status = %s ORDER BY users.Vip_Level DESC, DATE (requests.Request_Date) ASC",
            ["waiting"],
        )

    def AssignMePatient(self, id):
        # UPDATE requests SET Request_Status = "waiting"
        self.db.Update(
            "UPDATE requests SET Request_Status = %s WHERE Patient_ID= %s",
            ["ongoing", id],
        )
        self.db.Insert(
            "INSERT INTO chatdata (Patient_ID, Doc_ID, Chat_Status, StartDate) Values (%s,%s,%s,%s)",
            [id, self.userid, "ongoing", date.today()],
        )
        self.db.Insert(
            "INSERT INTO prescriptions (Patient_ID, Doc_ID) Values (%s,%s)",
            [id, self.userid],
        )
        self.db.Commit()

