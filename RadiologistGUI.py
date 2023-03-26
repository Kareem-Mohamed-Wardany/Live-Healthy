import contextlib
import tkinter as tk
from datetime import date
import queue
import time
import os
import customtkinter as ctk
from Model import *

from Images import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from User import *
from client import *
from tkinter.ttk import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from zipfile import ZipFile


class App(ctk.CTk):
    # load Config dict
    config = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Patient
    user = User("3")

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

        # let title be 'Welcome Specialist|Consultant UserName'
        Title = f"Welcome {self.user.userName}"
        self.title(Title)

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
        self.Male_image = ctk.CTkImage(
            MaleImage,
            size=(self.config.get("UserImageSize"),
                  self.config.get("UserImageSize")),
        )
        self.Female_image = ctk.CTkImage(
            FemaleImage,
            size=(self.config.get("UserImageSize"),
                  self.config.get("UserImageSize")),
        )
        self.Predict_scan_image = ctk.CTkImage(
            predict_image,
            size=(
                self.config.get("ButtonIconsSize"),
                self.config.get("ButtonIconsSize"),
            ),
        )
        self.chat_image = ctk.CTkImage(
            Chat,
            size=(
                self.config.get("ButtonIconsSize"),
                self.config.get("ButtonIconsSize"),
            ),
        )
        self.PurchaseVIP = ctk.CTkImage(
            PurchaseVIP,
            size=(
                self.config.get("ButtonIconsSize"),
                self.config.get("ButtonIconsSize"),
            ),
        )
        self.coin_image = ctk.CTkImage(
            coin,
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

        if (
            self.user.userGender == "Male"
        ):  # check if the user is a Male to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=self.Male_image,
                text="",
                width=100,
                height=50,
                compound="left",
                font=ctk.CTkFont(size=30, weight="bold"),
            )
        else:  # check if the user is a Female to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=self.Female_image,
                text="",
                width=100,
                height=50,
                compound="left",
                font=ctk.CTkFont(size=30, weight="bold"),
            )
        self.Image_label.grid(row=0, column=0, padx=20, pady=20)
        self.PatientName_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userName,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.PatientName_label.grid(row=1, column=0)

        self.PatientAge_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userAge,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.PatientAge_label.grid(row=2, column=0)

        self.VIP_level = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userVIPLevel,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.VIP_level.grid(row=3, column=0)

        self.VIP_end = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userVIPEnd,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.VIP_end.grid(row=4, column=0)

        self.Predict_Scan_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Predict X-Ray Scan",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.Predict_scan_image,
            anchor="w",
            command=self.Predict_Scan_button_event,
        )
        self.Predict_Scan_button.grid(row=5, column=0, sticky="ew")

        self.Credits_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=self.user.userBalance,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.coin_image,
            anchor="w",
            command=self.Credits_button_event,
        )
        self.Credits_button.grid(row=9, column=0, sticky="ew")
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

    def LoadPredictScanFrame(self):
        if self.Created[0]:
            self.Predict_Scan_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Predict_Scan_frame.winfo_children():
                widget.destroy()
        self.ScanPathEntry = ctk.CTkEntry(
            self.Predict_Scan_frame, width=700, state="disabled")
        self.ScanPathEntry.place(anchor="nw", relx=0.05, rely=0.05)
        ImportScanButton = ctk.CTkButton(
            self.Predict_Scan_frame, text="Import Folder", command=self.ImportScanFolder)
        ImportScanButton.place(anchor="nw", relx=0.7, rely=0.05)

    def ImportScanFolder(self):
        if self.ScanPathEntry.get() != "":
            self.ScanPathEntry.configure(state="normal")
            self.ScanPathEntry.delete(0, tk.END)
        self.ScansFolderPath = filedialog.askdirectory()
        print(self.ScansFolderPath)
        self.ScanPathEntry.configure(state="normal")
        self.ScanPathEntry.insert("end", self.ScansFolderPath)
        self.ScanPathEntry.configure(state="disabled")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Predict_Scan_button.configure(
            fg_color=(
                "gray75", "gray25") if name == "Predict_Scan" else "transparent"
        )

        # show selected frame
        if name == "Predict_Scan":
            self.Predict_Scan_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Predict_Scan_frame.grid_forget()

        # if name == "PatientRequests":
        #     self.PatientRequests_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     with contextlib.suppress(Exception):
        #         self.PatientRequests_frame.grid_forget()

        # if name == "Credits":
        #     self.credits_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     with contextlib.suppress(Exception):
        #         self.credits_frame.grid_forget()

    def Predict_Scan_button_event(self):
        self.LoadPredictScanFrame()
        self.select_frame_by_name("Predict_Scan")

    def PatientRequests_button_event(self):
        # self.loadWaitingPatients()
        self.select_frame_by_name("PatientRequests")

    def Credits_button_event(self):
        # self.loadCreditWithdraw()
        self.select_frame_by_name("Credits")

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.user.userSystemApperanceMode = new_appearance_mode
        self.db.Update(
            "UPDATE users SET Apperance_Mode = %s WHERE ID= %s",
            [new_appearance_mode, self.user.userid],
        )
        self.db.Commit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
