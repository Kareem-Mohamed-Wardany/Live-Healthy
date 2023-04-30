import contextlib
import os
import queue
import shutil
import subprocess
import time
import tkinter as tk
from datetime import date, timedelta
from tkinter import filedialog
from tkinter.ttk import *
from threading import Timer
import customtkinter as ctk
import openai

from client import *
from Config import *
from Database import *
from Error import *
from GUIHelperFunctions import *
from Images import *
from Patient import *
from UserFactory import *
from time import sleep
from ReturnedValueThreading import *
openai.api_key = "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"

class PatGUI(ctk.CTk):
    # load Config dict
    configfile = SystemConfig()
    systemError = SystemErrors()

    # Define the Patient
    Created = [
        True,
        True,
        True,
        True,
        True,
    ]  # Predict X-ray frame, Chat With doctor frame, vipPurchase Frame, Prescriptions Frame , credits PREVENTS duplications

    # Main Constructor
    def __init__(self, id):
        super().__init__()
        self.user = UserFactory.createUser(id, "patient")  
        self.WindowSettings()
        self.LeftSideBar()

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
        self.protocol('WM_DELETE_WINDOW', self.exit_function)

        self.grid_rowconfigure(0, weight=1)  # let the left sidebar take all the space
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        # load images
        self.Male_image = ctk.CTkImage(
            MaleImage,
            size=(self.configfile.get("UserImageSize"), self.configfile.get("UserImageSize")),
        )
        self.Female_image = ctk.CTkImage(
            FemaleImage,
            size=(self.configfile.get("UserImageSize"), self.configfile.get("UserImageSize")),
        )
        self.Predict_scan_image = ctk.CTkImage(
            predict_image,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        self.chat_image = ctk.CTkImage(
            Chat,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        self.PurchaseVIP = ctk.CTkImage(
            PurchaseVIP,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        self.PrescriptionsIcon = ctk.CTkImage(
            Prescriptions,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )
        self.coin_image = ctk.CTkImage(
            coin,
            size=(
                self.configfile.get("ButtonIconsSize"),
                self.configfile.get("ButtonIconsSize"),
            ),
        )

        # create LeftSideBar frame
        self.LeftSideBar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.configfile.get("FrameColor"))
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
                # height=50,
                compound="left",
            )
        else:  # check if the user is a Female to add Male image for him
            self.Image_label = ctk.CTkLabel(
                self.LeftSideBar_frame,
                image=self.Female_image,
                text="",
                # height=50,
                compound="left",
            )
        self.Image_label.grid(row=0, column=0)

        self.PatientName_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userName,
            height=20,
            text_color=self.configfile.get("TextColor"),
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.PatientName_label.grid(row=1, column=0)

        self.PatientAge_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.CalcAge(self.user.userAge),
            height=20,
            compound="left",
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.PatientAge_label.grid(row=2, column=0)
        
        if self.user.userVIPLevel == 1:
            self.VIP_level = ctk.CTkLabel(
                self.LeftSideBar_frame,
                text="",
                image=ctk.CTkImage(bronze,size=(35,35)),
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
                height=40,
                # bottom, center, left, none, right, or top
                compound="left",
                text_color=self.configfile.get("TextColor"),
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            self.VIP_end.grid(row=4, column=0)

        self.Predict_Scan_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            width=200,
            height=40,
            text="Predict X-Ray Scan",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.Predict_scan_image,
            border_spacing= 1,
            anchor="w",
            command=self.Predict_Scan_button_event,
        )  
        self.Predict_Scan_button.grid(row=5, column=0)

        self.ChatWithDoctor_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            text="Chat",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.chat_image,
            anchor="w",
            command=self.ChatWithDoctor_button_event,
        )
        self.ChatWithDoctor_button.grid(row=6, column=0, sticky="ew")
        
        self.PurchaseVIP_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            text="Purchase VIP",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.PurchaseVIP,
            anchor="w",
            command=self.PurchaseVIP_button_event,
        )
        self.PurchaseVIP_button.grid(row=7, column=0, sticky="ew")

        self.Prescriptions_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            text="All My Prescriptions",
            fg_color="transparent",
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.PrescriptionsIcon,
            anchor="w",
            command=self.Prescriptions_button_event,
        )
        self.Prescriptions_button.grid(row=8, column=0, sticky="ew")

        self.Credits_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            fg_color="transparent",
            image=self.coin_image,
            anchor="w",
            text=self.user.userBalance,
            command=self.Credits_button_event,
        )
        self.Credits_button.grid(row=10, column=0, sticky="ew")

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
        self.logoutbutton.grid(row=11, column=0, sticky="ew")
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
        self.appearance_mode_menu.grid(row=12, column=0, padx=20, pady=20, sticky="s")

    def logout(self):
        with contextlib.suppress(Exception):
            shutil.rmtree("Data/Prescriptions/")
            self.Userclient.end()
        self.user.Logout(self)

    def LoadPredictScanFrame(self):
        if self.Created[0]:
            self.Predict_Scan_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Predict_Scan_frame.winfo_children():
                widget.destroy()
        Infotext, self.Price = self.user.PriceInfo("")
        self.Price *= -1 
        MessageBox(self.Predict_Scan_frame,"info",Infotext)

        self.ScanPathEntry = ctk.CTkEntry(self.Predict_Scan_frame, width=700, state="disabled", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"),border_color=self.configfile.get("TextColor"))
        self.ScanPathEntry.place(anchor="nw", relx=0.05, rely=0.05)
        
        ImportScanButton = ctk.CTkButton(self.Predict_Scan_frame,text="Import Scan", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"), command=self.ImportScan)
        ImportScanButton.place(anchor="nw", relx=0.72, rely=0.05)

    def ImportScan(self):
        if self.ScanPathEntry.get() != "":
            self.ScanPathEntry.configure(state="normal")
            self.ScanPathEntry.delete(0, tk.END)

        self.ScanPath = filedialog.askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        self.ScanPathEntry.configure(state="normal")

        self.ScanPathEntry.insert("end", self.ScanPath) 
        self.ScanPathEntry.configure(state="disabled")

        ScanImage = ctk.CTkLabel(self.Predict_Scan_frame,text="",image=ctk.CTkImage(Image.open(self.ScanPath),size=(300,300)))
        ScanImage.place(anchor="nw", relx=0.7, rely=0.2)

        self.ClassOne = ctk.CTkLabel(self.Predict_Scan_frame, width=400, text="", font=ctk.CTkFont(size=16),text_color=self.configfile.get("TextColor"))
        self.ClassOne.place(anchor="nw", relx=0.05, rely=0.15)

        self.ClassTwo = ctk.CTkLabel(self.Predict_Scan_frame, width=400, text="", font=ctk.CTkFont(size=15),text_color=self.configfile.get("TextColor"))
        self.ClassTwo.place(anchor="nw", relx=0.05, rely=0.2)

        if self.user.userVIPLevel < 3:
            res = self.user.updateBalance(self.Predict_Scan_frame, self.Price)
            if res != -1:
                self.Predict()
                self.Credits_button = ctk.CTkButton(
                    self.LeftSideBar_frame,
                    corner_radius=0,
                    height=40,
                    border_spacing=10,
                    text=self.user.userBalance,
                    fg_color="transparent",
                    text_color=self.configfile.get("TextColor"),
                    hover_color=self.configfile.get("BackgroundColor"),
                    image=self.coin_image,
                    anchor="w",
                    command=self.Credits_button_event,
                )
                self.Credits_button.grid(row=10, column=0, sticky="ew")
                SavePredictionButton = ctk.CTkButton(self.Predict_Scan_frame,text="Save Prediction", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"), command= lambda: self.user.SavePrediction(self.ScanPath))
                SavePredictionButton.place(anchor="nw", relx=0.15, rely=0.26)
        else:
            self.Predict()
            SavePredictionButton = ctk.CTkButton(self.Predict_Scan_frame,text="Save Prediction", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"), command= lambda: self.user.SavePrediction(self.ScanPath))
            SavePredictionButton.place(anchor="nw", relx=0.15, rely=0.26)

    def Predict(self):
        Label1 , Label2 =  self.user.PredictMyScan(self.ScanPath, "Two")
        self.pr1 = f"Highest Class Percentage: {Label1}"
        self.pr2 = f"Second Class Percentage: {Label2}"
        self.ClassOne.configure(text=self.pr1)
        self.ClassTwo.configure(text=self.pr2)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.delType()
        self.Predict_Scan_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Predict_Scan" else "transparent"
        )
        self.ChatWithDoctor_button.configure(
            fg_color=self.configfile.get("BackgroundColor")
            if name == "ChatWithDoctor"
            else "transparent"
        )

        self.PurchaseVIP_button.configure(
            fg_color=self.configfile.get("BackgroundColor")
            if name == "PurchaseVIP"
            else "transparent"
        )

        self.Prescriptions_button.configure(
            fg_color=self.configfile.get("BackgroundColor")
            if name == "All My Prescriptions"
            else "transparent"
        )
        self.Credits_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Credits" else "transparent"
        )

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

        if name == "Credits":
            self.credits_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.credits_frame.grid_forget()

    def Predict_Scan_button_event(self):
        self.LoadPredictScanFrame()
        self.select_frame_by_name("Predict_Scan")

    def ChatWithDoctor_button_event(self):
        self.messages = [{"role": "system", "content": "You are an AI model in a medical system that assists pulmonary by interacting with patients and ask them firstly whether they have recent x-ray scan for their lungs or not, if yes ask them to import it to the system so the system can check what pulmonary diseases they have. Secondly ask them to say their symptoms that they feel or have. Thirdly Ask the patients how long they have been experiencing these symptoms because This information will help you and our system to better understand the patient's condition and provide more accurate recommendations for treatment. Fourthly ask them if they take any current medication or if they have taken any medication regarding thier condition. Fifthly ask them if they have any extra information that may be helpful for you to give them a proper medical advice for them after getting all these information predict if the patient has one from five diseases which are Covid-19, Fibrosis, Tuberculosis, viral pneumonia and bacterial pneumonia or if the patient is not having any of theese diseases after that predict if the patient's health state is critical and then give them a proper medical advice and recommend treatments according to their case from x-ray and recommend that they press on a button called Chat With Doctor which exists at the bottom right of the screen in the system in order to to chat with a doctor to help them. Do not answer anything other than pulmonary-related queries. Be positive and calm the patient down, try to ask only one question at each time and not multiple questions at a time. Finally, ask them whether they need anything else, if not thank them for using our system and try to end the conversation politely"}]
        self.ChatWithDoctor()
        self.select_frame_by_name("ChatWithDoctor")

    def PurchaseVIP_button_event(self):
        self.Purchase_VIP()
        self.select_frame_by_name("PurchaseVIP")

    def Purchase_VIP(self):
        if self.Created[2]:
            self.PurchaseVIP_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
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


        subscribeButton = ctk.CTkButton(Bronzeframe,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.user.Subscribe("bronze",self.PurchaseVIP_frame, self.LeftSideBar))
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


        subscribeButton = ctk.CTkButton(silverFrame,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.user.Subscribe("silver",self.PurchaseVIP_frame,self.LeftSideBar))
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


        subscribeButton = ctk.CTkButton(Goldframe,text="Subscribe", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.user.Subscribe("gold",self.PurchaseVIP_frame,self.LeftSideBar))
        subscribeButton.place(anchor="nw", relx=0.225, rely=0.82)   

    def Credits_button_event(self):
        self.loadCreditRecharge()
        self.select_frame_by_name("Credits")

    def loadCreditRecharge(self):
        # Prevent Error for stucking in this frame and can not enter other Frames
        if self.Created[4]:
            self.credits_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[4] = False

        # Remove card type|Specific amount entry in each start for frame as user may nav to other Frames and want to go back to this frame
        self.delType()
        # self.RemoveAmount("")

        # Credit Card Section
        self.CreditCardBlock()

        # Recharge Section
        self.RechargeBlock()

    def delType(self):
        # Try to handle error if any type was not shown so it will throw an error
        with contextlib.suppress(Exception):
            self.Americanlabel.destroy()
        with contextlib.suppress(Exception):
            self.Visalabel.destroy()
        with contextlib.suppress(Exception):
            self.Masterlabel.destroy()

    def CreditCardBlock(self):
        self.CardChecked = False
        self.InformationLabel = ctk.CTkLabel(
            self.credits_frame,
            text="Credit Card Information",
            text_color=self.configfile.get("TextColor"),
            width=60,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.InformationLabel.place(anchor="nw", relx=0.37, rely=0.05)

        self.CardNumber = ctk.CTkEntry(
            self.credits_frame,
            placeholder_text="Credit Card Number",
            text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("TextColor"),
            fg_color=self.configfile.get("FrameColor"),
            placeholder_text_color=self.configfile.get("TextColor"),
            width=200,
            font=ctk.CTkFont(size=14),
        )  # 5471462613718519
        self.CardNumber.place(anchor="nw", relx=0.05, rely=0.15)
        self.CardNumber.bind(
            "<Leave>", self.CardNumberValidation
        )  # Handle all functions will be applied for card number + validation

        self.CVV = ctk.CTkEntry(
            self.credits_frame,
            show="*",
            placeholder_text="CVV",
            fg_color=self.configfile.get("FrameColor"),
            text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("TextColor"),
            placeholder_text_color=self.configfile.get("TextColor"),
            width=70,
            font=ctk.CTkFont(size=14),
        )
        self.CVV.place(anchor="nw", relx=0.35, rely=0.15)
        self.CVV.bind("<Leave>", self.HandleCVV)

        self.ExpireMonth = ctk.CTkComboBox(
            self.credits_frame,
            fg_color=self.configfile.get("FrameColor"),
            button_color=self.configfile.get("FrameColor"),
            text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("FrameColor"),
            width=60,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        )
        self.ExpireMonth.place(anchor="nw", relx=0.55, rely=0.15)

        self.slashLabel = ctk.CTkLabel(
            self.credits_frame, text="/", width=20, font=ctk.CTkFont(size=14),text_color=self.configfile.get("TextColor")
        )
        self.slashLabel.place(anchor="nw", relx=0.615, rely=0.15)

        self.ExpireYear = ctk.CTkComboBox(
            self.credits_frame,
            fg_color=self.configfile.get("FrameColor"),
            button_color=self.configfile.get("FrameColor"),
            text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("FrameColor"),
            width=60,
            values=["21", "22", "23", "24", "25", "26", "27"],
        )
        self.ExpireYear.place(anchor="nw", relx=0.64, rely=0.15)

        self.CheckCard = ctk.CTkButton(
            self.credits_frame,
            text="Check Card Expiration",
            anchor="w",
            text_color=self.configfile.get("TextColor"), 
            fg_color=self.configfile.get("FrameColor"), 
            hover_color=self.configfile.get("FrameColor"),
            command=self.CheckCard_button_event,
        )
        self.CheckCard.place(anchor="nw", relx=0.74, rely=0.15)

    def CardNumberValidation(self, event):
        if (
            len(self.CardNumber.get()) != 16 or self.CardNumber.get().isalpha()
        ):  # 5471462613718519
            self.CardChecked = False
            return MessageBox(self.credits_frame, "warning", "Credit Card is not 16 digit")
        else:
            self.FormateCreditCard()
            self.CreditCardType()
            self.CardChecked = True

    def CreditCardType(self):
        # ---------------
        # American Express cards always begin with the number 3, more specifically 34 or 37.
        # Visa cards begin with the number 4.
        # Mastercards start with the number 5
        # Test Cases 4471462613718519 , 3471462613718519 , 5471462613718519
        if len(self.CardNumber.get()) != 0:  # check if Card Number is not Empty
            # load card Types Images into its label
            string = self.CardNumber.get()
            if int(string[0]) == 3:
                self.Americanlabel = ctk.CTkLabel(
                    self,
                    text="",
                    image=ctk.CTkImage(americanexpress, size=(25, 25)),
                )
                self.Americanlabel.place(anchor="nw", relx=0.36, rely=0.15)
            elif int(string[0]) == 4:
                self.Visalabel = ctk.CTkLabel(
                    self.credits_frame,
                    text="",
                    image=ctk.CTkImage(visa, size=(25, 25)),
                )
                self.Visalabel.place(anchor="nw", relx=0.25, rely=0.15)
            elif int(string[0]) == 5:
                self.Masterlabel = ctk.CTkLabel(
                    self.credits_frame,
                    text="",
                    image=ctk.CTkImage(mastercard, size=(25, 25)),
                )
                self.Masterlabel.place(anchor="nw", relx=0.25, rely=0.15)

    def FormateCreditCard(self):
        if len(self.CardNumber.get()) != 0:  # check if Card Number is not Empty
            # load card Types Images into its label
            string = self.CardNumber.get()
            x = " ".join(
                string[i : i + 4] for i in range(0, len(string), 4)
            )  # 3471462613718519 -> 3471 4626 1371 8519
            self.CardNumber.delete(
                "0", tk.END
            )  # Delete old card Number 3471462613718519
            self.CardNumber.insert(
                "end", x
            )  # Set Card Number IN GUI 3471 4626 1371 8519

    def HandleCVV(self, event):
        if len(self.CVV.get()) != 3 or self.CVV.get().isalpha():
            self.CardChecked = False
            MessageBox(self.credits_frame, "warning", "CVV is not 3 digit")
        else:
            self.CardChecked = True

    def CheckCard_button_event(self):
        Year = f"20{self.ExpireYear.get()}"
        if int(Year) < date.today().year:
            self.CardChecked = False
            return messagebox.showerror("Error", self.systemError.get(16), icon="error", parent=self.LeftSideBar_frame)
        if (
            int(self.ExpireMonth.get()) < date.today().month
            and int(Year) == date.today().year
        ):
            self.CardChecked = False
            return messagebox.showerror("Error", self.systemError.get(16), icon="error", parent=self.LeftSideBar_frame)
        else:
            self.CardChecked = True

    def RechargeBlock(self):
        self.PurchaseLabel = ctk.CTkLabel(
            self.credits_frame,
            text="Purchase Credits",
            text_color=self.configfile.get("TextColor"),
            width=60,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.PurchaseLabel.place(anchor="nw", relx=0.37, rely=0.28)
        
        self.AddPlan(0.06, 0.35, cashlvl1, "100", "7", "1")
        self.AddPlan(0.36, 0.35, cashlvl2, "200", "12", "2")
        self.AddPlan(0.66, 0.35, cashlvl3, "400", "20", "3")

    def AddPlan(self, x, y, pic, coins, pri, level):
        Plan = ctk.CTkFrame(self.credits_frame, corner_radius=10, fg_color="#C0C0C0",height= 450, width=230)
        Plan.place(anchor="nw", relx=x, rely=y)

        MoneyImage = ctk.CTkLabel(Plan,text="",image=ctk.CTkImage(pic,size=(75,75)))
        MoneyImage.place(anchor="nw", relx=0.325, rely=0.01)

        Credits = ctk.CTkLabel(Plan,text=coins, image=ctk.CTkImage(coin,size=(60,60)),compound="left",text_color="#00246B", font= ctk.CTkFont(size=15, weight="bold"))
        Credits.place(anchor="nw", relx=0.3, rely=0.27)

        price = ctk.CTkLabel(Plan,text=pri, image=ctk.CTkImage(dollar,size=(60,60)),compound="left",text_color="#00246B", font= ctk.CTkFont(size=15, weight="bold"))
        price.place(anchor="nw", relx=0.3, rely=0.47)

        PurchaseButton = ctk.CTkButton(Plan,text="Purchase", fg_color="#f3ca20", text_color="#000000", hover_color="#e1e1bd",font=ctk.CTkFont(size=14, weight="bold"), command= lambda: self.user.Purchase(level, Plan, self.LeftSideBar, self.CardChecked))
        PurchaseButton.place(anchor="nw", relx=0.2, rely=0.82) 

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.user.SetApperanceMode(new_appearance_mode)

    def ChatWithDoctor(self):  # Fix the box colors, turn them all Textbox instead of Entry
        if self.Created[1]:
            self.ChatWithDoctor_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent", height= self.winfo_height(), width= self.winfo_width()
            )
            self.Created[1] = False
        with contextlib.suppress(Exception):
            for widget in self.ChatWithDoctor_frame.winfo_children():
                widget.destroy()
            os.mkdir("Data/Prescriptions/")

        if self.user.checkRequest(): # Check if the Patient already has a request
            res = SelectQuery("SELECT Request_Status FROM requests WHERE Patient_ID= %s", [self.user.userid])[0][0]
            if res == "waiting":
                return MessageBox(self.ChatWithDoctor_frame,"info", "Waiting for a doctor to respond")
            self.DoctorID = SelectQuery("SELECT Doc_ID FROM chatdata WHERE Patient_ID= %s", [self.user.userid])[0][0]
            self.openChat()

        else:
            self.openChat(True)

            ImportScanButton = ctk.CTkButton(self.ChatWithDoctor_frame,text="Import Scan", text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor"),command=self.RequestScan)
            ImportScanButton.place(anchor="nw", relx=0.77, rely=0.05)

            ConsultLabel = ctk.CTkLabel(self.ChatWithDoctor_frame, text="Chat With Doctor", font= ctk.CTkFont(size=20,weight="bold"), image= ctk.CTkImage(consultation,size=(50,50)),compound="left", text_color=self.configfile.get("TextColor"))
            ConsultLabel.place(anchor="nw", relx=0.75, rely=0.9)
            ConsultLabel.bind("<Button-1>", lambda event: self.Consult(event))

    ScanPath=""
    prediction=""
    def RequestScan(self): 
        self.ScanPath = filedialog.askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        self.ChatBlock("Bot is analyzing...")
        self.prediction= self.user.PredictMyScan(self.ScanPath, "One")
        self.messages.append({"role": "system", "content": f"patient scan prediction is {self.prediction}, but don't share it immediately with the patient and share it at the end of the conversation after them answering all the questions you ask"})
        ScanImage = ctk.CTkLabel(self.ChatWithDoctor_frame,text="",image=ctk.CTkImage(Image.open(self.ScanPath),size=(300,300)))
        ScanImage.place(anchor="nw", relx=0.7, rely=0.2)
        answer = f"Live Healthy bot: {self.CustomChatGPT2()}"
        self.ChatBlock(answer, True)
        return messagebox.showinfo("Info", "Your scan has been imported")
    
    def Consult(self, event):
        if len(self.messages) <=1:
            return messagebox.showerror("Error", self.systemError.get(27))
        chat=[]
        for i in range(1, len(self.messages)):
            if self.messages[i]["role"] =="user":
                txt = self.messages[i]["content"]
                chat.append(f"{self.user.userName}: {txt}")

            elif self.messages[i]["role"] =="assistant":
                txt = self.messages[i]["content"]
                chat.append(f"Live Healthy bot: {txt}")
        textChat = "".join(chat[i] if i == 0 else f"&,&{chat[i]}" for i in range(len(chat)))
        self.FillRequest(textChat)

    def FillRequest(self, Chatlog):
        Infotext, self.Price = self.user.PriceInfo("Chat")
        self.Price *= -1 
        MessageBox(self.ChatWithDoctor_frame,"info",Infotext)
        if self.user.userVIPLevel < 3:
            res = self.user.updateBalance(self.ChatWithDoctor_frame, self.Price)
            if res != -1:
                self.user.CreateRequest(self.ScanPath, self.prediction, Chatlog)
                self.Credits_button = ctk.CTkButton(
                    self.LeftSideBar_frame,
                    corner_radius=0,
                    height=40,
                    border_spacing=10,
                    text=self.user.userBalance,
                    fg_color="transparent",
                    text_color=self.configfile.get("TextColor"),
                    hover_color=self.configfile.get("BackgroundColor"),
                    image=self.coin_image,
                    anchor="w",
                    command=self.Credits_button_event,
                )
                self.Credits_button.grid(row=10, column=0, sticky="ew")
                return MessageBox(self.ChatWithDoctor_frame, "info","Successfully added")
                
        else:
            self.user.CreateRequest(self.ScanPath, self.prediction, Chatlog)
            return MessageBox(self.ChatWithDoctor_frame, "info","Successfully added")

    # Chat Section
    def openChat(self, Bot=False):
    # Chat window that will contain ChatFrame that show the chat for the doctor and chatbox where the doctor type in his chat
    # also send icon that will show the text in chatbox on ChatFrame for both patient and doctor
        with contextlib.suppress(Exception):
            for widget in self.chatWindow.winfo_children():
                widget.destroy()
            self.Userclient.end()
        start_time = time.time()
        self.chatWindow = ctk.CTkFrame(
            self.ChatWithDoctor_frame, corner_radius=0, width=1000, fg_color="transparent", height=720
        )
        self.chatWindow.place(anchor="nw",relx = 0.01,rely = 0.01)

        self.ChatFrame = ctk.CTkScrollableFrame(
            self.chatWindow, fg_color=self.configfile.get("FrameColor"), width=700, height=500,scrollbar_button_color=self.configfile.get("FrameColor"), scrollbar_button_hover_color=self.configfile.get("TextColor"))
        self.ChatFrame.place(anchor="nw", relx=0.01, rely=0)
        # Doctor Data
        if not Bot:
            self.DoctorData(self.chatWindow)

        # ChatBox
        self.ChatBoxBlock(self.chatWindow, Bot)

        print(f"--- {time.time() - start_time} seconds ---")

        # if not Bot:
        # join Chat Servrt
            # self.JoinChatServer()

    def DoctorData(self, master):
        DoctorData = UserFactory.createUser(self.DoctorID,"doctor")  # Get the patient Data

        if DoctorData.userGender == "Male":
            Imagesrc = ctk.CTkImage(MaleImage, size=(200, 200))
        else:
            Imagesrc = ctk.CTkImage(FemaleImage, size=(200, 200))

        Patientinfo = ctk.CTkFrame(master,fg_color="transparent")
        Patientinfo.place(anchor="nw", relx=0.8, rely=0.005)

        PImage = ctk.CTkLabel(Patientinfo, height=40, text="", image=Imagesrc)
        PImage.grid(row=0, column=0)
        PName = ctk.CTkLabel(
            Patientinfo,
            height=10,
            text=DoctorData.userName,
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        PName.grid(row=1, column=0)

        PAge = ctk.CTkLabel(
            Patientinfo,
            height=10,
            text=DoctorData.userType,
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PAge.grid(row=2, column=0)

    def ChatBoxBlock(self, master, bot):
        self.chatbox = ctk.CTkTextbox(
            master, font=ctk.CTkFont(size=14, weight="bold"), width=675, height=25,fg_color= self.configfile.get("FrameColor"), text_color=self.configfile.get("TextColor"),border_color=self.configfile.get("TextColor"),border_width=1)
        self.chatbox.place(anchor="nw", relx=0.01, rely=0.72)
        self.chatbox.bind(
            "<Return>", lambda event,BOT=bot: self.sendMessage(event,BOT)
        )  # Enter Button will send the message
        self.chatbox.bind(
            "<Shift-Return>", self.NewLine
        )  # Shift + Enter will make new line inspired by discord and WhatsApp

        sendimage = ctk.CTkImage(sendICON, size=(25, 25))

        SendIcon = ctk.CTkLabel(
            master, text="", image=sendimage, bg_color="transparent"
        )
        SendIcon.place(anchor="nw", relx=0.7, rely=0.72)
        SendIcon.bind(
            "<Button-1>", lambda event,BOT=bot: self.sendMessage(event,BOT)
        )  # Bind if patient pressed the image text will

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
            self.LoadChatData()  # Load Chat data to LoaddedChat Queue and also ChatLOGS Queue
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

    def LoadChatData(self):
        # Load the chat of Patient with id
        res = SelectQuery(
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
        res = UpdateQuery(
            "UPDATE chatdata SET Chat_Logs= %s WHERE Patient_ID= %s", [textChat, self.user.userid]
        )

    def AddLoadedChat(self):
        # check that there is no items in LoaddedChat
        while self.LoaddedChat.qsize() > 0:
            msg = self.LoaddedChat.get()  # get chat data from the Queue
            self.ChatBlock(msg)  # add Chat to Chatbox

    def AddTochatBox(self):
        if not self.CurrentChat.empty():  # check if CurrentChat is not empty
            msg = self.CurrentChat.get()  # get the message
            self.ChatLOGS.put(msg)  # save the message in ChatLOGS
            self.SaveChat(self.ChatLOGS)  # update database with new chat data
            if msg != "":
                self.ChatBlock(msg)  # add Chat to Chatbox

        self.ChatFrame.after(
            1000, self.AddTochatBox)  # Repeat the function after 1000 ms

    def ChatBlock(self, msg, last=False):
        # Create Frame that will hold message of the user
        if last:  
            with contextlib.suppress(Exception):            
                self.ChatFrame.winfo_children()[-1].destroy()
            m_frame = ctk.CTkFrame(self.ChatFrame,fg_color="transparent")
            m_frame.pack(anchor="nw", pady=5)
            m_label = ctk.CTkLabel(
                m_frame,
                wraplength=600,
                text=msg,
                height=20,
                font=ctk.CTkFont("lucida",size=14,weight="bold"),
                text_color="#ffc0cb",
                justify="left",
                anchor="w")
            m_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")
        else:
            m_frame = ctk.CTkFrame(self.ChatFrame,fg_color="transparent")
            m_frame.pack(anchor="nw", pady=5)
            m_label = ctk.CTkLabel(
                m_frame,
                wraplength=600,
                text=msg,
                height=20,
                font=ctk.CTkFont("lucida",size=14,weight="bold"),
                text_color=self.configfile.get("TextColor"),
                justify="left",
                anchor="w")
            m_label.grid(row=1, column=1, padx=2, pady=2, sticky="w")

    def sendMessage(self, event, bot):
        # -1c means remove the last char which is an end line added by textbox
        txt = self.chatbox.get("1.0", "end-1c")
        self.chatbox.delete("1.0", "end")
        if bot:
            fulltext = f"{self.user.userName}: {txt}"
            self.ChatBlock(fulltext)
            self.ChatBlock("Bot is typing...")
            t = Timer(15, self.chatwithbot, [txt]) 
            t.start()
        else:
            self.Userclient.writeToServer(txt)
        return "break"  # to remove defult end line of the textbox

    def chatwithbot(self, msg):
        # Handle Run time to get no error with response
        gptthread = ReturnValueThread(target=self.CustomChatGPT,args=(msg,))
        gptthread.start()
        ans = gptthread.join()
        fullans = f"Live Healthy bot: {ans}"
        self.ChatBlock(fullans, True)

    def CustomChatGPT(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": ChatGPT_reply})
        return ChatGPT_reply
    
    def CustomChatGPT2(self):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": ChatGPT_reply})
        return ChatGPT_reply

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
        Title = ctk.CTkLabel(self.Prescriptions_frame,text="All My Prescriptions",font= ctk.CTkFont(size=25,weight="bold"),text_color=self.configfile.get("TextColor"))
        Title.place(anchor="nw", relx=0.35, rely=0.01)
        MainWindow = ctk.CTkScrollableFrame(self.Prescriptions_frame, fg_color=self.configfile.get("FrameColor"),width=1040,height=600,scrollbar_button_color=self.configfile.get("FrameColor"), scrollbar_button_hover_color=self.configfile.get("TextColor"))
        MainWindow.place(anchor="nw", relx=0.01, rely=0.1)
        res = self.user.MyPrescriptions()
        if len(res)==0:
            NoData= ctk.CTkLabel(MainWindow, text="No Prescriptions Found!" , width=1040, height=self.winfo_height() - 150, text_color=self.configfile.get("TextColor"), font=ctk.CTkFont(size=20))
            NoData.grid(row=0, column=0, pady=6)
        for pos, i in enumerate(res):
            self.PrescriptionEntry(MainWindow, pos, i[0], i[1], i[2])

    def PrescriptionEntry(self, master, pos, id, presDate, presPDF):
        Frame = ctk.CTkFrame(master, corner_radius=0,fg_color="transparent", width=1065,height=100)
        Frame.grid(row=pos, column=0, pady = 5)

        doctor = UserFactory.createUser(id,"doctor")

        doctorNameLabel = ctk.CTkLabel(Frame, text=f"Dr. {doctor.userName}", font= ctk.CTkFont(size=20,weight="bold"), text_color=self.configfile.get("TextColor"))
        doctorNameLabel.place(anchor="nw", relx=0.05, rely=0.4)

        doctorRankLabel = ctk.CTkLabel(Frame, text=doctor.userType, font= ctk.CTkFont(size=20,weight="bold"), text_color=self.configfile.get("TextColor"))
        doctorRankLabel.place(anchor="nw", relx=0.3, rely=0.4)

        DateLabel = ctk.CTkLabel(Frame, text=presDate, font= ctk.CTkFont(size=20,weight="bold"), text_color=self.configfile.get("TextColor"))
        DateLabel.place(anchor="nw", relx=0.6, rely=0.4)

        PDFLabel = ctk.CTkLabel(Frame, text="Download", font= ctk.CTkFont(size=20,weight="bold"), image= ctk.CTkImage(pdflogo,size=(50,50)),compound="left", text_color=self.configfile.get("TextColor"))
        PDFLabel.place(anchor="nw", relx=0.8, rely=0.3)
        PDFLabel.bind("<Button-1>", lambda event: self.user.DownloadPrescription(event, presDate, presPDF, self.Prescriptions_frame))

    def exit_function(self):
        with contextlib.suppress(Exception):
            shutil.rmtree("Data/Prescriptions/")
            self.Userclient.end()
        self.destroy()

if __name__ == "__main__":
    app = PatGUI(23)
    app.mainloop()
