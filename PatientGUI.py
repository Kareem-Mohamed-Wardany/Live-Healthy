import contextlib
import tkinter as tk
from datetime import date, timedelta
import queue
import time
import subprocess
import os
import customtkinter as ctk
# from Model import *

from Images import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from User import *
from client import *
from tkinter.ttk import *
from tkinter import filedialog


class App(ctk.CTk):
    # load Config dict
    configDict = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Patient
    user = User("5")  

    Created = [
        True,
        True,
        True,
        True,
        True,
    ]  # Predict X-ray frame, Chat With doctor frame, vipPurchase Frame, Prescriptions Frame , credits PREVENTS duplications

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
            self.configDict.get("FramesSizeWidth"),
            self.configDict.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)  # let the left sidebar take all the space
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        # load images
        self.Male_image = ctk.CTkImage(
            MaleImage,
            size=(self.configDict.get("UserImageSize"), self.configDict.get("UserImageSize")),
        )
        self.Female_image = ctk.CTkImage(
            FemaleImage,
            size=(self.configDict.get("UserImageSize"), self.configDict.get("UserImageSize")),
        )
        self.Predict_scan_image = ctk.CTkImage(
            predict_image,
            size=(
                self.configDict.get("ButtonIconsSize"),
                self.configDict.get("ButtonIconsSize"),
            ),
        )
        self.chat_image = ctk.CTkImage(
            Chat,
            size=(
                self.configDict.get("ButtonIconsSize"),
                self.configDict.get("ButtonIconsSize"),
            ),
        )
        self.PurchaseVIP = ctk.CTkImage(
            PurchaseVIP,
            size=(
                self.configDict.get("ButtonIconsSize"),
                self.configDict.get("ButtonIconsSize"),
            ),
        )
        self.PrescriptionsIcon = ctk.CTkImage(
            Prescriptions,
            size=(
                self.configDict.get("ButtonIconsSize"),
                self.configDict.get("ButtonIconsSize"),
            ),
        )
        self.coin_image = ctk.CTkImage(
            coin,
            size=(
                self.configDict.get("ButtonIconsSize"),
                self.configDict.get("ButtonIconsSize"),
            ),
        )

        # create LeftSideBar frame
        self.LeftSideBar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.LeftSideBar_frame.grid(row=0, column=0, sticky="nsew")
        self.LeftSideBar_frame.grid_rowconfigure(
            9, weight=1
        )  # let row 9 with bigger weight to sperate between credit button, apperance mode and other button

        if (
            self.user.userGender == "Male"
        ):  # check if the user is a Male to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=self.Male_image,
                text="",
                width=100,
                # height=50,
                compound="left",
            )
        else:  # check if the user is a Female to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=self.Female_image,
                text="",
                width=100,
                # height=50,
                compound="left",
            )
        self.Image_label.grid(row=0, column=0)
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
        
        if self.user.userVIPLevel == 1:
            self.VIP_level = ctk.CTkLabel(
                self.LeftSideBar_frame,
                text="",
                image=ctk.CTkImage(bronze,size=(35,35)),
                width=100,
                height=20,
                compound="left",
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            self.VIP_level.grid(row=3, column=0)

        if self.user.userVIPLevel == 2:
            self.VIP_level = ctk.CTkLabel(
                self.LeftSideBar_frame,
                text="",
                image=ctk.CTkImage(silver,size=(35,35)),
                width=100,
                height=20,
                compound="left",
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            self.VIP_level.grid(row=3, column=0)

    
        if self.user.userVIPLevel == 3:
            self.VIP_level = ctk.CTkLabel(
                self.LeftSideBar_frame,
                text="",
                image=ctk.CTkImage(gold,size=(35,35)),
                width=100,
                height=20,
                compound="left",
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            self.VIP_level.grid(row=3, column=0)

        if self.user.userVIPLevel != 0:
            self.VIP_end = ctk.CTkLabel(
                self.LeftSideBar_frame,
                text=self.user.userVIPEnd,
                image = ctk.CTkImage(EndDate,size=(35,35)),
                width=100,
                height=40,
                # bottom, center, left, none, right, or top
                compound="top",
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

        self.ChatWithDoctor_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Chat with our Doctor",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.ChatWithDoctor_button_event,
        )
        self.ChatWithDoctor_button.grid(row=6, column=0, sticky="ew")
        
        self.PurchaseVIP_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Purchase VIP",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.PurchaseVIP,
            anchor="w",
            command=self.PurchaseVIP_button_event,
        )
        self.PurchaseVIP_button.grid(row=7, column=0, sticky="ew")

        self.Prescriptions_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="All My Prescriptions",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.PrescriptionsIcon,
            anchor="w",
            command=self.Prescriptions_button_event,
        )
        self.Prescriptions_button.grid(row=8, column=0, sticky="ew")

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
        self.Credits_button.grid(row=10, column=0, sticky="ew")
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
        self.appearance_mode_menu.grid(row=11, column=0, padx=20, pady=20, sticky="s")

    def LoadPredictScanFrame(self):
        if self.Created[0]:
            self.Predict_Scan_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Predict_Scan_frame.winfo_children():
                widget.destroy()
        Infotext = self.ChatCreditsInfo("")
        MessageBox(self.Predict_Scan_frame,"info",Infotext)
        self.ScanPathEntry = ctk.CTkEntry(self.Predict_Scan_frame, width=700, state="disabled")
        self.ScanPathEntry.place(anchor="nw", relx=0.05, rely=0.05)
        self.ScanPathEntry2 = ctk.CTkEntry(self.Predict_Scan_frame, width=400, state="disabled")
        self.ScanPathEntry2.place(anchor="nw", relx=0.05, rely=0.15)
        self.ScanPathEntry3 = ctk.CTkEntry(self.Predict_Scan_frame, width=400, state="disabled")
        self.ScanPathEntry3.place(anchor="nw", relx=0.05, rely=0.25)
        ImportScanButton = ctk.CTkButton(self.Predict_Scan_frame,text="Import Scan", command=self.ImportScan)
        ImportScanButton.place(anchor="nw", relx=0.7, rely=0.05)
        ImportScanButton2 = ctk.CTkButton(self.Predict_Scan_frame,text="Save Prediction", command=self.SavePrediction)
        ImportScanButton2.place(anchor="nw", relx=0.05, rely=0.35)
        
    def ImportScan(self):
        if self.ScanPathEntry.get() != "":
            self.ScanPathEntry.configure(state="normal")
            self.ScanPathEntry.delete(0, tk.END)
        self.ScanPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        self.ScanPathEntry.configure(state="normal")
        self.ScanPathEntry.insert("end", self.ScanPath) 
        self.ScanPathEntry.configure(state="disabled")
        ScanImage = ctk.CTkLabel(self.Predict_Scan_frame,text="",image=ctk.CTkImage(Image.open(self.ScanPath),size=(300,300)))
        ScanImage.place(anchor="nw", relx=0.7, rely=0.2)
        if self.user.userVIPLevel < 3:
            if self.user.userVIPLevel == 1:
                value = -50
            elif self.user.userVIPLevel == 2:
                value = -25
            elif self.user.userVIPLevel == 0:
                value = -75
            res = self.user.updateBalance(self.Predict_Scan_frame, value)
            if res != -1:
                self.Predict()
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
                self.Credits_button.grid(row=10, column=0, sticky="ew")
        else:
            self.Predict()

    def Predict(self):
        m = ResNetModel()
        prediction = m.PredictScan(self.ScanPath)
        self.max1 = 0
        self.max2 = 0
        self.p1=""
        self.p2=""
        for i in prediction:
            value = float(i[1].split("%")[0])
            if value > self.max1 or value > self.max2:
                if self.max1 < self.max2:
                    self.max1 = value
                    self.p1 = i[0]
                else:
                    self.max2 = value
                    self.p2 = i[0]
        Label1 = f"{self.p1} ➜ {self.max1}%"
        Label2 = f"{self.p2} ➜ {self.max2}%"
        if self.ScanPathEntry2.get() != "" or self.ScanPathEntry3.get() !="":
            self.ScanPathEntry2.configure(state="normal")
            self.ScanPathEntry2.delete(0, tk.END)
            self.ScanPathEntry3.configure(state="normal")
            self.ScanPathEntry3.delete(0, tk.END)
        self.pr1 = f"Highest Class Percentage: {Label1}"
        self.pr2 = f"Second Class Percentage: {Label2}"
        self.ScanPathEntry2.configure(state="normal")
        self.ScanPathEntry2.insert("end", self.pr1) 
        self.ScanPathEntry3.configure(state="normal")
        self.ScanPathEntry3.insert("end", self.pr2)
        
    def SavePrediction(self):
        newpath = self.ScanPath.split(".")[0]
        newpath = f"{newpath}.txt"
        with open(newpath, "w") as f:
            f.write(f"Highest Class Percentage: {self.p1} --> {self.max1}% \n")
            f.write(f"Second Class Percentage: {self.p2} --> {self.max2}%")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Predict_Scan_button.configure(
            fg_color=("gray75", "gray25") if name == "Predict_Scan" else "transparent"
        )
        self.ChatWithDoctor_button.configure(
            fg_color=("gray75", "gray25")
            if name == "ChatWithDoctor"
            else "transparent"
        )

        self.PurchaseVIP_button.configure(
            fg_color=("gray75", "gray25")
            if name == "PurchaseVIP"
            else "transparent"
        )

        self.Prescriptions_button.configure(
            fg_color=("gray75", "gray25")
            if name == "All My Prescriptions"
            else "transparent"
        )
        # self.Credits_button.configure(
        #     fg_color=("gray75", "gray25") if name == "Credits" else "transparent"
        # )

        # show selected frame
        if name == "Predict_Scan":
            self.Predict_Scan_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Predict_Scan_frame.grid_forget()

        if name == "ChatWithDoctor":
            self.ChatWithDoctor_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.ChatWithDoctor_frame.grid_forget()

        if name == "PurchaseVIP":
            self.PurchaseVIP_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.PurchaseVIP_frame.grid_forget()

        if name == "All My Prescriptions":
            self.Prescriptions_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Prescriptions_frame.grid_forget()



        # if name == "Credits":
        #     self.credits_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     with contextlib.suppress(Exception):
        #         self.credits_frame.grid_forget()

    def Predict_Scan_button_event(self):
        self.LoadPredictScanFrame()
        self.select_frame_by_name("Predict_Scan")

    def ChatWithDoctor_button_event(self):
        self.ChatWithDoctor()
        self.select_frame_by_name("ChatWithDoctor")

    def PurchaseVIP_button_event(self):
        self.Purchase_VIP()
        self.select_frame_by_name("PurchaseVIP")

    def Purchase_VIP(self):
        if self.Created[2]:
            self.PurchaseVIP_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent", height= self.winfo_height(), width= self.winfo_width()
            )
            self.Created[2] = False
        with contextlib.suppress(Exception):
            for widget in self.PurchaseVIP_frame.winfo_children():
                widget.destroy()
        VipImage = ctk.CTkLabel(self.PurchaseVIP_frame, text="", image=ctk.CTkImage(PurchaseVIPLogo,size=(350,150)))
        VipImage.place(anchor="nw", relx=0.3, rely=0.01)
        self.AddBronzelevel(self.PurchaseVIP_frame)
        self.AddSilverlevel(self.PurchaseVIP_frame)
        self.AddGoldlevel(self.PurchaseVIP_frame)

    def AddBronzelevel(self, frame):
        Bronzeframe = ctk.CTkFrame(frame, corner_radius=15, fg_color="#CD7F32",height= 500, width=250)
        Bronzeframe.place(anchor="nw", relx=0.06, rely=0.28)

        LogoLabel = ctk.CTkLabel(Bronzeframe, text="Monthly Bronze Plan",image=ctk.CTkImage(bronze,size=(50,50)),compound="top", text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        LogoLabel.place(anchor="nw", relx=0.2, rely=0.02)

        Discount15Logo = ctk.CTkLabel(Bronzeframe, text="", image=ctk.CTkImage(FifteenPercent,size=(100,100)))
        Discount15Logo.place(anchor="nw", relx=0.3, rely=0.23)

        DiscountLogo = ctk.CTkLabel(Bronzeframe, text="", image=ctk.CTkImage(Discount,size=(75,75)))
        DiscountLogo.place(anchor="nw", relx=0.35, rely=0.47)

        Coinlogo = ctk.CTkLabel(Bronzeframe, text="100", image=ctk.CTkImage(coin,size=(75,75)), compound="left",text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        Coinlogo.place(anchor="nw", relx=0.25, rely=0.65)


        subscribeButton = ctk.CTkButton(Bronzeframe,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.Subscribe("bronze"))
        subscribeButton.place(anchor="nw", relx=0.225, rely=0.82)

    def AddSilverlevel(self, frame):
        silverFrame = ctk.CTkFrame(frame, corner_radius=15, fg_color="#C0C0C0",height= 500, width=250)
        silverFrame.place(anchor="nw", relx=0.36, rely=0.28)

        LogoLabel = ctk.CTkLabel(silverFrame, text="Monthly Silver Plan",image=ctk.CTkImage(silver,size=(50,50)),compound="top", text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        LogoLabel.place(anchor="nw", relx=0.225, rely=0.02)

        Discount15Logo = ctk.CTkLabel(silverFrame, text="", image=ctk.CTkImage(FiftyPercent,size=(100,100)))
        Discount15Logo.place(anchor="nw", relx=0.3, rely=0.23)

        DiscountLogo = ctk.CTkLabel(silverFrame, text="", image=ctk.CTkImage(Discount,size=(75,75)))
        DiscountLogo.place(anchor="nw", relx=0.35, rely=0.47)

        Coinlogo = ctk.CTkLabel(silverFrame, text="190", image=ctk.CTkImage(coin,size=(75,75)), compound="left",text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        Coinlogo.place(anchor="nw", relx=0.25, rely=0.65)


        subscribeButton = ctk.CTkButton(silverFrame,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.Subscribe("silver"))
        subscribeButton.place(anchor="nw", relx=0.225, rely=0.82)

    def AddGoldlevel(self, frame):
        Goldframe = ctk.CTkFrame(frame, corner_radius=15, fg_color="#cfb53b",height= 500, width=250)
        Goldframe.place(anchor="nw", relx=0.66, rely=0.28)

        LogoLabel = ctk.CTkLabel(Goldframe, text="Monthly Gold Plan",image=ctk.CTkImage(gold,size=(50,50)),compound="top", text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        LogoLabel.place(anchor="nw", relx=0.25, rely=0.02)

        Discount15Logo = ctk.CTkLabel(Goldframe, text="", image=ctk.CTkImage(HundredPercent,size=(100,100)))
        Discount15Logo.place(anchor="nw", relx=0.3, rely=0.23)

        DiscountLogo = ctk.CTkLabel(Goldframe, text="", image=ctk.CTkImage(Discount,size=(75,75)))
        DiscountLogo.place(anchor="nw", relx=0.35, rely=0.47)

        Coinlogo = ctk.CTkLabel(Goldframe, text="350", image=ctk.CTkImage(coin,size=(75,75)), compound="left",text_color="#fafad2", font=ctk.CTkFont(size=14, weight="bold"))
        Coinlogo.place(anchor="nw", relx=0.25, rely=0.65)


        subscribeButton = ctk.CTkButton(Goldframe,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.Subscribe("gold"))
        subscribeButton.place(anchor="nw", relx=0.225, rely=0.82)   

    def Subscribe(self, button):
        if button == "bronze":
            level = 1
            value = -100
        elif button == "silver":
            level = 2
            value = -190
        elif button == "gold":  
            level = 3
            value = -350
        res = self.user.updateBalance(self.PurchaseVIP_frame, value)
        if res != -1:
            if self.user.userVIPEnd == date(2001,1,1) or self.user.userVIPEnd < date.today():
                self.user.userVIPEnd = date.today() + timedelta(days=30)
            else:
                self.user.userVIPEnd += timedelta(days=30)
            self.user.userVIPLevel = level
            self.db.Update("UPDATE users SET Vip_Level= %s, Vip_End_Date= %s WHERE ID = %s",[self.user.userVIPLevel, self.user.userVIPEnd, self.user.userid])
            self.db.Commit()
            self.LeftSideBar()
            MessageBox(self.PurchaseVIP_frame,"info","Purchase Complete")

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

    def ChatWithDoctor(self):  # Fix the box colors, turn them all Textbox instead of Entry
        if self.Created[1]:
            self.ChatWithDoctor_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent", height= self.winfo_height(), width= self.winfo_width()
            )
            self.Created[1] = False
        with contextlib.suppress(Exception):
            for widget in self.ChatWithDoctor_frame.winfo_children():
                widget.destroy()

        if not self.user.checkRequest(): # Check if the Patient already has a request
            res = self.db.Select("SELECT Request_Status FROM requests WHERE Patient_ID= %s", [self.user.userid])[0][0]
            if res == "waiting":
                return MessageBox(self.ChatWithDoctor_frame,"info", "Waiting for a doctor to respond")
            self.DoctorID = self.db.Select("SELECT Doc_ID FROM chatdata WHERE Patient_ID= %s", [self.user.userid])[0][0]
            self.openChat()

        else:
            Infotext = self.ChatCreditsInfo("Chat")
            MessageBox(self.ChatWithDoctor_frame,"info",Infotext)

            self.ScanPathTextbox = ctk.CTkTextbox(self.ChatWithDoctor_frame, width=700, state = "disabled", height=10)
            self.ScanPathTextbox.place(anchor="nw", relx=0.05, rely=0.05)

            ImportScanButton = ctk.CTkButton(self.ChatWithDoctor_frame,text="Import Scan", command=self.ImportScan2)
            ImportScanButton.place(anchor="nw", relx=0.7, rely=0.05)

            Sym = ctk.CTkLabel(self.ChatWithDoctor_frame,text="Symptoms*",font= ctk.CTkFont(size=16))
            Sym.place(anchor="nw", relx=0.05, rely=0.10)

            self.symptoms = ctk.CTkTextbox(self.ChatWithDoctor_frame, width=600, height=140)
            self.symptoms.place(anchor="nw", relx=0.05, rely=0.15)

            sw = ctk.CTkLabel(self.ChatWithDoctor_frame,text="Since when have you been suffering these symptoms?*",font= ctk.CTkFont(size=16))
            sw.place(anchor="nw", relx=0.05, rely=0.35)

            self.illnessTime = ctk.CTkTextbox(self.ChatWithDoctor_frame, width=100,  height=10)
            self.illnessTime.place(anchor="nw", relx=0.05, rely=0.40)

            med = ctk.CTkLabel(self.ChatWithDoctor_frame,text="Current medications*",font= ctk.CTkFont(size=16))
            med.place(anchor="nw", relx=0.05, rely=0.45)

            self.medications = ctk.CTkTextbox(self.ChatWithDoctor_frame, width=600, height=120)
            self.medications.place(anchor="nw", relx=0.05, rely=0.50)

            extra = ctk.CTkLabel(self.ChatWithDoctor_frame,text="Extra information",font= ctk.CTkFont(size=16))
            extra.place(anchor="nw", relx=0.05, rely=0.67)

            self.extraInfo = ctk.CTkTextbox(self.ChatWithDoctor_frame, width=600, height=120)
            self.extraInfo.place(anchor="nw", relx=0.05, rely=0.72)

            FillRequestButton = ctk.CTkButton(self.ChatWithDoctor_frame,text="Fill Request",width=15, command=self.FillRequest)
            FillRequestButton.place(anchor="nw", relx=0.72, rely=0.85)

    def ImportScan2(self): 
        if self.ScanPathTextbox.get("end") != "":
            self.ScanPathTextbox.configure(state="normal")
            self.ScanPathTextbox.delete(0, tk.END)
        self.ScanPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        self.ScanPathTextbox.configure(state="normal")
        self.ScanPathTextbox.insert("end", self.ScanPath) 
        self.ScanPathTextbox.configure(state="disabled")
        m = ResNetModel()
        prediction = m.PredictScan(self.ScanPath)
        max = 0
        for i in prediction:
            value = float(i[1].split("%")[0])
            if value > max:
                max = value
                self.prediction= i[0]

    def FillRequest(self):
        if self.symptoms.get("1.0", "end-1c") == "":
            return MessageBox(self.ChatWithDoctor_frame, "error","Symptoms can not be empty")

        if self.illnessTime.get("1.0", "end-1c") == "":
            return MessageBox(self.ChatWithDoctor_frame, "error","Illness Time can not be empty")

        if self.medications.get("1.0", "end-1c") == "":
            return MessageBox(self.ChatWithDoctor_frame, "error","Medications can not be empty")

        symptoms = self.symptoms.get("1.0", "end-1c")

        illnessTime = self.illnessTime.get("1.0", "end-1c")

        medications = self.medications.get("1.0", "end-1c")

        if self.extraInfo.get("1.0", "end-1c") == "":
            extraInfo = "-"
        else:
            extraInfo = self.extraInfo.get("1.0", "end-1c")

        if self.user.userVIPLevel < 3:
            if self.user.userVIPLevel == 1:
                value = -100
            elif self.user.userVIPLevel == 2:
                value = -50
            elif self.user.userVIPLevel == 0:
                value = -150
            res = self.user.updateBalance(self.ChatWithDoctor_frame, value)
            if res != -1:
                self.user.addRequest(self.ScanPath, self.prediction, symptoms, illnessTime, medications, extraInfo)
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
                self.Credits_button.grid(row=10, column=0, sticky="ew")
                
        else:
            self.user.addRequest(self.ScanPath, self.prediction, symptoms, illnessTime, medications, extraInfo)
        self.ChatWithDoctor()
        return MessageBox(self.ChatWithDoctor_frame, "info","Successfully added")

    def ChatCreditsInfo(self, ContextType):
        if ContextType =="Chat":
            if self.user.userVIPLevel == 1:
                Infotext = "You are going to pay 100 credit to chat with our doctors"
            elif self.user.userVIPLevel == 2:
                Infotext = "You are going to pay 50 credit to chat with our doctors"
            elif self.user.userVIPLevel == 3:
                Infotext = "Chat with our doctors is Free"
            else:
                Infotext = "You are going to pay 150 credit to chat with our doctors"
        else:
            if self.user.userVIPLevel == 1:
                Infotext = "You are going to pay 50 credit to predict your X-ray Scan"
            elif self.user.userVIPLevel == 2:
                Infotext = "You are going to pay 25 credit to predict your X-ray Scan"
            elif self.user.userVIPLevel == 3:
                Infotext = "X-ray Scan prediction is Free"
            else:
                Infotext = "You are going to pay 75 credit to predict your X-ray Scan"
        return Infotext

    # Chat Section
    def openChat(self):
    # Chat window that will contain ChatFrame that show the chat for the doctor and chatbox where the doctor type in his chat
    # also send icon that will show the text in chatbox on ChatFrame for both patient and doctor
        with contextlib.suppress(Exception):
            for widget in chatWindow.winfo_children():
                widget.destroy()
            self.Userclient.end()
        start_time = time.time()
        chatWindow = ctk.CTkFrame(
            self.ChatWithDoctor_frame, corner_radius=0, width=1000, fg_color="transparent", height=720
        )
        chatWindow.place(anchor="nw",relx = 0.01,rely = 0.01)

        self.ChatFrame = ScrollableFrame(
            chatWindow, "gray40", width=700, height=500, scrollafter=8
        )
        self.ChatFrame.place(anchor="nw", relx=0.01, rely=0)
        # Doctor Data
        self.DoctorData(chatWindow)

        # Prescription
        self.GeneratePrescription(chatWindow)

        # ChatBox
        self.ChatBoxBlock(chatWindow)

        print(f"--- {time.time() - start_time} seconds ---")

        # join Chat Servrt
        # self.JoinChatServer()

    def DoctorData(self, master):
        DoctorData = User(self.DoctorID)  # Get the patient Data

        if DoctorData.userGender == "Male":
            Imagesrc = ctk.CTkImage(MaleImage, size=(200, 200))
        else:
            Imagesrc = ctk.CTkImage(FemaleImage, size=(200, 200))

        Patientinfo = ctk.CTkFrame(master)
        Patientinfo.place(anchor="nw", relx=0.8, rely=0.005)

        PImage = ctk.CTkLabel(Patientinfo, height=40, text="", image=Imagesrc)
        PImage.grid(row=0, column=0)
        PName = ctk.CTkLabel(
            Patientinfo,
            height=10,
            text=DoctorData.userName,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        PName.grid(row=1, column=0)

        PAge = ctk.CTkLabel(
            Patientinfo,
            height=10,
            text=DoctorData.userType,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PAge.grid(row=2, column=0)

    def GeneratePrescription(self, master):
        # Generate Prescription for a Patient
        GenerateReport = ctk.CTkLabel(
            master,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(GeneratePrescription, size=(40, 40)),
        )
        GenerateReport.place(anchor="nw", relx=0.83, rely=0.92)
        GenerateReport.bind(
            "<Button-1>", lambda event: self.HandlePrescription(event)
        )

    def HandlePrescription(self, event):
        path = f"Data\Prescriptions\{self.user.userName}.pdf"
        if not self.PrescriptionGenerated():
            return MessageBox(self.ChatWithDoctor_frame, "info", "Prescription is not created yet")
        self.db.write_file(self.Prescription, path)
        subprocess.Popen([path], shell=True)  # Show the Prescription for the patient

    def PrescriptionGenerated(self):
        self.Prescription = self.db.Select("SELECT prescriptionPDF FROM prescriptions WHERE Patient_ID= %s", [self.user.userid])[
            0
        ][0]
        return len(self.Prescription) != 0

    def ChatBoxBlock(self, master):
        self.chatbox = ctk.CTkTextbox(
            master, font=ctk.CTkFont(size=14, weight="bold"), width=650, height=25
        )
        self.chatbox.place(anchor="nw", relx=0.01, rely=0.71)
        self.chatbox.bind(
            "<Return>", self.sendMessage
        )  # Enter Button will send the message
        self.chatbox.bind(
            "<Shift-Return>", self.NewLine
        )  # Shift + Enter will make new line inspired by discord and WhatsApp

        sendimage = ctk.CTkImage(sendICON, size=(25, 25))

        SendIcon = ctk.CTkLabel(
            master, text="", image=sendimage, bg_color="transparent"
        )
        SendIcon.place(anchor="nw", relx=0.68, rely=0.71)
        SendIcon.bind(
            "<Button-1>", self.sendMessage
        )  # Bind if doctor pressed the image text will

    def JoinChatServer(self):
        # Check if the Chat server is online
        try:
            ADDR = ("127.0.0.1", 4073)  # Get the Address of Chat Server
            # Connect user to chat server and set the chat room to patient's ID as the patient will be in it
            self.Userclient = Client(self.user.userName, ADDR, self.user.userid)

            self.LoaddedChat = (
                queue.Queue()
            )  # Queue that will hold the chat from the database to be shown in Chat box
            self.ChatLOGS = (
                queue.Queue()
            )  # Queue that will hold old chat + new chat and save them in database to load it later
            self.LoadChatData(
                self.user.userid
            )  # Load Chat data to LoaddedChat Queue and also ChatLOGS Queue
            self.AddLoadedChat()  # Add old Chat to the Chatbox

            self.CurrentChat = (
                queue.Queue()
            )  # Queue that hold new chat either send or recived

            self.AddTochatBox()  # Function that will run every 1000 ms to check if doctor sends or recives any message
            self.receiveThread = threading.Thread(
                target=self.Userclient.receiveFromServer, args=(self.CurrentChat,)
            )  # Wait any messages from the patient
            self.receiveThread.start()
            # write thread
            writeThread = threading.Thread(
                target=self.Userclient.writeToServer,

            )  # Send any message to the Patient
            writeThread.start()
        except Exception:
            print("Chat Server is offline")

    def LoadChatData(self, Patientid):
        # Load the chat of Patient with id
        res = self.db.Select(
            "SELECT Chat_Logs FROM chatdata WHERE Patient_ID= %s", [self.user.userid]
        )[0][0]
        msg = res.split(
            "&,&"
        )  # split the chat as queue was saved as one string each item separated by &,&
        for i in msg:  # put each message in two Queues
            self.LoaddedChat.put(i)  # Queue that will be Loaded at chat box
            self.ChatLOGS.put(i)  # Queue that will save old chat with the new chat

    def SaveChat(self, chatqueue):
        c = list(chatqueue.queue)  # convert Queue to List
        textChat = "".join(c[i] if i == 0 else f"&,&{c[i]}" for i in range(len(c)))
        # Update the chat in database
        res = self.db.Update(
            "UPDATE chatdata SET Chat_Logs= %s WHERE Patient_ID= %s", [textChat, self.user.userid]
        )
        self.db.Commit()

    def AddLoadedChat(self):
        # check that there is no items in LoaddedChat
        while self.LoaddedChat.qsize() > 0:
            msg = self.LoaddedChat.get()  # get chat data from the Queue
            self.ChatBlock(msg)  # add Chat to Chatbox
            self.ChatFrame.ShowScrollbar()

    def AddTochatBox(self):
        if not self.CurrentChat.empty():  # check if CurrentChat is not empty
            msg = self.CurrentChat.get()  # get the message
            self.ChatLOGS.put(msg)  # save the message in ChatLOGS
            self.SaveChat(self.ChatLOGS)  # update database with new chat data
            if msg != "":
                self.ChatBlock(msg)  # add Chat to Chatbox
            self.ChatFrame.ShowScrollbar()

        self.ChatFrame.after(
            1000, self.AddTochatBox)  # Repeat the function after 1000 ms

    def ChatBlock(self, msg):
        # Create Frame that will hold message of the user
        m_frame = ctk.CTkFrame(self.ChatFrame.scrollable_frame, bg_color="#595656")
        m_frame.pack(anchor="nw", pady=5)
        m_frame.columnconfigure(0, weight=1)

        m_label = tk.Label(
            m_frame,
            wraplength=800,
            fg="black",
            bg="#c5c7c9",
            text=msg,
            font="lucida 14 bold",
            justify="left",
            anchor="w",
        )
        m_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")

    def sendMessage(self, event):
        # -1c means remove the last char which is an end line added by textbox
        self.Userclient.writeToServer(self.chatbox.get("1.0", "end-1c"))
        self.chatbox.delete("1.0", "end")
        return "break"  # to remove defult end line of the textbox

    def NewLine(self, event):
        self.chatbox.insert("end", "\n")  # add an endline to the end of text in textbox
        return "break"

    # Prescriptions Section
    def Prescriptions_button_event(self):
        self.ShowAllPrescriptions()
        self.select_frame_by_name("All My Prescriptions")

    def ShowAllPrescriptions(self):
        if self.Created[3]:
            self.Prescriptions_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[3] = False
        with contextlib.suppress(Exception):
            for widget in self.Prescriptions_frame.winfo_children():
                widget.destroy()
        Title = ctk.CTkLabel(self.Prescriptions_frame,text="All My Prescriptions",font= ctk.CTkFont(size=25,weight="bold"))
        Title.place(anchor="nw", relx=0.35, rely=0.01)
        MainWindow = ScrollableFrame(self.Prescriptions_frame, "gray30",width=1065,height=600,godown=False)
        MainWindow.place(anchor="nw", relx=0, rely=0.1)
        res = self.db.Select("SELECT Doc_ID, prescriptionDate, prescriptionPDF FROM prescriptions WHERE Patient_ID = %s ORDER BY prescriptionDate DESC",[self.user.userid]) 
        for pos, i in enumerate(res):
            self.PrescriptionEntry(MainWindow.scrollable_frame, pos, i[0], i[1], i[2])

    def PrescriptionEntry(self, master, pos, id, presDate, presPDF):
        Frame = ctk.CTkFrame(master, corner_radius=0,fg_color="gray40", width=1065,height=100)
        Frame.grid(row=pos, column=0, pady = 5)

        doctor = User(id)

        doctorNameLabel = ctk.CTkLabel(Frame, text=f"Dr. {doctor.userName}", font= ctk.CTkFont(size=20,weight="bold"))
        doctorNameLabel.place(anchor="nw", relx=0.05, rely=0.4)

        doctorRankLabel = ctk.CTkLabel(Frame, text=doctor.userType, font= ctk.CTkFont(size=20,weight="bold"))
        doctorRankLabel.place(anchor="nw", relx=0.3, rely=0.4)

        DateLabel = ctk.CTkLabel(Frame, text=presDate, font= ctk.CTkFont(size=20,weight="bold"))
        DateLabel.place(anchor="nw", relx=0.6, rely=0.4)

        PDFLabel = ctk.CTkLabel(Frame, text="Download", font= ctk.CTkFont(size=20,weight="bold"), image= ctk.CTkImage(pdflogo,size=(50,50)),compound="left")
        PDFLabel.place(anchor="nw", relx=0.8, rely=0.3)
        PDFLabel.bind("<Button-1>", lambda event: self.DownloadPrescription(event, id, presDate, presPDF))

    def DownloadPrescription(self, event, id, presDate, presPDF):
        SavePath = filedialog.askdirectory(title="Select Where to Download Prescription")
        FullPathName = f"{SavePath}/Prescription_{presDate}.pdf"
        self.db.write_file(presPDF, FullPathName)
        subprocess.Popen([FullPathName], shell=True)  # Show the Prescription for the patient
        return MessageBox(self.Prescriptions_frame,"info","Prescription saved successfully")



        
if __name__ == "__main__":
    app = App()
    app.mainloop()
