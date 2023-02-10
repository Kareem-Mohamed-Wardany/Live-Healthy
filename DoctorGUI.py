import contextlib
import tkinter as tk
from datetime import date
import queue
import time
import os
import customtkinter as ctk

from Images import *
from Config import *
from Database import *
from GUIHelperFunctions import *
from User import *
from client import *


class App(ctk.CTk):
    # load Config dict
    config = SystemConfig()

    # connect to DB
    db = Database()

    # Define the Doctor
    user = User("4")  # 2 Khaled Cons   4 Amira Spec

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
        Title = f"Welcome {self.user.userType} {self.user.userName}"
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
        self.Active_chats_image = ctk.CTkImage(
            ActiveChats,
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
            5, weight=1
        )  # let row 5 with bigger weight to sperate between credit button, apperance mode and other button

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
        self.DoctorName_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userName,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.DoctorName_label.grid(row=1, column=0)

        self.DoctorJob_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userType,
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.DoctorJob_label.grid(row=2, column=0)

        self.Active_Chats_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Active Chats",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.Active_chats_image,
            anchor="w",
            command=self.Active_Chats_button_event,
        )  #
        self.Active_Chats_button.grid(row=3, column=0, sticky="ew")

        self.PatientRequests_button = ctk.CTkButton(
            self.LeftSideBar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Patients Requests",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.chat_image,
            anchor="w",
            command=self.PatientRequests_button_event,
        )  #
        self.PatientRequests_button.grid(row=4, column=0, sticky="ew")

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
        self.Credits_button.grid(row=6, column=0, sticky="ew")
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
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

    # Active Chat Section
    def LoadActiveChat(self):
        # Prevent Error for stucking in this frame and can not enter other Frames
        if self.Created[0]:
            self.Active_Chats_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[0] = False
        with contextlib.suppress(Exception):
            self.Userclient.end()
        for widget in self.Active_Chats_frame.winfo_children():
            widget.destroy()

        # Get Ids for all patients that chat with that doctor
        res = self.user.GetMyChatMembers()
        self.MyChats(res)

    def MyChats(self, res):
        # Create Scrollable Frame to hold all chats for Doctor
        frame = ScrollableFrame(
            self.Active_Chats_frame, "gray30", width=250, height=714
        )
        frame.grid(row=0, column=0, sticky="nsew")
        start_time = time.time()
        for pos, item in enumerate(res):
            self.AddtoChatMenu(frame.scrollable_frame, item[0], pos)
        print(f"--- {time.time() - start_time} seconds ---")

    def AddtoChatMenu(self, master, id, pos):
        output = self.db.Select("SELECT Name, Gender FROM users WHERE ID=%s", [id])
        Name = output[0][0]
        Gender = output[0][1]
        if Gender == "Male":
            Imagesrc = ctk.CTkImage(ChatMaleImage, size=(50, 50))
        else:
            Imagesrc = ctk.CTkImage(ChatFemaleImage, size=(50, 50))
        self.patientChat = ctk.CTkButton(
            master,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=Name,
            width=250,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray20", "gray60"),
            image=Imagesrc,
            anchor="w",
            command=lambda m=id: self.openChat(m),
        )
        self.patientChat.grid(row=pos, column=0, pady=6)

    def openChat(self, id):
        # Chat window that will contain ChatFrame that show the chat for the doctor and chatbox where the doctor type in his chat
        # also send icon that will show the text in chatbox on ChatFrame for both patient and doctor
        with contextlib.suppress(Exception):
            for widget in chatWindow.winfo_children():
                widget.destroy()
            self.Userclient.end()
        start_time = time.time()
        chatWindow = ctk.CTkFrame(
            self.Active_Chats_frame, corner_radius=0, width=840, fg_color="transparent"
        )
        chatWindow.grid(row=0, column=4, sticky="NSEW")

        self.ChatFrame = ScrollableFrame(
            chatWindow, "gray40", width=550, height=400, scrollafter=8
        )
        self.ChatFrame.place(anchor="nw", relx=0.01, rely=0)

        # End Chat
        self.EndChatButton(chatWindow, id)

        # Report Patient
        self.ReportPatient(chatWindow, id)

        # Generate Prescription for a Patient
        self.GeneratePrescription(chatWindow)

        # ChatBox
        self.ChatBoxBlock(chatWindow)

        # Patient Basic data
        self.PatientData(chatWindow, id)

        # Patient Health Status
        self.PatientHealthStatus(chatWindow, id)

        # Patient Data Filled During Creating Request
        self.PatientRequestData(chatWindow, id)
        print(f"--- {time.time() - start_time} seconds ---")
        # join Chat Servrt
        self.JoinChatServer()

    def ChatBoxBlock(self, master):
        self.chatbox = ctk.CTkTextbox(
            master, font=ctk.CTkFont(size=14, weight="bold"), width=520, height=25
        )
        self.chatbox.place(anchor="nw", relx=0.01, rely=0.57)
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
        SendIcon.place(anchor="nw", relx=0.635, rely=0.57)
        SendIcon.bind(
            "<Button-1>", self.sendMessage
        )  # Bind if doctor pressed the image text will

    def PatientData(self, master, id):
        PatientData = User(id)  # Get the patient Data

        if PatientData.userGender == "Male":
            Imagesrc = ctk.CTkImage(MaleImage, size=(100, 100))
        else:
            Imagesrc = ctk.CTkImage(FemaleImage, size=(100, 100))
        PImage = ctk.CTkLabel(master, height=40, text="", image=Imagesrc)
        PImage.place(anchor="nw", relx=0.81, rely=0.005)
        PName = ctk.CTkLabel(
            master,
            height=10,
            text=PatientData.userName,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        PName.place(anchor="nw", relx=0.855, rely=0.15)
        PAge = ctk.CTkLabel(
            master,
            height=10,
            text=PatientData.userAge,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PAge.place(anchor="nw", relx=0.855, rely=0.18)

        PBloodType = ctk.CTkLabel(
            master,
            height=10,
            text=PatientData.Blood_Type,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PBloodType.place(anchor="nw", relx=0.855, rely=0.21)

    def PatientHealthStatus(self, master, id):
        PatientData = User(id)  # Get the patient Data

        # Frame that holds all health Status of the patients as Checkbox if he has that status it will be checked
        HealthStatusFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            width=290,
            height=250,
            fg_color="transparent",
            bg_color="gray40",
        )
        HealthStatusFrame.place(anchor="nw", relx=0.01, rely=0.63)

        HealthStatusLabel = ctk.CTkLabel(
            HealthStatusFrame,
            height=10,
            text="Patient Health Status:",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="gray40",
        )
        HealthStatusLabel.place(anchor="nw", relx=0.2, rely=0.03)

        AllergiesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Allergies",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        AllergiesBox.place(anchor="nw", relx=0.03, rely=0.15)

        DiabetesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Diabetes",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        DiabetesBox.place(anchor="nw", relx=0.03, rely=0.35)

        CancerBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Cancer",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        CancerBox.place(anchor="nw", relx=0.03, rely=0.55)

        Heart_DiseasesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Heart Diseases",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        Heart_DiseasesBox.place(anchor="nw", relx=0.03, rely=0.75)

        ObesityBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Obesity",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        ObesityBox.place(anchor="nw", relx=0.5, rely=0.15)

        SmokerBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Smoker",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        SmokerBox.place(anchor="nw", relx=0.5, rely=0.35)

        HypertensionBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Hypertension",
            state="disabled",
            bg_color="gray40",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled="#000000",
        )
        HypertensionBox.place(anchor="nw", relx=0.5, rely=0.55)

        # Check the box if he has this state
        if PatientData.Heart_Diseases:
            Heart_DiseasesBox.select()
        if PatientData.Diabetes:
            DiabetesBox.select()
        if PatientData.Cancer:
            CancerBox.select()
        if PatientData.Obesity:
            ObesityBox.select()
        if PatientData.Smoker:
            SmokerBox.select()
        if PatientData.Hypertension:
            HypertensionBox.select()
        if PatientData.Allergies:
            AllergiesBox.select()

    def PatientRequestData(self, master, id):
        PatientData = User(id)  # Get the patient Data
        res = self.db.Select(
            "SELECT Symptoms, X_ray_scan, Prediction, Medications, Extra_Info, Illness_Time FROM requests WHERE Patient_ID= %s",
            [id],
        )
        (
            Symptoms,
            X_ray_scan,
            Prediction,
            Medications,
            Extra_Info,
            Illness_Time,
        ) = self.FetchPatientData(res[0])

        if Extra_Info is None:
            Extra_Info = "-"
        if Medications is None:
            Medications = "-"

        # Create blocks that will contain Symptoms, Medications, Illness_Time, Extra_Info
        self.Createblock(master, 0.71, 0.24, 230, 90, "Symptoms", Symptoms)
        self.Createblock(master, 0.71, 0.38, 230, 90, "Medications", Medications)
        self.Createblock(master, 0.71, 0.52, 230, 90, "Illness_Time", Illness_Time)
        self.Createblock(master, 0.71, 0.66, 230, 90, "Extra_Info", Extra_Info)

        # Scan Block will contain Patient X-ray Scan with the prediction made by the system
        self.createScanBlock(
            master,
            PatientData.userName,
            0.39,
            0.63,
            250,
            250,
            X_ray_scan,
            Prediction,
        )

    def EndChatButton(self, master, id):
        # END Chat
        EndChat = ctk.CTkLabel(
            master,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(CloseDoctorChat, size=(40, 40)),
        )
        EndChat.place(anchor="nw", relx=0.95, rely=0.92)
        EndChat.bind("<Button-1>", lambda event: self.EndButtonEvent(event, id))

    def ReportPatient(self, master, id):
        PatientData = User(id)  # Get the patient Data
        # Report Patient
        ReportPatient = ctk.CTkLabel(
            master,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(ReportUser, size=(40, 40)),
        )
        ReportPatient.place(anchor="nw", relx=0.89, rely=0.92)
        ReportPatient.bind(
            "<Button-1>",
            lambda event: self.ReportReasonBlock(event, PatientData.userName, id),
        )

    def GeneratePrescription(self, master):
        # Generate Prescription for a Patient
        GenerateReport = ctk.CTkLabel(
            master,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(GeneratePrescription, size=(40, 40)),
        )
        GenerateReport.place(anchor="nw", relx=0.83, rely=0.92)

    def JoinChatServer(self):
        # Check if the Chat server is online
        try:
            ADDR = ("127.0.0.1", 4073)  # Get the Address of Chat Server
            # Connect user to chat server and set the chat room to patient's ID as the patient will be in it
            self.Userclient = Client(self.user.userName, ADDR, id)

            self.LoaddedChat = (
                queue.Queue()
            )  # Queue that will hold the chat from the database to be shown in Chat box
            self.ChatLOGS = (
                queue.Queue()
            )  # Queue that will hold old chat + new chat and save them in database to load it later
            self.LoadChatData(
                id
            )  # Load Chat data to LoaddedChat Queue and also ChatLOGS Queue
            self.AddLoadedChat()  # Add old Chat to the Chatbox

            self.CurrentChat = (
                queue.Queue()
            )  # Queue that hold new chat either send or recived

            self.AddTochatBox(
                id
            )  # Function that will run every 1000 ms to check if doctor sends or recives any message
            self.receiveThread = threading.Thread(
                target=self.Userclient.receiveFromServer, args=(self.CurrentChat,)
            )  # Wait any messages from the patient
            self.receiveThread.start()
            # write thread
            writeThread = threading.Thread(
                target=self.Userclient.writeToServer,
                args=(self.chatbox.get("1.0", "end-1c"),),
            )  # Send any message to the Patient
            writeThread.start()
        except Exception:
            print("Chat Server is offline")

    def LoadChatData(self, Patientid):
        # Load the chat of Patient with id
        res = self.db.Select(
            "SELECT Chat_Logs FROM chatdata WHERE Patient_ID= %s", [Patientid]
        )[0][0]
        msg = res.split(
            "&,&"
        )  # split the chat as queue was saved as one string each item separated by &,&
        for i in msg:  # put each message in two Queues
            self.LoaddedChat.put(i)  # Queue that will be Loaded at chat box
            self.ChatLOGS.put(i)  # Queue that will save old chat with the new chat

    def Createblock(self, master, x, y, w, h, Title, Content):
        # Frame that will hold label with Title and Textbox that is disabled to use the scroll feature in it
        blockFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            width=w,
            height=h,
            fg_color="transparent",
            bg_color="gray40",
        )
        blockFrame.place(anchor="nw", relx=x, rely=y)

        firsttextLabel = ctk.CTkLabel(
            blockFrame,
            height=10,
            text=Title,
            font=ctk.CTkFont(size=12, weight="bold"),
            bg_color="gray40",
        )
        firsttextLabel.place(anchor="nw", relx=0.01, rely=0.01)

        wid = w - ((20 / w) * 100)
        text = ctk.CTkTextbox(
            blockFrame,
            height=50,
            width=wid,
            font=ctk.CTkFont(size=12, weight="bold"),
            bg_color="gray40",
        )
        text.place(anchor="nw", relx=0.03, rely=0.36)
        text.insert("end", Content)
        text.configure(state="disabled")

    def createScanBlock(self, master, name, x, y, w, h, scan, prediction):
        # Frame that will hold Scan Image and Label for its prediction
        blockFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            width=w,
            height=h,
            fg_color="transparent",
            bg_color="gray40",
        )
        blockFrame.place(anchor="nw", relx=x, rely=y)

        # save binary Data of image as an image named as PatientName.png
        self.db.write_file(scan, name)

        scanImage = f"Data/PatientScans/{name}.png"

        X_ray = ctk.CTkLabel(
            blockFrame,
            height=10,
            text="",
            image=ctk.CTkImage(Image.open(scanImage), size=(220, 220)),
            font=ctk.CTkFont(size=12, weight="bold"),
            bg_color="gray40",
        )
        X_ray.place(anchor="nw", relx=0.05, rely=0.05)
        X_ray.bind(
            "<Button-1>", lambda event: self.Zoom(event, scanImage)
        )  # When doctor click on the scan it will be opend in new window with size 720x720

        predictionLabel = ctk.CTkLabel(
            blockFrame,
            height=10,
            text=prediction,
            font=ctk.CTkFont(size=12, weight="bold"),
            bg_color="gray40",
        )
        predictionLabel.place(anchor="nw", relx=0.4, rely=0.93)

    def Zoom(self, event, name):
        # Create New Window
        ScanZoomWindow = ctk.CTkToplevel()
        PatientName = name.split("/")[-1].split(".")[
            0
        ]  # Get Patient Name from Image Name
        title = f"X-ray Scan of {PatientName}"
        ScanZoomWindow.title(title)
        # ScanZoomWindow.geometry("720x720")
        center(ScanZoomWindow, 720, 720)  # Open the window in the center of the Screen
        ScanZoomWindow.resizable(False, False)
        X_ray = ctk.CTkLabel(
            ScanZoomWindow,
            height=720,
            width=720,
            text="",
            image=ctk.CTkImage(Image.open(name), size=(720, 720)),
        )
        X_ray.place(anchor="nw", relx=0, rely=0)

    def SaveChat(self, id, chatqueue):
        c = list(chatqueue.queue)  # convert Queue to List
        textChat = "".join(c[i] if i == 0 else f"&,&{c[i]}" for i in range(len(c)))
        # Update the chat in database
        res = self.db.Update(
            "UPDATE chatdata SET Chat_Logs= %s WHERE Patient_ID= %s", [textChat, id]
        )
        self.db.Commit()

    def AddLoadedChat(self):
        # check that there is no items in LoaddedChat
        while self.LoaddedChat.qsize() > 0:
            msg = self.LoaddedChat.get()  # get chat data from the Queue
            self.ChatBlock(msg)  # add Chat to Chatbox

    def AddTochatBox(self, id):
        if not self.CurrentChat.empty():  # check if CurrentChat is not empty
            msg = self.CurrentChat.get()  # get the message
            self.ChatLOGS.put(msg)  # save the message in ChatLOGS
            self.SaveChat(id, self.ChatLOGS)  # update database with new chat data
            if msg != "":
                self.ChatBlock(msg)  # add Chat to Chatbox

        self.ChatFrame.after(
            1000, self.AddTochatBox, id
        )  # Repeat the function after 1000 ms

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

    def EndButtonEvent(self, event, id):
        if not self.ReportGenerated(id):
            list(
                map(
                    os.unlink,
                    (
                        os.path.join("Data/PatientScans/", f)
                        for f in os.listdir("Data/PatientScans/")
                    ),
                )
            )
            self.EndChat(id, "Close")
            res = self.user.updateBalance(
                self, 100
            )  # add Credits to the doctor When he ends the chat
            # update button Balance
            if res != -1:
                self._extracted_from_Withdraw_button_event_9(
                    "Credits added to your balance!"
                )
        else:
            MessageBox(self, "warning", "Report Should be Generated")

    def EndChat(self, id, EndType):
        if EndType == "Close":
            res1 = self.db.Update(
                "UPDATE requests SET Request_Status= %s WHERE Patient_ID= %s",
                ["Done", id],
            )
            res2 = self.db.Update(
                "UPDATE chatdata SET Chat_Status= %s WHERE Patient_ID= %s", ["Done", id]
            )
        if EndType == "Report":
            res1 = self.db.Update(
                "UPDATE requests SET Request_Status= %s WHERE Patient_ID= %s",
                ["Reported", id],
            )
            res2 = self.db.Update(
                "UPDATE chatdata SET Chat_Status= %s WHERE Patient_ID= %s",
                ["Reported", id],
            )
        self.db.Commit()
        self.LoadActiveChat()

    def ReportGenerated(self, id):
        res = self.db.Select("SELECT Report FROM chatdata WHERE Patient_ID= %s", [id])[
            0
        ][0]
        return len(res) != 0

    def ReportReasonBlock(self, event, name, id):
        # Create New Window
        ReportWindow = ctk.CTkToplevel()
        center(ReportWindow)  # Open the window in the center of the Screen
        title = f"Report {name}"
        ReportWindow.title(title)
        ReportWindow.geometry("400x200")
        ReportWindow.resizable(False, False)
        self.reasonEntry = ctk.CTkEntry(
            ReportWindow, width=270, placeholder_text="Enter Reason"
        )
        self.reasonEntry.place(anchor="nw", relx=0.15, rely=0.3)

        ConfirmButton = ctk.CTkButton(
            ReportWindow, text="Report", command=lambda: self.ReportEvent(id)
        )
        ConfirmButton.place(anchor="nw", relx=0.3, rely=0.6)

    def ReportEvent(self, id):
        Reason = self.reasonEntry.get()
        if len(Reason) == 0:
            return MessageBox(self, "error", "Reason Should not be empty")
        self.user.ReportUser(id, Reason)
        self.EndChat(id, "Report")
        res = self.user.updateBalance(self, 100)
        # update button Balance
        if res != -1:
            self.UpdateBalanceButton("User Reported Refund added to your balance")

    # End of Active Chat Section

    # Load LoadWaitingPatients Section
    def loadWaitingPatients(self):
        # Prevent Error for stucking in this frame and can not enter other Frames
        if self.Created[1]:
            self.PatientRequests_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent", width=1100, height=720
            )
            self.Created[1] = False
        # allways Clear the Frame to do the Update
        for widget in self.PatientRequests_frame.winfo_children():
            widget.destroy()
        HeaderLabel = ctk.CTkLabel(
            self.PatientRequests_frame,
            text="Available Patients",
            width=100,
            height=50,
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        HeaderLabel.place(anchor="nw", relx=0.35, rely=0)

        res = self.db.Select(
            "SELECT requests.Patient_ID, requests.Request_Date, users.Name, users.Gender, users.Age, users.Vip_Level FROM requests,users WHERE requests.Patient_ID LIKE users.ID AND requests.Request_Status = %s ORDER BY users.Vip_Level DESC, DATE (requests.Request_Date) ASC",
            ["waiting"],
        )
        # Scrollable frame that will hold all Available Patients with request status as waiting
        AvailablePatientsFrame = ScrollableFrame(
            self.PatientRequests_frame, "gray20", width=1070, height=650, scrollafter=5
        )
        AvailablePatientsFrame.place(anchor="nw", relx=0, rely=0.08)

        for i in range(len(res)):
            (
                Patient_ID,
                Patient_Req_Date,
                Patient_Name,
                Patient_Gender,
                Patient_Age,
                Patient_VIP,
            ) = self.FetchPatientData(res[i])
            patient_border = ctk.CTkFrame(
                AvailablePatientsFrame.scrollable_frame,
                corner_radius=0,
                fg_color="gray40",
                width=1070,
                height=100,
            )
            patient_border.grid(row=i, column=0, pady=6)

            if (
                Patient_Gender == "Male"
            ):  # check if the user is a Male to add Male image for him
                Image_label = ctk.CTkLabel(
                    patient_border,
                    image=ctk.CTkImage(MaleImage, size=(40, 40)),
                    text="",
                    width=100,
                    height=20,
                )
            else:  # check if the user is a Female to add Male image for him
                Image_label = ctk.CTkLabel(
                    patient_border,
                    image=ctk.CTkImage(FemaleImage, size=(40, 40)),
                    text="",
                    width=100,
                    height=20,
                )
            self.AddPatient(Patient_Name, patient_border, Image_label)

            if Patient_VIP == 1:
                VIP = ctk.CTkLabel(
                    patient_border,
                    image=ctk.CTkImage(bronze, size=(40, 40)),
                    text="",
                    width=100,
                    height=20,
                )
            elif Patient_VIP == 2:
                VIP = ctk.CTkLabel(
                    patient_border,
                    image=ctk.CTkImage(silver, size=(40, 40)),
                    text="",
                    width=100,
                    height=20,
                )
            elif Patient_VIP == 3:
                VIP = ctk.CTkLabel(
                    patient_border,
                    image=ctk.CTkImage(gold, size=(40, 40)),
                    text="",
                    width=100,
                    height=20,
                )
            else:
                VIP = ctk.CTkLabel(patient_border, text="", width=100, height=20)
            VIP.place(anchor="nw", relx=0.2, rely=0.25)

            GenderLabel = ctk.CTkLabel(
                patient_border,
                text=Patient_Gender,
                bg_color="transparent",
                fg_color="transparent",
                width=100,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            GenderLabel.place(anchor="nw", relx=0.3, rely=0.35)

            AgeLabel = ctk.CTkLabel(
                patient_border,
                text=Patient_Age,
                bg_color="transparent",
                fg_color="transparent",
                width=100,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            AgeLabel.place(anchor="nw", relx=0.5, rely=0.35)

            ReqDateLabel = ctk.CTkLabel(
                patient_border,
                text=Patient_Req_Date,
                bg_color="transparent",
                fg_color="transparent",
                width=100,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            ReqDateLabel.place(anchor="nw", relx=0.7, rely=0.35)

            AcceptButton = ctk.CTkButton(
                patient_border,
                text="Chat",
                bg_color="gray50",
                fg_color="transparent",
                corner_radius=0,
                width=100,
                height=20,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=lambda m=Patient_ID: self.AssignPatient(m),
            )
            AcceptButton.place(anchor="nw", relx=0.88, rely=0.35)

    def AddPatient(self, Patient_Name, patient_border, Image_label):
        Image_label.place(anchor="nw", relx=0, rely=0.25)

        NameLabel = ctk.CTkLabel(
            patient_border,
            text=Patient_Name,
            bg_color="transparent",
            fg_color="transparent",
            width=100,
            height=20,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        NameLabel.place(anchor="nw", relx=0.1, rely=0.35)

    def AssignPatient(self, id):
        # UPDATE requests SET Request_Status = "waiting"
        self.db.Update(
            "UPDATE requests SET Request_Status = %s WHERE Patient_ID= %s",
            ["ongoing", id],
        )
        self.db.Insert(
            "INSERT INTO chatdata (Patient_ID, Doc_ID, Chat_Status) Values (%s,%s,%s)",
            [id, self.user.userid, "ongoing"],
        )
        self.loadWaitingPatients()
        self.db.Commit()

    # End of LoadWaitingPatients Section

    # Credits section
    def loadCreditWithdraw(self):

        # Prevent Error for stucking in this frame and can not enter other Frames
        if self.Created[2]:
            self.credits_frame = ctk.CTkFrame(
                self, corner_radius=0, fg_color="transparent"
            )
            self.Created[2] = False

        # Remove card type|Specific amount entry in each start for frame as user may nav to other Frames and want to go back to this frame
        self.delType()
        self.RemoveAmount("")

        # Credit Card Section
        self.CreditCardBlock()

        # entering withdraw balance
        self.WithdrawBlock()

    def delType(self):
        # Try to handle error if any type was not shown so it will throw an error
        with contextlib.suppress(NameError, AttributeError):
            self.Americanlabel.destroy()
        with contextlib.suppress(NameError, AttributeError):
            self.Visalabel.destroy()
        with contextlib.suppress(NameError, AttributeError):
            self.Masterlabel.destroy()

    def CreditCardBlock(self):
        self.CardChecked = False
        self.InformationLabel = ctk.CTkLabel(
            self.credits_frame,
            text="Credit Card Information",
            width=60,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.InformationLabel.place(anchor="nw", relx=0.4, rely=0.05)

        self.CardNumber = ctk.CTkEntry(
            self.credits_frame,
            placeholder_text="Credit Card Number",
            width=160,
            font=ctk.CTkFont(size=14),
        )  # 5471462613718519
        self.CardNumber.place(anchor="nw", relx=0.05, rely=0.25)
        self.CardNumber.bind(
            "<Leave>", self.CardNumberValidation
        )  # Handle all functions will be applied for card number + validation

        self.CVV = ctk.CTkEntry(
            self.credits_frame,
            show="*",
            placeholder_text="CVV",
            width=42,
            font=ctk.CTkFont(size=14),
        )
        self.CVV.place(anchor="nw", relx=0.35, rely=0.25)
        self.CVV.bind("<Leave>", self.HandleCVV)

        self.ExpireMonth = ctk.CTkComboBox(
            self.credits_frame,
            width=60,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        )
        self.ExpireMonth.place(anchor="nw", relx=0.55, rely=0.25)

        self.slashLabel = ctk.CTkLabel(
            self.credits_frame, text="/", width=20, font=ctk.CTkFont(size=14)
        )
        self.slashLabel.place(anchor="nw", relx=0.615, rely=0.25)

        self.ExpireYear = ctk.CTkComboBox(
            self.credits_frame,
            width=60,
            values=["21", "22", "23", "24", "25", "26", "27"],
        )
        self.ExpireYear.place(anchor="nw", relx=0.64, rely=0.25)

        self.CheckCard = ctk.CTkButton(
            self.credits_frame,
            text="Check Card Expiration",
            anchor="w",
            fg_color="gray50",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.CheckCard_button_event,
        )
        self.CheckCard.place(anchor="nw", relx=0.74, rely=0.25)

    def CardNumberValidation(self, event):
        if (
            len(self.CardNumber.get()) != 16 or self.CardNumber.get().isalpha()
        ):  # 5471462613718519
            self.CardChecked = False
            return MessageBox(self, "warning", "Credit Card is not 16 digit")
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
                self.Americanlabel.place(anchor="nw", relx=0.318, rely=0.25)
            elif int(string[0]) == 4:
                self.Visalabel = ctk.CTkLabel(
                    self.credits_frame,
                    text="",
                    image=ctk.CTkImage(visa, size=(25, 25)),
                )
                self.Visalabel.place(anchor="nw", relx=0.2, rely=0.25)
            elif int(string[0]) == 5:
                self.Masterlabel = ctk.CTkLabel(
                    self.credits_frame,
                    text="",
                    image=ctk.CTkImage(mastercard, size=(25, 25)),
                )
                self.Masterlabel.place(anchor="nw", relx=0.2, rely=0.25)

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
            MessageBox(self, "warning", "CVV is not 3 digit")
        else:
            self.CardChecked = True

    def WithdrawBlock(self):
        self.WithdrawLabel = ctk.CTkLabel(
            self.credits_frame,
            text="Withdraw Credits",
            width=60,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.WithdrawLabel.place(anchor="nw", relx=0.4, rely=0.45)

        self.QuickSelectionsFrame = ctk.CTkFrame(
            self.credits_frame, corner_radius=0, fg_color="gray30", width=350
        )
        self.QuickSelectionsFrame.place(anchor="nw", relx=0.05, rely=0.65)

        self.Label = ctk.CTkLabel(
            self.QuickSelectionsFrame, text="Select Credits:", font=ctk.CTkFont(size=14)
        )
        self.Label.place(anchor="w", relx=0.41, rely=0.1)

        self.image = ctk.CTkLabel(
            self.QuickSelectionsFrame,
            text="",
            image=ctk.CTkImage(cashlvl3, size=(100, 100)),
        )
        self.image.place(anchor="w", relx=0.61, rely=0.5)

        self.credit_val = tk.IntVar(value=0)

        self.selec1 = self.AddOption(
            self.QuickSelectionsFrame, 0.1, 0.18, self.credit_val, "5", 5
        )
        self.selec2 = self.AddOption(
            self.QuickSelectionsFrame, 0.1, 0.36, self.credit_val, "50", 50
        )
        self.selec3 = self.AddOption(
            self.QuickSelectionsFrame, 0.1, 0.54, self.credit_val, "500", 500
        )
        self.selec4 = self.AddOption(
            self.QuickSelectionsFrame, 0.1, 0.72, self.credit_val, "5000", 5000
        )
        self.selec5 = self.AddOption(
            self.QuickSelectionsFrame, 0.1, 0.9, self.credit_val, "Other", -1, False
        )

        self.Withdraw_Button = ctk.CTkButton(
            self.credits_frame,
            text="Withdraw",
            anchor="w",
            fg_color="gray50",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.Withdraw_button_event,
        )
        self.Withdraw_Button.place(anchor="nw", relx=0.66, rely=0.8)

    def AddOption(self, master, x, y, vari, txt, val, fun=True):
        option = ctk.CTkRadioButton(master, variable=vari, text=txt, value=val)
        option.place(anchor="w", relx=x, rely=y)
        if fun:
            option.bind("<Button-1>", self.RemoveAmount)  # Remove Entry Frame if found
        else:
            option.bind("<Button-1>", self.HandleAmount)  # Show Entry Frame if found
        return option

    def HandleAmount(self, event):
        if self.Created[3]:
            self.AmountFrame = ctk.CTkFrame(
                self.credits_frame, corner_radius=0, fg_color="gray30", width=150
            )
            self.Created[3] = False
        self.AmountFrame.place(anchor="nw", relx=0.38, rely=0.65)

        self.clabel = ctk.CTkLabel(
            self.AmountFrame, text="Enter Credits:", font=ctk.CTkFont(size=14)
        )
        self.clabel.place(anchor="w", relx=0.2, rely=0.1)

        self.Amount = ctk.CTkEntry(
            self.AmountFrame,
            placeholder_text="Amount",
            width=100,
            font=ctk.CTkFont(size=14),
        )  # 5471462613718519
        self.Amount.place(anchor="w", relx=0.2, rely=0.5)

    def RemoveAmount(self, event):
        with contextlib.suppress(Exception):
            for widget in self.AmountFrame.winfo_children():
                widget.destroy()
            self.AmountFrame.destroy()
            self.Created[3] = True

    def CheckCard_button_event(self):
        Year = f"20{self.ExpireYear.get()}"
        print(Year, self.ExpireMonth.get(), date.today().month, date.today().year)
        if int(Year) < date.today().year:
            self.CardChecked = False
            return MessageBox(self, "error", "Credit Card Expired")
        if (
            int(self.ExpireMonth.get()) < date.today().month
            and int(Year) == date.today().year
        ):
            self.CardChecked = False
            return MessageBox(self, "error", "Credit Card Expired")
        else:
            self.CardChecked = True

    def Withdraw_button_event(self):
        if self.CardChecked == False:  #
            MessageBox(self, "error", "Credit Card is not checked")
        else:
            if int(self.credit_val.get()) == -1:
                if (
                    self.Amount.get() == ""
                    or self.Amount.get().isalpha()
                    or int(self.Amount.get()) <= 0
                ):
                    return MessageBox(self, "error", "Invalid Amount")
                else:
                    Amount = int(self.Amount.get()) * -1
            else:
                Amount = int(self.credit_val.get()) * -1
            res = self.user.updateBalance(self, Amount)
            # update button Balance
            if res != -1:
                self.UpdateBalanceButton(
                    "Credits will be added to you bank account Soon!"
                )

    def UpdateBalanceButton(self, arg0):
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
        self.Credits_button.grid(row=6, column=0, sticky="ew")
        MessageBox(self, "info", arg0)

    # Other functions
    def FetchPatientData(self, data):
        for j in range(len(data)):
            yield data[j]

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.Active_Chats_button.configure(
            fg_color=("gray75", "gray25") if name == "Active_Chats" else "transparent"
        )
        self.PatientRequests_button.configure(
            fg_color=("gray75", "gray25")
            if name == "PatientRequests"
            else "transparent"
        )
        self.Credits_button.configure(
            fg_color=("gray75", "gray25") if name == "Credits" else "transparent"
        )

        # show selected frame
        if name == "Active_Chats":
            self.Active_Chats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.Active_Chats_frame.grid_forget()

        if name == "PatientRequests":
            self.PatientRequests_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.PatientRequests_frame.grid_forget()

        if name == "Credits":
            self.credits_frame.grid(row=0, column=1, sticky="nsew")
        else:
            with contextlib.suppress(Exception):
                self.credits_frame.grid_forget()

    def Active_Chats_button_event(self):
        self.LoadActiveChat()
        self.select_frame_by_name("Active_Chats")

    def PatientRequests_button_event(self):
        self.loadWaitingPatients()
        self.select_frame_by_name("PatientRequests")

    def Credits_button_event(self):
        self.loadCreditWithdraw()
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
