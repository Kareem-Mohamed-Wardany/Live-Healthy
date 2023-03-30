from LoginGUI import *

def MoveTo(UserInfo):
    id = str(UserInfo[0])
    if UserInfo[1] == "patient": # ahmed@gmail.com     PW: 123
        patient = PatGUI(id)
        patient.mainloop()
    if UserInfo[1] == "Radiologist": # salma@gmail.com     PW: 123
        Radiologist = RadioloGUI(id)
        Radiologist.mainloop()
    if UserInfo[1] == "Administrator": # admin@admin.com    PW: admin
        Admin = AdminGUI(id)
        Admin.mainloop()
    if UserInfo[1] in ["Specialist","Consultant"]: # khaled@gmail.com     PW: 123
        Doctor = DocGUI(id)
        Doctor.mainloop()

def Run():
    app = Login()
    app.mainloop()


    if app.Moveto:
        userinfo = User.Login(app.email, app.password)
        MoveTo(userinfo)

    if app.MovetoReg:
        reg = Register()
        reg.mainloop()



Run()
