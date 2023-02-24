import contextlib
import tkinter as tk
from datetime import date
import queue
import time
import os
import customtkinter as ctk
# from Model import *

from Images import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from UserFactory import *
from client import *
from tkinter.ttk import *
# importing askopenfile function
# from class filedialo


class App(ctk.CTk):
    # load Config dict
    config = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Patient
    user = UserFactory.createUser(0,"admin")

    Created = [
        True,
        True,
        True,
        True,
    ]  # Active chat frame, Patient Req frame, Credits Frame, amount Frame in credits PREVENTS duplications

    def __init__(self):
        super().__init__()
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
            self.config.get("FramesSizeWidth"),
            self.config.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

        # let the left sidebar take all the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        # load images
        Administrator_Image = ctk.CTkImage(
            AdministratorImage,
            size=(self.config.get("UserImageSize"),
                  self.config.get("UserImageSize")),
        )
        Handle_Reports_image = ctk.CTkImage(
            HandleReports,
            size=(
                self.config.get("ButtonIconsSize"),
                self.config.get("ButtonIconsSize"),
            ),
        )
        Verify_Doctors_image = ctk.CTkImage(
            VerifyDoctor,
            size=(
                self.config.get("ButtonIconsSize"),
                self.config.get("ButtonIconsSize"),
            ),
        )
        # create LeftSideBar frame
        self.LeftSideBar_frame = ctk.CTkFrame(self, corner_radius=0)
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
            text="Handle Reports",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
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
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=Verify_Doctors_image,
            anchor="w",
            # command=self.Credits_button_event,
        )
        self.Verify_Doctors_button.grid(row=3, column=0, sticky="ew")
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

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Handle_Reports_button.configure(
            fg_color=(
                "gray75", "gray25") if name == "Handle_Reports" else "transparent"
        )

        # show selected frame
        if name == "Handle_Reports":
            self.Handle_Reports_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Handle_Reports_frame.grid_forget()

    def LoadHandleReportsFrame(self):
        if self.Created[0]:
            self.Handle_Reports_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Handle_Reports_frame.winfo_children():
                widget.destroy()

        Title = ctk.CTkLabel(self.Handle_Reports_frame, text="Available Reports",
                             font=ctk.CTkFont(size=20, weight="bold"))
        Title.place(anchor="nw", relx=0.4, rely=0.02)

        LogsFrame = ctk.CTkScrollableFrame(
            self.Handle_Reports_frame, fg_color="gray40", width=1050,height=600)
        LogsFrame.place(anchor="nw", relx=0.01, rely=0.1)

        DoctorNameLabel = ctk.CTkLabel(LogsFrame, text="Doctor Name",
                                       font=ctk.CTkFont(size=17, weight="bold"), width=200)
        DoctorNameLabel.grid(row=0, column=0,pady=10)

        PatientNameLabel = ctk.CTkLabel(LogsFrame, text="Patient Name",
                                        font=ctk.CTkFont(size=17, weight="bold"), width=200)
        PatientNameLabel.grid(row=0, column=1)

        ReasonLabel = ctk.CTkLabel(LogsFrame, text="Reason",
                                   font=ctk.CTkFont(size=17, weight="bold"), width=200)
        ReasonLabel.grid(row=0, column=2)

        DateLabel = ctk.CTkLabel(LogsFrame, text="Date",
                                 font=ctk.CTkFont(size=17, weight="bold"), width=200)
        DateLabel.grid(row=0, column=3)

        ShowChatLabel = ctk.CTkLabel(LogsFrame, text="Chat",
                                     font=ctk.CTkFont(size=17, weight="bold"), width=200)
        ShowChatLabel.grid(row=0, column=4)

        # reports.Issuer_ID, reports.Reporter_ID, reports.Reason, reports.ReportDate, oldchat.ChatLOGS
        res = self.user.getAllReports()
        for pos, item in enumerate(res):
            # entryFrame = ctk.CTkFrame()
            patient = UserFactory.createUser(item[0],"patient")
            Doctor = UserFactory.createUser(item[1],"doctor")
            DName = ctk.CTkLabel(LogsFrame, text=f"Dr.{Doctor.userName}", wraplength=180,
                                 font=ctk.CTkFont(size=20, weight="bold"))
            DName.grid(row=pos+1, column=0,pady=10)

            PName = ctk.CTkLabel(LogsFrame, text=patient.userName, wraplength=180,
                                 font=ctk.CTkFont(size=20, weight="bold"))
            PName.grid(row=pos+1, column=1)

            Reas = ctk.CTkLabel(LogsFrame, text=item[2], wraplength=180,
                                font=ctk.CTkFont(size=20, weight="bold"))
            Reas.grid(row=pos+1, column=2)

            Repdate = ctk.CTkLabel(LogsFrame, text=item[3],
                                   font=ctk.CTkFont(size=20, weight="bold"))
            Repdate.grid(row=pos+1, column=3)

            Chat = ctk.CTkLabel(LogsFrame, text="Show Chat", image=ctk.CTkImage(Adminchat, size=(35, 35)), compound="left",
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
        ChatLogsFrame = ctk.CTkScrollableFrame(
            ChatWindow, fg_color="gray30", width=500,height=300)
        ChatLogsFrame.place(anchor="nw", relx=0.01, rely=0.01)
        Chatdata = chat.split("&,&")
        for pos, i in enumerate(Chatdata):
            chatitemLabel = ctk.CTkLabel(ChatLogsFrame, text=i, anchor='e',font=ctk.CTkFont(size=15, weight="bold"))
            chatitemLabel.grid(row=pos, column=0,sticky="W")
            
        RevokeButton = ctk.CTkButton(ChatWindow, text="Revoke Suspension",fg_color="#46c100", command= lambda:self.user.RevokeSuspension(ChatWindow, id, self.LoadHandleReportsFrame))
        RevokeButton.place(anchor="nw", relx=0.5, rely=0.85)

        PermaButton = ctk.CTkButton(ChatWindow, text="Permanent Suspension",fg_color="#ff0000", command= lambda:self.user.ConfirmSuspension(ChatWindow, id, self.LoadHandleReportsFrame))
        PermaButton.place(anchor="nw", relx=0.75, rely=0.85)


    def Handle_Reports_button_event(self):
        self.LoadHandleReportsFrame()
        self.select_frame_by_name("Handle_Reports")

    # def PatientRequests_button_event(self):
    #     # self.loadWaitingPatients()
    #     self.select_frame_by_name("PatientRequests")

    # def Credits_button_event(self):
    #     # self.loadCreditWithdraw()
    #     self.select_frame_by_name("Credits")

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.user.SetApperanceMode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
