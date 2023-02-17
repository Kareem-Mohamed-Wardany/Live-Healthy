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
from User import *
from client import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename


class App(ctk.CTk):
    # load Config dict
    config = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Patient
    user = User("5")  

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

        self.grid_rowconfigure(0, weight=1)  # let the left sidebar take all the space
        self.grid_columnconfigure(1, weight=1)

    def LeftSideBar(self):
        # load images
        self.Male_image = ctk.CTkImage(
            MaleImage,
            size=(self.config.get("UserImageSize"), self.config.get("UserImageSize")),
        )
        self.Female_image = ctk.CTkImage(
            FemaleImage,
            size=(self.config.get("UserImageSize"), self.config.get("UserImageSize")),
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
        
        # self.PurchaseVIP_button = ctk.CTkButton(
        #     self.LeftSideBar_frame,
        #     corner_radius=0,
        #     height=40,
        #     border_spacing=10,
        #     text="Purchase VIP",
        #     fg_color="transparent",
        #     text_color=("gray10", "gray90"),
        #     hover_color=("gray70", "gray30"),
        #     image=self.PurchaseVIP,
        #     anchor="w",
        #     command=self.PatientRequests_button_event,
        # )
        # self.PurchaseVIP_button.grid(row=7, column=0, sticky="ew")

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
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

    def LoadPredictScanFrame(self):
        if self.Created[0]:
            self.Predict_Scan_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            for widget in self.Predict_Scan_frame.winfo_children():
                widget.destroy()
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
        self.Predict()
        # m = ResNetModel()
        # print(m.PredictScan(self.ScanPath))

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
        # print(Label1)
        # print(Label2)
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

        #print(prediction[0][1])

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Predict_Scan_button.configure(
            fg_color=("gray75", "gray25") if name == "Predict_Scan" else "transparent"
        )
        # self.PatientRequests_button.configure(
        #     fg_color=("gray75", "gray25")
        #     if name == "PatientRequests"
        #     else "transparent"
        # )
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
            print(self.winfo_height())
            self.ChatWithDoctor_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent", height= self.winfo_height(), width= self.winfo_width()
            )
            self.Created[1] = False
        with contextlib.suppress(Exception):
            for widget in self.ChatWithDoctor_frame.winfo_children():
                widget.destroy()

        if self.user.checkRequest(): # Check if the Patient already has a request
            res = self.db.Select("SELECT Request_Status FROM requests WHERE Patient_ID= %s", [self.user.userid])[0][0]
            if res == "waiting":
                return MessageBox(self.ChatWithDoctor_frame,"info", "Waiting for a doctor to respond")
            else:
                self.openChat()

        else:
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

    def ImportScan2(self):  # sourcery skip: avoid-builtin-shadow
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
        print(self.prediction)

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

        self.user.addRequest(self.ScanPath, self.prediction, symptoms, illnessTime, medications, extraInfo)
        self.ChatWithDoctor()
        return MessageBox(self.ChatWithDoctor_frame, "info","Successfully added")

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
            self.ChatWithDoctor_frame, corner_radius=0, width=840, fg_color="transparent", height=720
        )
        chatWindow.place(anchor="nw",relx = 0.01,rely = 0.01)

        self.ChatFrame = ScrollableFrame(
            chatWindow, "gray40", width=550, height=330, scrollafter=8
        )
        self.ChatFrame.place(anchor="nw", relx=0.01, rely=0)

        # ChatBox
        self.ChatBoxBlock(chatWindow)
        print(f"--- {time.time() - start_time} seconds ---")
        # join Chat Servrt
        self.JoinChatServer()

    def ChatBoxBlock(self, master):
        self.chatbox = ctk.CTkTextbox(
            master, font=ctk.CTkFont(size=14, weight="bold"), width=520, height=25
        )
        self.chatbox.place(anchor="nw", relx=0.01, rely=0.48)
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
        SendIcon.place(anchor="nw", relx=0.635, rely=0.48)
        SendIcon.bind(
            "<Button-1>", self.sendMessage
        )  # Bind if doctor pressed the image text will

    def JoinChatServer(self):
        # Check if the Chat server is online
        # try:
            ADDR = ("127.0.0.1", 4053)  # Get the Address of Chat Server
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
        # except Exception:
        #     print("Chat Server is offline")

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

    def AddTochatBox(self):
        if not self.CurrentChat.empty():  # check if CurrentChat is not empty
            msg = self.CurrentChat.get()  # get the message
            self.ChatLOGS.put(msg)  # save the message in ChatLOGS
            self.SaveChat(self.ChatLOGS)  # update database with new chat data
            if msg != "":
                self.ChatBlock(msg)  # add Chat to Chatbox

        self.ChatFrame.after(
            1000, self.AddTochatBox)  # Repeat the function after 1000 ms

    def ChatBlock(self, msg):
        # Create Frame that will hold message of the user
        m_frame = ctk.CTkFrame(self.ChatFrame.scrollable_frame, bg_color="#595656")
        m_frame.pack(anchor="nw", pady=5)
        m_frame.columnconfigure(0, weight=1)

        m_label = tk.Label(
            m_frame,
            wraplength=250,
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
