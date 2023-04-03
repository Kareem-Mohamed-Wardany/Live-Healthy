from AdministratorGUI import *
from DoctorGUI import *
from PatientGUI import *
from RadiologistGUI import *
from LoginGUI import *
from RegisterGUI import RegisterGUI

def MoveTo(UserInfo):
    id = str(UserInfo[0])
    if UserInfo[1].lower() == "patient": # sali@gmail.com       pw: 123
        patient = PatGUI(id)
        patient.mainloop()
    if UserInfo[1].lower() == "radiologist": # salma@gmail.com     PW: 123
        Radiologist = RadioloGUI(id)
        Radiologist.mainloop()
    if UserInfo[1].lower() == "administrator": # admin   PW: admin
        Admin = AdminGUI(id)
        Admin.mainloop()
    if UserInfo[1].lower() in ["specialist","consultant"]: # sherif_mohamed@gmail.com       pw: 123
        Doctor = DocGUI(id)
        Doctor.mainloop()


def StartGUI():
    print("Running")
    app = LoginGUI()
    app.mainloop()


    if app.Moveto:
        userinfo = User.Login(app.email, app.password)
        MoveTo(userinfo)

    if app.MovetoReg:
        reg = RegisterGUI()
        reg.mainloop()