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
    # --------------------------------END OF VARIABLES SECTION------------------------------------------#

    # --------------------------------FUNCTIONS SECTION-------------------------------------------------#
    def __init__(self, id):
        # constructor Used during Login to get user id
        self.userid = id
        res = self.db.Select("SELECT * FROM users WHERE ID= %s", [self.userid]) 
        (self.userName,
        self.userMail,
        self.userPassword,
        self.userType,
        self.userBalance,
        self.userPhone,
        self.userAge,
        self.userSystemApperanceMode,
        self.userGender,
        self.userVIPLevel,
        self.userVIPEnd) = self.fillindata(res[0],[0])

    def GetMaxID(self):
        return self.db.Select("SELECT MAX(ID) FROM users")[0][0]

    def CalcAge(self, Birthdate):
        return (
            date.today().year
            - Birthdate.year
            - (
                (date.today().month, date.today().day)
                < (Birthdate.month, Birthdate.day)
            )
        )

    @classmethod
    def CreateUser(cls, name, Mail, Password, Utype, Phone, Age, Gender):

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
        return cls
    
    @classmethod
    def Login(cls, email, password):
        res = cls.db.Select(
            "SELECT ID, Account_Type FROM users WHERE Mail LIKE %s AND Password=%s", [email, password]
        )
        if len(res) == 0:
            return messagebox.showerror("User not found","Please Enter a valid email address and password")
        cls.userid = res[0][0]
        cls.userType = res[0][1]
        return cls.userid, cls.userType

    def Logout(self):
        pass

    def SaveData(self):
        self.db.Insert(
            "INSERT INTO users (ID, Name, Mail, Password, Type, Phone, Age, Gender, System_Apperance_Mode, Balance, VIP_Level, VIP_End) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                self.userName,
                self.userMail,
                self.userPassword,
                self.userType,
                self.userPhone,
                self.userAge,
                self.userGender,
                self.userSystemApperanceMode,
                self.userBalance,
                self.userVIPLevel,
                self.userVIPEnd]
        )

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

    def SetApperanceMode(self, mode):
        self.userSystemApperanceMode = mode
        self.db.Update(
            "UPDATE users SET Apperance_Mode = %s WHERE ID= %s",
            [mode, self.userid],
        )
        self.db.Commit()
    # --------------------------------END OF FUNCTIONS SECTION---------------------------------------------#