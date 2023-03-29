import csv
import os
import os.path

from PIL import Image

from Model import *
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
        cls.userSystemApperanceMode = "System"
        cls.userBalance = 0
        cls.userVIPLevel = 0
        cls.userVIPEnd = date(2001, 1, 1)
        cls.CenterName = CenterName
        return cls
    

    def PredictScanFolder(self, FolderPath):
        output = []
        m = ResNetModel()
        valid_images = [".jpg",".gif",".png",".tga"]
        for f in os.listdir(FolderPath):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            FullPath = os.path.join(FolderPath,f)
            print(FullPath)
            imageName= os.path.splitext(f)[0]
            output.append((imageName, m.PredictScan(FullPath,True)))

        return output

    # Generate Excel file
    def createcsv(self, Path, out):
        loc = f"{Path}/Predictions.csv"
        with open(loc, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(out)

