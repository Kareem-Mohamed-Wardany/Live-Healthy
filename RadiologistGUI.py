import contextlib
import os
import queue
import time
import tkinter as tk
from datetime import date
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from zipfile import ZipFile

import customtkinter as ctk

from client import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from Images import *
from User import *
from UserFactory import *



class RadioloGUI(ctk.CTk):
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
        self.user = UserFactory.createUser(id, "radiologist")
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
        self.configure(bg_color=self.configfile.get("BackgroundColor"))
        self.configure(fg_color=self.configfile.get("BackgroundColor"))
        # set Dimension of GUI
        center(
            self,
            self.configfile.get("FramesSizeWidth"),
            self.configfile.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

        # let the left sidebar take all the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        self.Predict_scan_image = ctk.CTkImage(
            predict_image,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        # create LeftSideBar frame
        self.LeftSideBar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.configfile.get("FrameColor"))
        self.LeftSideBar_frame.grid(row=0, column=0, sticky="nsew")
        # self.LeftSideBar_frame.grid_rowconfigure(3, weight=1)  # let row 6 with bigger weight to sperate between credit button, apperance mode and other button
        # let row 6 with bigger weight to sperate between credit button, apperance mode and other button
        self.LeftSideBar_frame.grid_rowconfigure(5, weight=1)

        if (
            self.user.userGender == "Male"
        ):  # check if the user is a Male to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=ctk.CTkImage(
                    MaleImage,
                    size=(self.configfile.get("UserImageSize"),
                          self.configfile.get("UserImageSize")),
                ),
                text="",
                width=100,
                height=50,
                compound="left",
                font=ctk.CTkFont(size=30, weight="bold"),
            )
        else:  # check if the user is a Female to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=ctk.CTkImage(
                    FemaleImage,
                    size=(self.configfile.get("UserImageSize"),
                          self.configfile.get("UserImageSize")),
                ),
                text="",
                width=100,
                height=50,
                compound="left",
                font=ctk.CTkFont(size=30, weight="bold"),
            )
        self.Image_label.grid(row=0, column=0, padx=20, pady=20)

        self.RadiologistName_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userName,
            width=100,
            height=20,
            compound="left",
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.RadiologistName_label.grid(row=1, column=0)

        self.RadiologyCenterName_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.CenterName,
            width=100,
            height=20,
            compound="left",
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.RadiologyCenterName_label.grid(row=2, column=0)

        self.Predict_Scan_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Predict X-Ray Scan",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.Predict_scan_image,
            anchor="w",
            command=self.Predict_Scan_button_event,
        )
        self.Predict_Scan_button.grid(row=4, column=0, sticky="ew")


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
        self.logoutbutton.grid(row=6, column=0, sticky="ew")

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
            row=7, column=0, padx=20, pady=20, sticky="s")
        

    def logout(self):
        self.destroy()
        from Runner import Runit

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
            self.Predict_Scan_frame, width=700, state="disabled", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"),border_color=self.configfile.get("TextColor"))
        self.ScanPathEntry.place(anchor="nw", relx=0.05, rely=0.05)
        ImportScanButton = ctk.CTkButton(
            self.Predict_Scan_frame, text="Import Folder", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"),hover_color=self.configfile.get("FrameColor"), command=self.ImportScanFolder)
        ImportScanButton.place(anchor="nw", relx=0.7, rely=0.05)

    def ImportScanFolder(self):
        if self.ScanPathEntry.get() != "":
            self.ScanPathEntry.configure(state="normal")
            self.ScanPathEntry.delete(0, tk.END)
        self.ScansFolderPath = filedialog.askdirectory()
        self.ScanPathEntry.configure(state="normal")
        self.ScanPathEntry.insert("end", self.ScansFolderPath)
        self.ScanPathEntry.configure(state="disabled")

        MessageBox(self.Predict_Scan_frame, "info", "Don't Panic!")
        output = self.user.PredictScanFolder(self.ScansFolderPath)

        ScrollableFrame = ctk.CTkScrollableFrame(
            self.Predict_Scan_frame, width=550,fg_color=self.configfile.get("FrameColor"),
            scrollbar_button_color=self.configfile.get("FrameColor"), 
            scrollbar_button_hover_color=self.configfile.get("TextColor"))
        ScrollableFrame.place(anchor="nw", relx=0.05, rely=0.2)

        Name = ctk.CTkLabel(ScrollableFrame, text="Image Name", text_color=self.configfile.get("TextColor"),
                            font=ctk.CTkFont(size=15), width=275)
        Name.grid(row=0, column=0)
        Name = ctk.CTkLabel(ScrollableFrame, text="Prediction",text_color=self.configfile.get("TextColor"),
                            font=ctk.CTkFont(size=15), width=275)
        Name.grid(row=0, column=1)

        for pos, i in enumerate(output):
            ImageName = ctk.CTkLabel(
                ScrollableFrame, text=i[0], font=ctk.CTkFont(size=15), width=275,text_color=self.configfile.get("TextColor"))
            ImageName.grid(row=pos+1, column=0)
            ImageName.bind("<Button-1>", lambda event,
                           imageName=i[0]: self.ShowImage(event, imageName))

            Prediction = ctk.CTkLabel(
                ScrollableFrame, text=i[1], font=ctk.CTkFont(size=15), width=275,text_color=self.configfile.get("TextColor"))
            Prediction.grid(row=pos+1, column=1)
            Prediction.bind("<Button-1>", lambda event,
                            imageName=i[0]: self.ShowImage(event, imageName))

        self.user.createcsv(self.ScansFolderPath, output)
        MessageBox(self.Predict_Scan_frame, "info",
                   "Predictions File Created successfully")

    def GetFullPath(self, Name):
        for i in os.listdir(self.ScansFolderPath):
            if Name in i:
                return os.path.join(self.ScansFolderPath, i)

    def ShowImage(self, event, Name):
        FullPath = self.GetFullPath(Name)

        image = ctk.CTkLabel(self.Predict_Scan_frame, text="", image=ctk.CTkImage(
            Image.open(FullPath), size=(300, 300)))
        image.place(anchor="nw", relx=0.7, rely=0.2)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Predict_Scan_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Predict_Scan" else "transparent"
        )

        # show selected frame
        if name == "Predict_Scan":
            self.Predict_Scan_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Predict_Scan_frame.grid_forget()

    def Predict_Scan_button_event(self):
        self.LoadPredictScanFrame()
        self.select_frame_by_name("Predict_Scan")

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.user.userSystemApperanceMode = new_appearance_mode
        self.db.Update(
            "UPDATE users SET Apperance_Mode = %s WHERE ID= %s",
            [new_appearance_mode, self.user.userid],
        )
        self.db.Commit()


if __name__ == "__main__":
    app = RadioloGUI(3)
    app.mainloop()
