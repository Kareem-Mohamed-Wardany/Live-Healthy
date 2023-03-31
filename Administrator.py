from User import *
from tkinter import filedialog
from datetime import date, timedelta


class Administrator(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        super().__init__(id)

    def getAllReports(self):
        return SelectQuery(
            "SELECT reports.Issuer_ID, reports.Reporter_ID, reports.Reason, reports.ReportDate, oldchat.ChatLOGS FROM reports, oldchat WHERE reports.Reporter_ID = oldchat.Doc_ID AND reports.Issuer_ID = oldchat.Patient_ID AND reports.ReportDate = oldchat.EndDate ORDER BY reports.ReportDate ASC")

    def RevokeSuspension(self, master, id, Update):
        DeleteQuery("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        DeleteQuery("DELETE FROM suspended WHERE User_ID= %s",[id])
        Update()
        MessageBox(master,"info","Suspension revoked for the patient")

    def ConfirmSuspension(self, master, id, update):
        DeleteQuery("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        UpdateQuery("UPDATE suspended SET Suspention_Type= %s WHERE User_ID= %s",["Permanent",id])
        update()
        MessageBox(master,"info","Patient permanently suspended")

    def getUnverifiedDoctors(self):
        return SelectQuery("SELECT doctordata.Doctor_ID, users.Name, doctordata.University, doctordata.ID_Card, doctordata.Prof_License FROM doctordata,users WHERE doctordata.Doctor_ID = users.ID AND doctordata.Verified =%s ORDER BY doctordata.Doctor_ID ASC",[0])

    def VerifyDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[1, id])
        update()
        MessageBox(master,"info","Doctor Verified")

    def BanDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[-1, id])
        InsertQuery("INSERT INTO suspended (User_ID, Suspention_Type, Suspention_Date, Reason) VALUES (%s, %s, %s, %s)",[id, "Permanent",date.today(),"Register With Fake ID and License",])
        update()
        MessageBox(master,"info","Doctor Suspended")


