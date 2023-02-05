import base64
import io

from PIL import Image

from Database import *
from GUIHelperFunctions import *


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
            self.userVIPLevel,
            self.userVIPEnd,
            self.userSystemApperanceMode,
            self.userGender,
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

    # --------------------------------END OF FUNCTIONS SECTION---------------------------------------------#
