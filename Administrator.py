from User import *
from tkinter import filedialog
from datetime import date, timedelta


class Administrator(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        super().__init__(id)

    def getAllReports(self):
        return self.db.Select(
            "SELECT reports.Issuer_ID, reports.Reporter_ID, reports.Reason, reports.ReportDate, oldchat.ChatLOGS FROM reports, oldchat WHERE reports.Reporter_ID = oldchat.Doc_ID AND reports.Issuer_ID = oldchat.Patient_ID AND reports.ReportDate = oldchat.EndDate ORDER BY reports.ReportDate ASC")

    def RevokeSuspension(self, master, id, Update):
        self.db.Delete("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        self.db.Delete("DELETE FROM suspended WHERE User_ID= %s",[id])
        self.db.Commit()
        Update()
        MessageBox(master,"info","Suspension revoked for the patient")
        

    def ConfirmSuspension(self, master, id, update):
        self.db.Delete("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        self.db.Update("UPDATE suspended SET Suspention_Type= %s WHERE User_ID= %s",["Permanent",id])
        self.db.Commit()
        update()
        MessageBox(master,"info","Patient permanently suspended")

# a = Administrator(0)
# a.getAllReports(
# )