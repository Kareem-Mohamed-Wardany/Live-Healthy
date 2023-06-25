import csv
import os
import os.path
from multiprocessing import Pool
from functools import partial


from PIL import Image

from Model import *
from User import *
from ReturnedValueThreading import *

class Radiologist(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        if id != -1:
            super().__init__(id)
            radiodata = SelectQuery("SELECT Center_ID FROM radiologists WHERE Radiologist_ID= %s",[self.userid], )[0][0]  # get the id for Radiology center
            self.CenterName = SelectQuery("SELECT Name FROM radiologycenters WHERE ID= %s", [radiodata])[0][0] 

    def SaveData(self):
        super().SaveData()
        centerID = SelectQuery("SELECT ID FROM radiologycenters WHERE Name LIKE %s", [self.CenterName])[0][0] 
        InsertQuery(
            "INSERT INTO radiologists (Radiologist_ID, Center_ID) VALUES (%s, %s)",
            [
                self.userid,
                centerID,
            ])
    
    @classmethod
    def CreateRadiologist(cls, name, Mail, Password, Utype, Phone, Age, Gender, CenterName):
        r = cls(-1)
        r.userid = r.GetMaxID() + 1 
        r.userName = name
        r.userMail = Mail
        r.userPassword = Password
        r.userType = Utype
        r.userPhone = Phone
        r.userAge = Age
        r.userGender = Gender
        r.userSystemApperanceMode = "System"
        r.userBalance = 0
        r.userVIPLevel = 0
        r.userVIPEnd = date(2001, 1, 1)
        r.CenterName = CenterName
        return r
    
    def PredictScanFolder(self, FolderPath):
        output = []
        m = ResNetModel()
        valid_images = [".jpg",".gif",".png",".tga",".jpeg"]
        for f in os.listdir(FolderPath):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            FullPath = os.path.join(FolderPath,f)
            imageName= os.path.splitext(f)[0]
            output.append((imageName, m.PredictScan(FullPath, True)))
        return output

    # Generate Excel file
    def createcsv(self, Path, out):
        loc = f"{Path}/Predictions.csv"
        with open(loc, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(out)

