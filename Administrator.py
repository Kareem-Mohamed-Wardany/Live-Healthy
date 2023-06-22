import smtplib
import ssl
from datetime import date, timedelta
from email.message import EmailMessage
from tkinter import filedialog

from User import *


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
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been re-activated successfully")
        Update()
        messagebox.showinfo("info","Suspension revoked for the patient")

    def ConfirmSuspension(self, master, id, update):
        DeleteQuery("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        UpdateQuery("UPDATE suspended SET Suspention_Type= %s WHERE User_ID= %s",["Permanent",id])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been permanently suspended")
        update()
        messagebox.showinfo("info","Patient permanently suspended")

    def getUnverifiedDoctors(self):
        return SelectQuery("SELECT doctordata.Doctor_ID, users.Name, doctordata.University, doctordata.ID_Card, doctordata.Prof_License FROM doctordata,users WHERE doctordata.Doctor_ID = users.ID AND doctordata.Verified =%s ORDER BY doctordata.Doctor_ID ASC",[0])

    def VerifyDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[1, id])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been verified successfully")
        update()
        messagebox.showinfo("info","Doctor Verified")

    def BanDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[-1, id])
        InsertQuery("INSERT INTO suspended (User_ID, Suspention_Type, Suspention_Date, Reason) VALUES (%s, %s, %s, %s)",[id, "Permanent",date.today(),"Register With Fake ID and License",])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been suspended")
        update()
        messagebox.showinfo("info","Doctor Verified")

    def GetMail(self, id):
        return SelectQuery("SELECT Mail FROM users WHERE ID =%s",[id])[0][0]
    
    def SendMail(self, mail, Subject, msg):
        # Define email sender and receiver
        email_sender = 'livehealthy171@gmail.com'
        email_password = 'gowdfobqansntowb'
        email_receiver = mail

        # Set the subject and body of the email
        subject = Subject
        body = msg

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


a = Administrator(0)
print(a.GetMail(10))