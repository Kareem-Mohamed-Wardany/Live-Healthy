from Patient import *
from Doctor import *
from Radiologist import *


class UserFactory:
    @staticmethod
    def createUser(id, Type):
        
        if Type.lower() == "patient":
            return Patient(id)
        elif Type.lower() in ["doctor", "specialist", "consultant"]:
            return Doctor(id)
        elif Type.lower() == "radiologist":
            return Radiologist(id)


x = UserFactory.createUser(5, "Patient")
print(x.userName)
