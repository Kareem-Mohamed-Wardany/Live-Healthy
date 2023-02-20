from User import *

class Radiologist(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        super().__init__(id)
        radiodata = self.db.Select("SELECT Center_ID FROM radiologists WHERE Radiologist_ID= %s",[self.userid], )[0][0]  # get the id for Radiology center
        self.CenterName = self.db.Select("SELECT Name FROM radiologycenters WHERE ID= %s", [radiodata])[0][0] 

    def SaveData(self):
        super().SaveData()
        centerID = self.db.Select("SELECT ID FROM radiologycenters WHERE Name LIKE %s", [self.CenterName])[0][0] 
        self.db.Insert(
            "INSERT INTO radiologists (Radiologist_ID, Center_ID) VALUES (%s, %s)",
            [
                self.userid,
                centerID,
            ])
    
    @classmethod
    def CreateRadiologist(cls, name, Mail, Password, Utype, Phone, Age, Gender, CenterName):
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
        cls.CenterName = CenterName
        return cls

