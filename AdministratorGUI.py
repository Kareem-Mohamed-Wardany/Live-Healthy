import contextlib
import os
import queue
import shutil
import time
import tkinter as tk
from datetime import date
from tkinter.ttk import *

import customtkinter as ctk

from client import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from Images import *
from UserFactory import *

# from Model import *

# importing askopenfile function
# from class filedialo


class AdminGUI(ctk.CTk):
    # load Config dict
    configfile = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Patient
    

    Created = [
        True,
        True,
        True,
        True,
    ]  # Active chat frame, Patient Req frame, Credits Frame, amount Frame in credits PREVENTS duplications

    def __init__(self, id):
        super().__init__()
        self.user = UserFactory.createUser(id,"admin")
        self.configure(bg_color=self.configfile.get("BackgroundColor"))
        self.configure(fg_color=self.configfile.get("BackgroundColor"))
        self.WindowSettings()
        self.LeftSideBar()

    # Main Constructor

    def WindowSettings(self):
        # load Apperance model of the user
        ctk.set_appearance_mode(
            self.user.userSystemApperanceMode
        )  # Set Appearance mode of the user to what he has chosen

        self.title("Administrator Panel")

        # set Dimension of GUI
        center(
            self,
            self.configfile.get("FramesSizeWidth"),
            self.configfile.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.exit_function)

        # let the left sidebar take all the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        # load images
        Administrator_Image = ctk.CTkImage(
            AdministratorImage,
            size=(self.configfile.get("UserImageSize"),
                  self.configfile.get("UserImageSize")),
        )
        Handle_Reports_image = ctk.CTkImage(
            HandleReports,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        Verify_Doctors_image = ctk.CTkImage(
            VerifyDoctor,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        # create LeftSideBar frame
        self.LeftSideBar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.configfile.get("FrameColor"))
        self.LeftSideBar_frame.grid(row=0, column=0, sticky="nsew")
        self.LeftSideBar_frame.grid_rowconfigure(
            8, weight=1
        )  # let row 6 with bigger weight to sperate between credit button, apperance mode and other button

        Image_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            image=Administrator_Image,
            text="",
            width=100,
            height=50,
            compound="left",
            font=ctk.CTkFont(size=30, weight="bold"),)
        Image_label.grid(row=0, column=0, padx=20, pady=20)

        Administrator_Name_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userName,
            text_color=self.configfile.get("TextColor"),
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        Administrator_Name_label.grid(row=1, column=0)

        self.Handle_Reports_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            text="Handle Reports",
            fg_color="transparent",
            image=Handle_Reports_image,
            anchor="w",
            command=self.Handle_Reports_button_event,
        )
        self.Handle_Reports_button.grid(row=2, column=0, sticky="ew")

        self.Verify_Doctors_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Verify Doctors",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=Verify_Doctors_image,
            anchor="w",
            command=self.Verify_Doctors_button_event,
        )
        self.Verify_Doctors_button.grid(row=3, column=0, sticky="ew")

        self.logoutimg = ctk.CTkImage(
            logout,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        self.logoutbutton = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Logout",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.logoutimg,
            anchor="w",
            command=self.logout,
        )
        self.logoutbutton.grid(row=9, column=0, sticky="ew")
        # create Apperance Mode to what currently the GUI running with
        if self.user.userSystemApperanceMode == "Dark":
            v = ["Dark", "Light", "System"]
        elif self.user.userSystemApperanceMode == "Light":
            v = ["Light", "Dark", "System"]
        elif self.user.userSystemApperanceMode == "System":
            v = ["System", "Light", "Dark"]
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.LeftSideBar_frame, values=v, command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(
            row=10, column=0, padx=20, pady=20, sticky="s")
        
    def logout(self):
        self.destroy()
        from Runner import Runit

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Handle_Reports_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Handle_Reports" else "transparent"
        )
        self.Verify_Doctors_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Verify_Doctors" else "transparent"
        )

        # show selected frame
        if name == "Handle_Reports":
            self.Handle_Reports_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Handle_Reports_frame.grid_forget()

        if name == "Verify_Doctors":
            self.Verify_Doctors_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Verify_Doctors_frame.grid_forget()

    def LoadHandleReportsFrame(self):
        if self.Created[0]:
            self.Handle_Reports_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Handle_Reports_frame.winfo_children():
                widget.destroy()

        Title = ctk.CTkLabel(self.Handle_Reports_frame, text="Available Reports",font=ctk.CTkFont(size=20, weight="bold"), text_color=self.configfile.get("TextColor"))
        Title.place(anchor="nw", relx=0.4, rely=0.02)

        LogsFrame = ctk.CTkScrollableFrame(
            self.Handle_Reports_frame,width=1050,height=600,fg_color=self.configfile.get("FrameColor"),
            scrollbar_button_color=self.configfile.get("FrameColor"), 
            scrollbar_button_hover_color=self.configfile.get("TextColor"),)
        LogsFrame.place(anchor="nw", relx=0.01, rely=0.1)

        DoctorNameLabel = ctk.CTkLabel(LogsFrame, text="Doctor Name",text_color=self.configfile.get("TextColor"),
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        DoctorNameLabel.grid(row=0, column=0,pady=10)

        PatientNameLabel = ctk.CTkLabel(LogsFrame, text="Patient Name",text_color=self.configfile.get("TextColor"),
                                        font=ctk.CTkFont(size=17, weight="bold"), width=200)
        PatientNameLabel.grid(row=0, column=1)

        ReasonLabel = ctk.CTkLabel(LogsFrame, text="Reason",text_color=self.configfile.get("TextColor"),
                                   font=ctk.CTkFont(size=17, weight="bold"), width=200)
        ReasonLabel.grid(row=0, column=2)

        DateLabel = ctk.CTkLabel(LogsFrame, text="Date",text_color=self.configfile.get("TextColor"),
                                 font=ctk.CTkFont(size=17, weight="bold"), width=200)
        DateLabel.grid(row=0, column=3)

        ShowChatLabel = ctk.CTkLabel(LogsFrame, text="Chat",text_color=self.configfile.get("TextColor"),
                                     font=ctk.CTkFont(size=17, weight="bold"), width=200)
        ShowChatLabel.grid(row=0, column=4)

        # reports.Issuer_ID, reports.Reporter_ID, reports.Reason, reports.ReportDate, oldchat.ChatLOGS
        res = self.user.getAllReports()
        for pos, item in enumerate(res):
            # entryFrame = ctk.CTkFrame()
            patient = UserFactory.createUser(item[0],"patient")
            Doctor = UserFactory.createUser(item[1],"doctor")
            DName = ctk.CTkLabel(LogsFrame, text=f"Dr.{Doctor.userName}", wraplength=180, text_color=self.configfile.get("TextColor"),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            DName.grid(row=pos+1, column=0,pady=10)

            PName = ctk.CTkLabel(LogsFrame, text=patient.userName, wraplength=180, text_color=self.configfile.get("TextColor"),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            PName.grid(row=pos+1, column=1)

            Reas = ctk.CTkLabel(LogsFrame, text=item[2], wraplength=180, text_color=self.configfile.get("TextColor"),
                                font=ctk.CTkFont(size=20, weight="bold"))
            Reas.grid(row=pos+1, column=2)

            Repdate = ctk.CTkLabel(LogsFrame, text=item[3], text_color=self.configfile.get("TextColor"),
                                   font=ctk.CTkFont(size=20, weight="bold"))
            Repdate.grid(row=pos+1, column=3)

            Chat = ctk.CTkLabel(LogsFrame, text="Show Chat", image=ctk.CTkImage(Adminchat, size=(35, 35)), compound="left", text_color=self.configfile.get("TextColor"),
                                font=ctk.CTkFont(size=14, weight="bold"))
            Chat.grid(row=pos+1, column=4)
            Chat.bind("<Button-1>",lambda event, id = item[0], PN =patient.userName, DN = Doctor.userName, Chatt = item[4] : self.showChat(event, id, PN, DN, Chatt ))

    def showChat(self, event, id, PName, DName, chat):
        ChatWindow = ctk.CTkToplevel()
        title = f"Chat Between Dr.{DName} and {PName}"
        ChatWindow.title(title)
        center(ChatWindow, 600, 400)  # Open the window in the center of the Screen
        ChatWindow.attributes('-topmost', 'true',)
        ChatWindow.resizable(False, False)
        ChatWindow.configure(bg_color=self.configfile.get("BackgroundColor"))
        ChatWindow.configure(fg_color=self.configfile.get("BackgroundColor"))
        ChatLogsFrame = ctk.CTkScrollableFrame(
            ChatWindow, width=500,height=300,fg_color=self.configfile.get("FrameColor"),
            scrollbar_button_color=self.configfile.get("FrameColor"), 
            scrollbar_button_hover_color=self.configfile.get("TextColor"),)
        ChatLogsFrame.place(anchor="nw", relx=0.01, rely=0.01)
        Chatdata = chat.split("&,&")
        for pos, i in enumerate(Chatdata):
            chatitemLabel = ctk.CTkLabel(ChatLogsFrame, text=i, anchor='e',font=ctk.CTkFont(size=15, weight="bold"))
            chatitemLabel.grid(row=pos, column=0,sticky="W")
            
        RevokeButton = ctk.CTkButton(ChatWindow, text="Revoke Suspension", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"), command= lambda:self.user.RevokeSuspension(ChatWindow, id, self.LoadHandleReportsFrame))
        RevokeButton.place(anchor="nw", relx=0.5, rely=0.85)

        PermaButton = ctk.CTkButton(ChatWindow, text="Permanent Suspension", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"), command= lambda:self.user.ConfirmSuspension(ChatWindow, id, self.LoadHandleReportsFrame))
        PermaButton.place(anchor="nw", relx=0.75, rely=0.85)

    def Handle_Reports_button_event(self):
        self.LoadHandleReportsFrame()
        self.select_frame_by_name("Handle_Reports")

    def Verify_Doctors_button_event(self):
        self.LoadVerifyDoctorsFrame()
        self.select_frame_by_name("Verify_Doctors")

    def LoadVerifyDoctorsFrame(self):
        if self.Created[1]:
            self.Verify_Doctors_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[1] = False
        with contextlib.suppress(Exception):
            os.mkdir("Data/images/") 
            for widget in self.Verify_Doctors_frame.winfo_children():
                widget.destroy()

        Title = ctk.CTkLabel(self.Verify_Doctors_frame, text="Unverified Doctors", text_color=self.configfile.get("TextColor"),
                             font=ctk.CTkFont(size=20, weight="bold"))
        Title.place(anchor="nw", relx=0.4, rely=0.02)

        Doctors_frame = ctk.CTkScrollableFrame(self.Verify_Doctors_frame, fg_color=self.configfile.get("FrameColor"), width=1050,height=600,
            scrollbar_button_color=self.configfile.get("FrameColor"), 
            scrollbar_button_hover_color=self.configfile.get("TextColor"),)
        Doctors_frame.place(anchor="nw", relx=0.01, rely=0.1)

        DoctorNameLabel = ctk.CTkLabel(Doctors_frame, text="Doctor Name",text_color=self.configfile.get("TextColor"),
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        DoctorNameLabel.grid(row=0, column=0,pady=10)

        UniversityLabel = ctk.CTkLabel(Doctors_frame, text="University Name",text_color=self.configfile.get("TextColor"),
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        UniversityLabel.grid(row=0, column=1,pady=10)

        IDCardLabel = ctk.CTkLabel(Doctors_frame, text="ID Card",text_color=self.configfile.get("TextColor"),
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        IDCardLabel.grid(row=0, column=2,pady=10)

        ProfLicLabel = ctk.CTkLabel(Doctors_frame, text="Profession License",text_color=self.configfile.get("TextColor"),
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        ProfLicLabel.grid(row=0, column=3,pady=10)
        res = self.user.getUnverifiedDoctors()
        for pos, i in enumerate(res):
            # doctordata.Doctor_ID, users.Name, doctordata.University, doctordata.ID_Card, doctordata.Prof_License
            DName = ctk.CTkLabel(Doctors_frame, text=f"Dr. {i[1]}", wraplength=180, text_color=self.configfile.get("TextColor"),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            DName.grid(row=pos+1, column=0,pady=10)

            UniversityName = ctk.CTkLabel(Doctors_frame, text=f"{i[2]}", wraplength=180,text_color=self.configfile.get("TextColor"),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            UniversityName.grid(row=pos+1, column=1,pady=10)


            write_file(i[3],f"Data/images/ID_Card_{i[1]}.png")
            img = Image.open(f"Data/images/ID_Card_{i[1]}.png")

            IDCard = ctk.CTkLabel(Doctors_frame, text="", wraplength=180,image= ctk.CTkImage(img,size=(150,50)),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            IDCard.grid(row=pos+1, column=2,pady=10)
            IDCard.bind("<Button-1>", lambda event, name = i[1], im = img, type="ID Card": self.Zoom(event, name, im, type))



            write_file(i[4],f"Data/images/Prof_lic_{i[1]}.png")
            img2 = Image.open(f"Data/images/Prof_lic_{i[1]}.png")

            Prof_lic = ctk.CTkLabel(Doctors_frame, text="", wraplength=180,image= ctk.CTkImage(img2,size=(150,50)),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            Prof_lic.grid(row=pos+1, column=3,pady=10)
            Prof_lic.bind("<Button-1>", lambda event, name = i[1], im = img2, type="Profession License": self.Zoom(event, name, im, type))


            verfiy = ctk.CTkLabel(Doctors_frame, text="", width=100,image= ctk.CTkImage(Verify,size=(50,50)),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            verfiy.grid(row=pos+1, column=4,pady=10)
            # master, id, update
            verfiy.bind("<Button-1>", lambda event, id = i[0]: self.user.VerifyDoctor(event, self.Verify_Doctors_frame, id, self.LoadVerifyDoctorsFrame))

            ban = ctk.CTkLabel(Doctors_frame, text="", width=100,image= ctk.CTkImage(Ban,size=(50,50)),
                                 font=ctk.CTkFont(size=20, weight="bold"))
            ban.grid(row=pos+1, column=5,pady=10)
            ban.bind("<Button-1>", lambda event, id = i[0]: self.user.BanDoctor(event, self.Verify_Doctors_frame, id, self.LoadVerifyDoctorsFrame))

    def Zoom(self, event, name, img, type):
        ZoomWindow = ctk.CTkToplevel()
        title = f"{type} For {name}"
        ZoomWindow.title(title)
        center(ZoomWindow, 600, 400)  # Open the window in the center of the Screen
        ZoomWindow.attributes('-topmost', 'true',)
        ZoomWindow.resizable(False, False)
        imgLabel = ctk.CTkLabel(ZoomWindow, text="",image=ctk.CTkImage(img,size=(600,400)))
        imgLabel.grid(row=0,column=0)

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.user.SetApperanceMode(new_appearance_mode)

    def exit_function(self):
        try:
            shutil.rmtree("Data/images/")
        except OSError as e:
            pass
        self.destroy()

if __name__ == "__main__":
    app = AdminGUI(0)
    app.mainloop()
