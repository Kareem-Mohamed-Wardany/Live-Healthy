class UserFactory:
    @staticmethod
    def createUser(id, Type):
        
        if Type.lower() == "patient":
            from Patient import Patient
            return Patient(id)
        elif Type.lower() in ["doctor", "specialist", "consultant"]:
            from Doctor import Doctor
            return Doctor(id)
        elif Type.lower() == "radiologist":
            from Radiologist import Radiologist
            return Radiologist(id)
        elif Type.lower() == "admin":
            from Administrator import Administrator
            return Administrator(id)

