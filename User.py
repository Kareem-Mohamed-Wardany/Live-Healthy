import base64
import io

from PIL import Image

from Database import *
from GUIHelperFunctions import *
from datetime import date
from fpdf import FPDF

class User:

    # --------------------------------VARIABLES SECTION----------------------------------------------#
    db = Database()  # Create connection with Database to access it

    # General Variables for All Users
    userid = userBalance = userVIPLevel = 0
    userVIPEnd = None
    userName = (
        userMail
    ) = (
        userPassword
    ) = userType = userPhone = userAge = userGender = userSystemApperanceMode = ""

    # define patient extra variables for his own information
    Heart_Diseases = Diabetes = Cancer = Obesity = Smoker = Hypertension = Allergies = 0
    Blood_Type = ""

    # define Specialist|Consultant extra variables for his own information
    University = ID_Card = Prof_License = ""
    Verified = 0

    # define Radiogist extra variables for his own information
    CenterName = ""
    # --------------------------------END OF VARIABLES SECTION------------------------------------------#

    # --------------------------------FUNCTIONS SECTION-------------------------------------------------#
    def __init__(self, email, password):  # constructor Used during Login to get user id
        self.userid = self.db.Select(
            "SELECT ID FROM users WHERE Mail= %s AND Password=%s", [email, password]
        )[0][0]

    def __init__(self, id):  # constructor to fill in the data for the user

        self.userid = id

        res = self.db.Select(
            "SELECT * FROM users WHERE ID= %s", [self.userid]
        )  # Select Query to get the user data

        # assign each data to its variable to be easly use in the system
        (
            self.userName,
            self.userMail,
            self.userPassword,
            self.userType,
            self.userBalance,
            self.userPhone,
            self.userAge,
            self.userSystemApperanceMode,
            self.userGender,
            self.userVIPLevel,
            self.userVIPEnd
        ) = self.fillindata(res[0], [0])

        
        if self.userType == "patient":  # check if the user is a patient
            healthStatus = self.db.Select(
                "SELECT * FROM patienthealthstatus WHERE Patient_ID= %s", [self.userid]
            )  # Select Query to get the patient saved Health Status
            # assign each data to its variable to be easly use in the system
            (
                self.Heart_Diseases,
                self.Diabetes,
                self.Cancer,
                self.Obesity,
                self.Smoker,
                self.Hypertension,
                self.Allergies,
                self.Blood_Type,
            ) = self.fillindata(healthStatus[0], [0])

        if self.userType in [
            "Specialist",
            "Consultant",
        ]:  # check if the user is a Specialist|Consultant
            docData = self.db.Select(
                "SELECT * FROM doctordata WHERE Doctor_ID	= %s", [self.userid]
            )  # Select Query to get the Specialist|Consultant saved data
            (
                self.Verified,
                self.University,
                self.ID_Card,
                self.Prof_License,
            ) = self.fillindata(docData[0], [0])

        if self.userType == "Radiogist":  # check if the user is a Radiogist
            radiodata = self.db.Select(
                "SELECT Center_ID FROM radiologists WHERE Radiologist_ID= %s",
                [self.userid],
            )[0][
                0
            ]  # get the id for Radiology center
            self.CenterName = self.db.Select(
                "SELECT Name FROM radiologycenters WHERE ID= %s", [radiodata]
            )[0][
                0
            ]  # get the Name of Radiology center

    def fillindata(self, input, skipValues=None):
        if skipValues is None:
            skipValues = []
        for i in range(len(input)):
            if i in skipValues:
                continue
            else:
                yield input[i]

    def updateBalance(self, parent, val):
        if val < 0:
            check = val * (-1)
            if check > self.userBalance:
                MessageBox(parent, "error", "Insufficient Funds")
                return -1
        elif val == 0:
            MessageBox(parent, "error", "Invalid Amount")
            return -1
        self.userBalance += val
        self.db.Update(
            "UPDATE users SET Credits_Balance = %s WHERE ID= %s",
            [self.userBalance, self.userid],
        )
        self.db.Commit()

    def checkRequest(self):
        res = self.db.Select(
            "SELECT * FROM requests WHERE Patient_ID= %s", [self.userid]
        )
        return len(res) > 0

    def addRequest(self, ScanPath, prediction, symptoms, illnessTime, medications, extraInfo):
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
                illnessTime
            ],
        )
        self.db.Commit()

    # Specialist|Consultant Functions
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

    def MakePrescription(self, id, Medicine, MedicineComment):
        patient = User(id)
        res = self.db.Select(
            "SELECT X_ray_scan, Prediction FROM requests WHERE Patient_ID= %s",
            [id],
        )
        self.db.write_file(res[0][0], patient.userName)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=15)

        # Add MainPage Style
        pdf.image("asset\\report.png", x=0, y=0, w=219, h=300, type="PNG")

        # Add Doctor information
        pdf.set_xy(20,45)
        DoctorName = f"Doctor {self.userName}"
        pdf.cell(180, 10,txt=DoctorName, ln=1, align="C")
        Doctortitle = f"{self.userType} in Department of Respiratory Diseases at Live Healthy"
        pdf.set_xy(20,55)
        pdf.cell(180, 10,txt=Doctortitle, ln=0, align="C")

        # Add Patient information
        Name = f"Name: {patient.userName}"
        pdf.set_xy(10,70)
        pdf.cell(200, 10, txt=Name, ln=1, align="L")

        Age = f"Age: {str(patient.userAge)}"
        pdf.set_xy(10,80)
        pdf.cell(200, 10, txt=Age, ln=2, align="L")

        Gender = f"Gender: {patient.userGender}"
        pdf.set_xy(40,80)
        pdf.cell(200, 10, txt=Gender, ln=2, align="L")

        Date = f"Date: {date.today().day}/{date.today().month}/{date.today().year}"
        pdf.set_xy(85,80)
        pdf.cell(180, 10, txt=Date, ln=2, align="L")

        Prediction = f"Prediction: {res[0][1]}"
        pdf.set_xy(130,80)
        pdf.cell(180, 10, txt=Prediction, ln=1, align="L")

        pdf.set_xy(15,85)
        pdf.cell(180, 10, txt="_________________________________________________________________", ln=1, align="L")

        pdf.set_xy(10,100)
        # Medicine Section
        for pos,item in enumerate(Medicine):
            pdf.set_font("Times", size=14)
            Med = f"R/ {item}"
            pdf.cell(180, 10, txt=Med, ln=2, align="L")
            pdf.cell(180, 10, txt=MedicineComment[pos], ln=2, align="C")
        file = f"Data\Prescriptions\{patient.userName}.pdf"
        pdf.output(file)
        binaryFile = self.db.convertToBinaryData(file)
        self.db.Update("UPDATE prescriptions SET prescriptionPDF= %s, prescriptionDate = %s Where Patient_ID= %s",[binaryFile, date.today(), patient.userid])
        self.db.Commit()

    # --------------------------------END OF FUNCTIONS SECTION---------------------------------------------#