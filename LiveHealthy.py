# Imports
import contextlib
import csv
import os
import os.path
import queue
import re
import shutil
import smtplib
import socket
import ssl
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from random import shuffle
from threading import Timer
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *

import customtkinter as ctk
import cv2
import fpdf
import mysql.connector
import numpy as np
import openai
import tensorflow
from keras import Model, utils
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from keras.layers import (Activation, Add, BatchNormalization, Conv2D, Dense,
                          Flatten, GlobalAveragePooling2D, Input, Lambda)
from keras.models import load_model
from keras.optimizers import SGD, schedules
from PIL import Image, ImageTk
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tkcalendar import Calendar

# System Images Load
logo = Image.open("asset\Logo.png")


LoginBG = Image.open("asset/login.jpg")
LoginBG2 = Image.open("asset/login2.jpg")

RegisterBG = Image.open("asset/RegBG.jpg")



logout = Image.open("asset\logout.png")


# Male and Female Images
MaleImage = Image.open("asset\Male.png")
FemaleImage = Image.open("asset\Female.png")
AdministratorImage = Image.open("asset\\administrator.png")

ChatMaleImage = Image.open("asset\ChatMale.png")
ChatFemaleImage = Image.open("asset\ChatFemale.png")


# Doctor GUI Left side bar Images
ActiveChats = Image.open("asset\ActiveChats.png")
Chat = Image.open("asset\Chat.png")
coin = Image.open("asset\coin.png")
consultation = Image.open("asset\consultation.png")

# Money Images
cashlvl1 = Image.open("asset\cashlvl1.png")
cashlvl2 = Image.open("asset\cashlvl2.png")
cashlvl3 = Image.open("asset\cashlvl3.png")
dollar = Image.open("asset\dollar-symbol.png")

# Credit Card Images
americanexpress = Image.open("asset\\americanexpress.png")
visa = Image.open("asset\\visa.png")
mastercard = Image.open("asset\\mastercard.png")

# VIP Images
gold = Image.open("asset\\gold-medal.png")
silver = Image.open("asset\\silver-medal.png")
bronze = Image.open("asset\\bronze-medal.png")
EndDate = Image.open("asset\\hourglass.png")

# Generate Prescription for Patient
GeneratePrescription = Image.open("asset\GenerateReport.png")
Prescriptions = Image.open("asset\clipboard.png")
pdflogo = Image.open("asset\pdf.png")

AddIcon = Image.open("asset\\add.png")

DeleteIcon = Image.open("asset\\trash.png")

# Report User
ReportUser = Image.open("asset\ReportUser.png")

# Close|End Chat
CloseDoctorChat = Image.open("asset\CloseChat.png")

# Send Icon for Chatbox
sendICON = Image.open("asset\send.png")

# Predict X-ray scan
predict_image = Image.open("asset\predict.png")

# Purchase VIP
PurchaseVIP = Image.open("asset\\vip.png")
PurchaseVIPLogo = Image.open("asset\\vip1.png")

Discount = Image.open("asset\\discount.png")
FifteenPercent = Image.open("asset\\fifteen.png")
FiftyPercent = Image.open("asset\\50.png")
HundredPercent = Image.open("asset\\100.png")
calendar = Image.open("asset\\calendar.png")


# Administrator Section
VerifyDoctor = Image.open("asset\\VerifyDoctor.png")
HandleReports = Image.open("asset\\HandleReports.png")
Adminchat = Image.open("asset\\Adminchat.png")
Verify = Image.open("asset\\checked.png")
Ban = Image.open("asset\\forbidden.png")

# ConfigFile
def SystemConfig():
    return {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "Systemdb",
        "IMAGE_SIZE": 224,
        "ClassLabels": 6,
        "FramesSizeWidth": 1280,
        "FramesSizeHeight": 720,
        "UserImageSize": 100,
        "ButtonIconsSize": 50,
        "MessageBoxSize": "500x150",
        "ServerAddress": "127.0.0.1",
        "ServerPort": 4073,
        "BackgroundColor":"#6883bc",
        "FrameColor":"#1e2761",
        "TextColor":"#f3ca20" 
    }
# Database
class Database:
    # Database connection String
    configfile = SystemConfig()

    __instance = None
    
    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    @staticmethod
    def OnlineDB():
        configfile = SystemConfig()
        try:
            mydb = mysql.connector.connect(
                host=configfile.get("host"),
                user=configfile.get("user"),
                password=configfile.get("password"),
                database=configfile.get("database"),
            )
            mycursor = mydb.cursor()
            return 1
        except Exception:
            return -100

    def __init__(self):
        if Database.__instance is None:
            Database.__instance = self
            self.Connect()

    def Connect(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.configfile.get("host"),
                user=self.configfile.get("user"),
                password=self.configfile.get("password"),
                database=self.configfile.get("database"),
            )
            self.mycursor = self.mydb.cursor()
        except Exception:
            return -100

    def Update(self, Query, Values):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()
        

    def Select(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        data = self.mycursor.fetchall()
        self.mycursor.close()
        return data

    def Insert(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()

    def Delete(self, Query, Values=None):
        if Values is None:
            Values = []
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(Query, Values)
        self.mycursor.close()

    def Commit(self):
        self.mydb.commit()
def UpdateQuery(Query, Values):
    db = Database.getInstance()
    db.Update(Query, Values)
    db.Commit()

def SelectQuery(Query, Values=None):
    db = Database.getInstance()
    res = db.Select(Query, Values)
    return res

def InsertQuery(Query, Values=None):
    db = Database.getInstance()
    db.Insert(Query, Values)
    db.Commit()

def DeleteQuery(Query, Values=None):
    db = Database.getInstance()
    db.Delete(Query, Values)
    db.Commit()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
        with open(filename, "wb") as file:
            file.write(data)
        file.close()

# Client Side
class Client:
    # format for messages
    FORMAT = "utf-8"
    HOST = "127.0.0.1"
    PORT = 4073

    # creating a socket for client
    # initializing
    # name of a client, chanel , client adress
    def __init__(self, name, addr, chnl):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.channel = chnl
        self.clientsocket.connect(addr)

    # function for sending messages to a server
    def writeToServer(self, userInput=None):
        # name input
        if userInput is not None:
            message = f"{self.name}: {userInput}"

            # send name to server
            self.clientsocket.send(message.encode(self.FORMAT))

    def receiveFromServer(self, q):
        while True:
            try:
                # recieve a message from server
                message = self.clientsocket.recv(1024).decode(self.FORMAT)

                # if the message contains a keyword "+getName+Channel", send name and channel to server
                if message == "getData":
                    self.clientsocket.send(
                        f"{self.name}&,&{self.channel}".encode(self.FORMAT)
                    )
                elif message != "Please enter message" or message != "":
                    q.put(message)
            except Exception:
                self.end()
                break

    def end(self):
        self.clientsocket.close()

# DataSet
class Dataset:
    def loadDataset(self):  # load the gray data that was read before and labeled
        return np.load("Data/DatasetGray.npy", allow_pickle=True)  # load dataset

    def saveDataset(
        self, path, data
    ):  # save the data of images with labels to be used later
        np.save(path, data)

    def loadTrainData(self):
        if os.path.exists("Data/x_train.npy"):
            images = np.load("Data/x_train.npy", allow_pickle=True)
        if os.path.exists("Data/y_train.npy"):
            labels = np.load("Data/y_train.npy", allow_pickle=True)
        return images, labels

    def loadTestData(self):
        if os.path.exists("Data/x_test.npy"):
            images = np.load("Data/x_test.npy", allow_pickle=True)
        if os.path.exists("Data/y_test.npy"):
            labels = np.load("Data/y_test.npy", allow_pickle=True)
        return images, labels

    def CreateValidData(self):
        x_train, y_train = self.loadTrainData()
        x_train, x_valid, y_train, y_valid = train_test_split(
            x_train, y_train, test_size=0.2
        )
        return x_train, x_valid, y_train, y_valid

# ImageProcessing Class
class ImageProcessing:

    # load config dict
    config = SystemConfig()
    # Class Variables
    Dataset = None  # Variable that will hold whole dataset images and its label

    root_folder = "Data/Dataset/"  # Directory path for folders that contains images
    IMAGE_SIZE = config.get("IMAGE_SIZE")  # Image size height and width

    def GenerateDataSet(self):
        dsM = Dataset()
        data = None
        if os.path.exists(
            "Data/DatasetGray.npy"
        ):  # If you have already created the dataset:
            data = dsM.loadDataset()
        else:  # If dataset is not created:
            folders = [
                os.path.join(self.root_folder, x)
                for x in (
                    "COVID/train/",
                    "Fibrosis/train/",
                    "Normal/train/",
                    "Tuberculosis/train/",
                    "PNEUMONIA/train/",
                )
            ]  # create a list contains all sub folders in our root
            data = [
                img
                for folder in folders
                for img in self.load_images_from_folder(folder)
            ]  # get images in each subfolder
            shuffle(data)  # shuffle arrangement of dataset
            dsM.saveDataset(
                "Data/DatasetGray.npy", data
            )  # Save dataset to be easily used later
        images = np.array(
            [i[0] for i in data]
        )  # holds the images from dataset into this variable
        labels = [
            i[1] for i in data
        ]  # holds the labels for each image into this variable
        labels = keras.utils.to_categorical(
            labels, self.config.get("ClassLabels")
        )  # Converts a class vector (integers) to binary class matrix for example COVID = 1 => [0. 1. 0. 0. 0. 0.]
        return images, labels

    def load_images_from_folder(self, folder):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, filename), 0)
            if img is not None:
                img = cv2.resize(img, (self.IMAGE_SIZE, self.IMAGE_SIZE))
                images.append([np.array(img), self.create_label(folder, filename)])
        return images

    def create_label(self, filename, imagename):
        # Normal = 0
        # COVID = 1
        # Bacterial PNEUMONIA = 2
        # Viral PNEUMONIA = 3
        # Fibrosis = 4
        # Tuberculosis = 5
        # set label for each disease to labels in previous lines
        label = "None"
        if "PNEUMONIA" in filename:  # check if folder name contains PNEUMONIA
            if "bacteria" in imagename:  # check if image name contains bacteria
                label = 2
            elif "virus" in imagename:  # check if image name contains virus
                label = 3
        elif "COVID" in filename:  # check if folder name contains COVID
            label = 1
        elif "Fibrosis" in filename:  # check if folder name contains Fibrosis
            label = 4
        elif "Normal" in filename:  # check if folder name contains Normal
            label = 0
        elif "Tuberculosis" in filename:  # check if folder name contains Tuberculosis
            label = 5
        return label

    def load_image(self, filepath):
        img = cv2.imread(filepath, 0)
        img = cv2.resize(img, (self.IMAGE_SIZE, self.IMAGE_SIZE))
        return [np.array(img)]

# HelperFunctions
def MessageBox(parent, type, Text):

    if type == "error":
        messagebox.showerror("Error", Text, icon="error", parent=parent)
    elif type == "info":
        messagebox.showinfo("Info", Text, icon="info", parent=parent)
    elif type == "question":
        messagebox.askyesno("Question", Text, icon="question", parent=parent)
    elif type == "warning":
        messagebox.showwarning("Warning", Text, icon="warning", parent=parent)


# function to let any window be in the center of the screen
def center(win, w, h):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    win.iconbitmap(default="asset\TitleImage.ico",)


# Error ConfigFile
def SystemErrors():
    return {
        1: "Please fill all fields!",
        2: "Invalid Name!",
        3: "Invalid email address!",
        4: "Your radiology center has reached its maximum amount of users!",
        5: "Invalid radiology center code!",
        6: "Password Mismatch!",
        7: "Password should be longer than 8 characters!",
        8: "Invalid phone number!",
        9: "Please select your gender",
        10: "Please enter your university",
        11: "Please check your ID",
        12: "Please check your Profession License",
        13: "Please check your ID and Profession License",
        14: "Please enter your email address",
        15: "Please wait until you are verified",
        16:"Credit Card Expired",
        17:"Credit Card is not checked",
        18:"Invalid Amount",
        19:"Reason Should not be empty",
        20:"No Medicine to be added to Prescription",
        21:"Medicine Name cannot be empty",
        22:"Symptoms can not be empty",
        23:"Illness Time can not be empty",
        24:"Medications can not be empty",
        25:"No Credit Card details found",
        26:"You are suspended",
        27:"Please chat first with our assistant",
        28:"Database is not Connected",
        29:"Chat Server is offline",
        30:"Please Enter a valid email address and password",
    }


# Model Config
def model_configuration():
    # Dataset size
    dsM = Dataset()
    x_train, x_valid, y_train, y_valid = dsM.CreateValidData()
    train_size = len(y_train)
    val_size = len(y_valid)

    # Generic config
    width, height, channels = 224, 224, 1
    batch_size = 128
    num_classes = 6
    verbose = 1
    n = 3
    init_fm_dim = 16

    shortcut_type = "identity"

    # Number of steps per epoch is dependent on batch size
    maximum_number_iterations = 64000  # per the He et al. paper
    steps_per_epoch = tensorflow.math.floor(
        train_size / batch_size
    )  # calculating Number of steps per epoch
    val_steps_per_epoch = tensorflow.math.floor(val_size / batch_size)
    epochs = tensorflow.cast(
        tensorflow.math.floor(maximum_number_iterations / steps_per_epoch),
        dtype=tensorflow.int64,
    )

    # Define loss function
    loss = tensorflow.keras.losses.CategoricalCrossentropy(from_logits=True)

    # Learning rate config per the He et al. paper
    boundaries = [32000, 48000]
    values = [0.1, 0.01, 0.001]
    lr_schedule = schedules.PiecewiseConstantDecay(boundaries, values)

    # Set layer init
    initializer = tensorflow.keras.initializers.HeNormal()

    # Define optimizer
    optimizer_momentum = 0.9
    optimizer_additional_metrics = ["accuracy"]
    optimizer = SGD(learning_rate=lr_schedule, momentum=optimizer_momentum)

    # Load Tensorboard callback
    # tensorboard = TensorBoard(
    #     log_dir=os.path.join(os.getcwd(), "logs"), histogram_freq=1, write_images=True
    # )

    # Save a model checkpoint after every epoch
    checkpoint = ModelCheckpoint(
        "Data/ResNet.h5", monitor="val_accuracy", verbose=1, save_best_only=True
    )
    early = EarlyStopping(monitor="val_accuracy", min_delta=0, patience=30, verbose=1)

    # Add callbacks to list
    callbacks =  [checkpoint, early] #[tensorboard, checkpoint, early]

    return {
        "width": width,
        "height": height,
        "dim": channels,
        "batch_size": batch_size,
        "num_classes": num_classes,
        "verbose": verbose,
        "stack_n": n,
        "initial_num_feature_maps": init_fm_dim,
        "training_ds_size": train_size,
        "steps_per_epoch": steps_per_epoch,
        "val_steps_per_epoch": val_steps_per_epoch,
        "num_epochs": epochs,
        "loss": loss,
        "optim": optimizer,
        "optim_learning_rate_schedule": lr_schedule,
        "optim_momentum": optimizer_momentum,
        "optim_additional_metrics": optimizer_additional_metrics,
        "initializer": initializer,
        "callbacks": callbacks,
        "shortcut_type": shortcut_type,
    }

# Model
class ResNetModel:
    def residual_block(self, x, number_of_filters, match_filter_size=False):
        """
        Residual block with
        """
        # Retrieve initializer
        config = model_configuration()
        initializer = config.get("initializer")

        # Create skip connection
        x_skip = x

        # Perform the original mapping
        if match_filter_size:
            x = Conv2D(
                number_of_filters,
                kernel_size=(3, 3),
                strides=(2, 2),
                kernel_initializer=initializer,
                padding="same",
            )(x_skip)
        else:
            x = Conv2D(
                number_of_filters,
                kernel_size=(3, 3),
                strides=(1, 1),
                kernel_initializer=initializer,
                padding="same",
            )(x_skip)
        x = BatchNormalization(axis=3)(x)
        x = Activation("relu")(x)
        x = Conv2D(
            number_of_filters,
            kernel_size=(3, 3),
            kernel_initializer=initializer,
            padding="same",
        )(x)
        x = BatchNormalization(axis=3)(x)

        # Perform matching of filter numbers if necessary
        if match_filter_size and config.get("shortcut_type") == "identity":
            x_skip = Lambda(
                lambda x: tensorflow.pad(
                    x[:, ::2, ::2, :],
                    tensorflow.constant(
                        [
                            [
                                0,
                                0,
                            ],
                            [0, 0],
                            [0, 0],
                            [number_of_filters // 4, number_of_filters // 4],
                        ]
                    ),
                    mode="CONSTANT",
                )
            )(x_skip)

        # Add the skip connection to the regular mapping
        x = Add()([x, x_skip])

        # Nonlinearly activate the result
        x = Activation("relu")(x)

        # Return the result
        return x

    def ResidualBlocks(self, x):
        """
        Set up the residual blocks.
        """
        # Retrieve values
        config = model_configuration()

        # Set initial filter size
        filter_size = config.get("initial_num_feature_maps")

        # Paper: "Then we use a stack of 6n layers (...)
        # 	with 2n layers for each feature map size."
        # 6n/2n = 3, so there are always 3 groups.
        for layer_group in range(3):

            # Each block in our code has 2 weighted layers,
            # and each group has 2n such blocks,
            # so 2n/2 = n blocks per group.
            for block in range(config.get("stack_n")):

                # Perform filter size increase at every
                # first layer in the 2nd block onwards.
                # Apply Conv block for projecting the skip
                # connection.
                if layer_group > 0 and block == 0:
                    filter_size *= 2
                    x = self.residual_block(x, filter_size, match_filter_size=True)
                else:
                    x = self.residual_block(x, filter_size)
        # Return final layer
        return x

    def model_base(self, shp):
        """
        Base structure of the model, with residual blocks
        attached.
        """
        # Get number of classes from model configuration
        config = model_configuration()
        initializer = model_configuration().get("initializer")

        # Define model structure
        # logits are returned because Softmax is pushed to loss function.
        inputs = Input(shape=shp)
        x = Conv2D(
            config.get("initial_num_feature_maps"),
            kernel_size=(3, 3),
            strides=(1, 1),
            kernel_initializer=initializer,
            padding="same",
        )(inputs)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = self.ResidualBlocks(x)
        x = GlobalAveragePooling2D()(x)
        x = Flatten()(x)
        outputs = Dense(config.get("num_classes"), kernel_initializer=initializer)(x)

        return inputs, outputs

    def init_model(self):
        """
        Initialize a compiled ResNet model.
        """
        # Get shape from model configuration
        config = model_configuration()

        # Get model base
        inputs, outputs = self.model_base(
            (config.get("width"), config.get("height"), config.get("dim"))
        )

        # Initialize and compile model
        model = Model(inputs, outputs, name=config.get("name"))
        model.compile(
            loss=config.get("loss"),
            optimizer=config.get("optim"),
            metrics=config.get("optim_additional_metrics"),
        )
        return model

    def train_model(self, model, x_train, x_valid, y_train, y_valid):
        """
        Train an initialized model.
        """

        # Get model configuration
        config = model_configuration()

        # Fit data to model
        model.fit(
            x_train,
            y_train,
            batch_size=config.get("batch_size"),
            epochs=config.get("num_epochs"),
            verbose=config.get("verbose"),
            callbacks=config.get("callbacks"),
            steps_per_epoch=config.get("steps_per_epoch"),
            validation_data=(x_valid, y_valid),
            validation_steps=config.get("val_steps_per_epoch"),
        )

        return model

    def evaluate_model(self, model, xtest, ytest):
        """
        Evaluate a trained model.
        """
        # Evaluate model
        score = model.evaluate(xtest, ytest, verbose=1)
        print(f"Test loss: {score[0]} / Test accuracy: {score[1]}")

    def training_process(self, ev=False):
        # load test and train data
        dsM = Dataset()
        x_test, y_test = dsM.loadTestData()
        x_train, x_valid, y_train, y_valid = dsM.CreateValidData()
        resnet = self.init_model()
        trained_resnet = self.train_model(resnet, x_train, x_valid, y_train, y_valid)
        if ev:
            self.evaluate_model(trained_resnet, x_test, y_test)
        return trained_resnet

    def PredictScan(self, Scanpath, OneValue = False):
        import tensorflow
        IP = ImageProcessing()
        if os.path.exists(resource_path("Data/ResNet.h5")):
            trained_resnet = load_model(resource_path("Data/ResNet.h5"))
        else:
            trained_resnet = self.training_process()
        img = IP.load_image(Scanpath)
        img = np.array(img)
        x = trained_resnet.predict(img,verbose=0)
        percentage_list = []
        classes = [
            "Normal",
            "Covid-19",
            "Bacterial PNEUMONIA",
            "Viral PNEUMONIA",
            "Fibrosis",
            "Tuberculosis",
        ]
        for i in range(len(x[0])):
            normalized = (x[0][i] - min(x[0])) / (max(x[0]) - min(x[0]))
            percentage_list.append("{0:.2%}".format(normalized))
            li = list(zip(classes, percentage_list))

        if not OneValue:
            return li
        
        max1 = 0
        for i in li:
            value = float(i[1].split("%")[0])
            if value > max1:
                max1 = value
                res= i[0]
        return res

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Threading With return value
class ReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result

# Users Class
class User:

    # --------------------------------VARIABLES SECTION----------------------------------------------#
    db = Database()  # Create connection with Database to access it
    systemError = SystemErrors()
    # --------------------------------END OF VARIABLES SECTION------------------------------------------#

    # --------------------------------FUNCTIONS SECTION-------------------------------------------------#
    def __init__(self, id):
        # constructor Used during Login to get user id
        self.userid = id
        res = SelectQuery("SELECT * FROM users WHERE ID= %s", [self.userid]) 
        (self.userName,
        self.userMail,
        self.userPassword,
        self.userType,
        self.userBalance,
        self.userPhone,
        self.userAge,
        self.userSystemApperanceMode,
        self.userGender,
        self.userVIPLevel,
        self.userVIPEnd) = self.fillindata(res[0],[0])

    def GetMaxID(self):
        return SelectQuery("SELECT MAX(ID) FROM users")[0][0]

    def CalcAge(self, Birthdate):
        return (
            date.today().year
            - Birthdate.year
            - (
                (date.today().month, date.today().day)
                < (Birthdate.month, Birthdate.day)
            )
        )

    @classmethod
    def CreateUser(cls, name, Mail, Password, Utype, Phone, Age, Gender):

        cls.userid = cls.GetMaxID(cls) + 1 
        cls.userName = name
        cls.userMail = Mail
        cls.userPassword = Password
        cls.userType = Utype
        cls.userPhone = Phone
        cls.userAge = Age
        cls.userGender = Gender
        cls.userSystemApperanceMode = "Light"
        cls.userBalance = 0
        cls.userVIPLevel = 0
        cls.userVIPEnd = date(2001, 1, 1)
        return cls
    
    @classmethod
    def Login(cls, email, password):
        res = cls.db.Select(
            "SELECT ID, Account_Type FROM users WHERE Mail LIKE %s AND Password=%s", [email, password]
        )
        if len(res) == 0:
            messagebox.showerror("Error", cls.systemError.get(30), icon="error")
        cls.userid = res[0][0]
        cls.userType = res[0][1]
        return cls.userid, cls.userType

    def Logout(self,frame):
        from Starter import Starter
        frame.destroy()
        app = Starter()
        app.mainloop()

    def SaveData(self):
        InsertQuery(
            "INSERT INTO users (ID, Name, Mail, Password, Account_Type, Credits_Balance, Phone, DateOfBirth, Apperance_Mode, Gender, Vip_Level, Vip_End_Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                self.userName,
                self.userMail,
                self.userPassword,
                self.userType,
                self.userBalance,
                self.userPhone,
                self.userAge,
                self.userSystemApperanceMode,
                self.userGender,
                self.userVIPLevel,
                self.userVIPEnd
            ]
        )

    def fillindata(self, input, skipValues=None):
        if skipValues is None:
            skipValues = []
        for i in range(len(input)):
            if i in skipValues:
                continue
            else:
                yield input[i]

    def updateBalance(self, parent, val):
        if val < 0:
            check = val * (-1)
            if check > self.userBalance:
                MessageBox(parent, "error", "Insufficient Funds")
                return -1
        elif val == 0:
            MessageBox(parent, "error", "Invalid Amount")
            return -1
        self.userBalance += val
        UpdateQuery(
            "UPDATE users SET Credits_Balance = %s WHERE ID= %s",
            [self.userBalance, self.userid],
        )

    def SetApperanceMode(self, mode):
        self.userSystemApperanceMode = mode
        UpdateQuery(
            "UPDATE users SET Apperance_Mode = %s WHERE ID= %s",
            [mode, self.userid],
        )

class Patient(User):

    db = Database()  # Create connection with Database to access it
    systemError = SystemErrors()

    BasePredictScanPrice = 75
    BaseChatPrice = 150

    def __init__(self, id):
        if id != -1:
            super().__init__(id)
            res= SelectQuery("SELECT * FROM patienthealthstatus WHERE Patient_ID= %s",[self.userid])
            (
                self.Heart_Diseases,
                self.Diabetes,
                self.Cancer,
                self.Obesity,
                self.Smoker,
                self.Hypertension,
                self.Allergies,
                self.Blood_Type,
                ) = self.fillindata(res[0], [0])

    def SaveData(self):
        super().SaveData()
        InsertQuery(
            "INSERT INTO patienthealthstatus (Patient_ID, Heart_Diseases, Diabetes, Cancer, Obesity, Smoker, Hypertension, Allergies, Blood_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                self.Heart_Diseases,
                self.Diabetes,
                self.Cancer,
                self.Obesity,
                self.Smoker,
                self.Hypertension,
                self.Allergies,
                self.Blood_Type,
            ])
    
    @classmethod
    def CreatePatient(cls, name, Mail, Password, Utype, Phone, Age, Gender, HD = 0, diabetes = 0, cancer = 0, obesity = 0, smoker = 0, hypertension = 0, Allergies = 0, BloodType = "UNKNOWN"):
        p = cls(-1)
        p.userid = p.GetMaxID() + 1
        p.userName = name
        p.userMail = Mail
        p.userPassword = Password
        p.userType = Utype
        p.userPhone = Phone
        p.userAge = Age
        p.userGender = Gender
        p.userSystemApperanceMode = "System"
        p.userBalance = 0
        p.userVIPLevel = 0
        p.userVIPEnd = date(2001, 1, 1)
        p.Heart_Diseases = HD
        p.Diabetes = diabetes
        p.Cancer = cancer
        p.Obesity = obesity
        p.Smoker = smoker
        p.Hypertension = hypertension
        p.Allergies = Allergies
        p.Blood_Type = BloodType
        return p

    def checkRequest(self):
        res = SelectQuery("SELECT * FROM requests WHERE Patient_ID= %s", [self.userid])
        return len(res) > 0

    def CreateRequest(self, ScanPath, prediction, Chatlog):
        binaryimage = convertToBinaryData(ScanPath) if ScanPath != "" else ""
        RequestDate = date.today()
        InsertQuery(
            "INSERT INTO requests (Patient_ID, Request_Date, Request_Status, X_ray_scan, Prediction, BotChat) VALUES (%s, %s, %s, %s, %s, %s)",
            [
                self.userid,
                RequestDate,
                "waiting",
                binaryimage,
                prediction,
                Chatlog
            ],
        )

    def RequestData(self):
        res = SelectQuery(
            "SELECT X_ray_scan, Prediction, BotChat FROM requests WHERE Patient_ID= %s",
            [self.userid],
        )
        return res[0]

    def PredictMyScan(self, ScanPath, SaveType):
        m = ResNetModel()
        if SaveType == "Two":
            prediction = m.PredictScan(ScanPath)
            self.max1 = -99
            self.max2 = -98
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

            if self.max1 < self.max2:
                temp = self.max1
                temptext = self.p1
                self.max1 = self.max2
                self.p1 = self.p2
                self.p2 = temptext
                self.max2=temp

            Label1 = f"{self.p1} ➜ {self.max1}%"
            Label2 = f"{self.p2} ➜ {self.max2}%"
            return Label1, Label2
        elif SaveType == "One":
            prediction = m.PredictScan(ScanPath, True)
            return prediction

    def SavePrediction(self, Scanpath):
        newpath = Scanpath.split(".")[0]
        newpath = f"{newpath}.txt"
        with open(newpath, "w") as f:
            f.write(f"Highest Class Percentage: {self.p1} --> {self.max1}% \n")
            f.write(f"Second Class Percentage: {self.p2} --> {self.max2}%")
        messagebox.showinfo("Info","Text File saved successfully")

    def PriceInfo(self, ContextType):
        if ContextType =="Chat":
            if self.userVIPLevel == 1:
                Credits = self.GetDiscount(self.BaseChatPrice, 15)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
            elif self.userVIPLevel == 2:
                Credits = self.GetDiscount(self.BaseChatPrice, 50)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
            elif self.userVIPLevel == 3:
                Credits = self.GetDiscount(self.BaseChatPrice, 100)
                Infotext = "Chat with our doctors is Free"
            else:
                Credits = self.GetDiscount(self.BaseChatPrice, 0)
                Infotext = f"You are going to pay {Credits} credit to chat with our doctors"
        else:
            if self.userVIPLevel == 1:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 15)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
            elif self.userVIPLevel == 2:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 50)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
            elif self.userVIPLevel == 3:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 100)
                Infotext = "X-ray Scan prediction is Free"
            else:
                Credits = self.GetDiscount(self.BasePredictScanPrice, 0)
                Infotext = f"You are going to pay {Credits} credit to predict your X-ray Scan"
        return Infotext, Credits

    def GetDiscount(self, value, percentage):
        return int(value - (value * (percentage/100)))

    def Subscribe(self, button, master, LeftSideBar):
        if button == "bronze":
            level = 1
            value = -100
        elif button == "silver":
            level = 2
            value = -190
        elif button == "gold":  
            level = 3
            value = -350
        res = self.updateBalance(master, value)
        if res != -1:
            if self.userVIPEnd < date.today():
                self.userVIPEnd = date.today() + timedelta(days=30)
            else:
                self.userVIPEnd += timedelta(days=30)
            self.userVIPLevel = level
            UpdateQuery("UPDATE users SET Vip_Level= %s, Vip_End_Date= %s WHERE ID = %s",[self.userVIPLevel, self.userVIPEnd, self.userid])
            LeftSideBar() # Update Left Side bar in GUI passed as a function
            MessageBox(master,"info","Purchase Complete")

    def Purchase(self, button, master, LeftSideBar, CardChecked):
        if CardChecked == False:  #
            messagebox.showerror("Error", self.systemError.get(17), icon="error", parent=master)
        else:
            if button == "1":
                value = 100
            elif button == "2":
                value = 200
            elif button == "3":  
                value = 400
            res = self.updateBalance(master, value)
            if res != -1:
                LeftSideBar() # Update Left Side bar in GUI passed as a function
                MessageBox(master,"info","Balance Recharge Completed")

    def MyPrescriptions(self):
        return SelectQuery("SELECT Doc_ID, prescriptionDate, prescriptionPDF FROM prescriptions WHERE Patient_ID = %s ORDER BY prescriptionDate DESC",[self.userid]) 

    def DownloadPrescription(self, event, presDate, presPDF, master):
        SavePath = filedialog.askdirectory(title="Select Where to Download Prescription")
        FullPathName = f"{SavePath}/Prescription_{presDate}.pdf"
        write_file(presPDF, FullPathName)
        subprocess.Popen([FullPathName], shell=True)  # Show the Prescription for the patient
        return MessageBox(master,"info","Prescription saved successfully")

class Doctor(User):

    def __init__(self, id):
        if id != -1:
            super().__init__(id)
            res = SelectQuery(
                "SELECT * FROM doctordata WHERE Doctor_ID= %s", [self.userid]
            )
            (
                self.Verified,
                self.University,
                self.ID_Card,
                self.Prof_License,
            ) = self.fillindata(res[0], [0])

    def SaveData(self):
        super().SaveData()
        InsertQuery(
            "INSERT INTO doctordata (Doctor_ID, Verified, University, ID_Card, Prof_License) VALUES (%s, %s, %s, %s, %s)",
            [
                self.userid,
                self.Verified,
                self.University,
                self.ID_Card,
                self.Prof_License,
            ],
        )

    @classmethod
    def CreateDoctor(
        cls,
        name,
        Mail,
        Password,
        Utype,
        Phone,
        Age,
        Gender,
        University,
        ID_Card,
        Prof_License,
        Verified=0,
    ):
        d = cls(-1)
        d.userid = d.GetMaxID() + 1
        d.userName = name
        d.userMail = Mail
        d.userPassword = Password
        d.userType = Utype
        d.userPhone = Phone
        d.userAge = Age
        d.userGender = Gender
        d.userSystemApperanceMode = "System"
        d.userBalance = 0
        d.userVIPLevel = 0
        d.userVIPEnd = date(2001, 1, 1)
        d.Verified = Verified
        d.University = University
        d.ID_Card = ID_Card
        d.Prof_License = Prof_License
        return d

    def ReportUser(self, userID, Reason):
        ReportDate = date.today()
        InsertQuery(
            "INSERT INTO reports (Issuer_ID, Reporter_ID, Reason, ReportDate) VALUES (%s, %s, %s, %s)",
            [userID, self.userid, Reason, ReportDate],
        )
        InsertQuery(
            "INSERT INTO suspended (User_ID, Suspention_Type, Suspention_Date, Reason) VALUES (%s, %s, %s, %s)",
            [userID, "temp", ReportDate, Reason],
        )

    def GetMyChatMembers(self):
        return SelectQuery(
            "SELECT Patient_ID FROM chatdata WHERE Chat_Status = %s and Doc_ID = %s",
            ["ongoing", self.userid],
        )

    def HandlePrescription(self, event, id, FillMedication):
        patient = User(id)
        path = f"Data\Prescriptions\{patient.userName}.pdf"
        if not self.PrescriptionGenerated(id):
            subprocess.Popen([path], shell=True)  # Show the Prescription for the Doctor
        else:
            FillMedication

    def MakePrescription(self, id, Medicine, MedicineComment):
        patient = User(id)
        res = SelectQuery(
            "SELECT X_ray_scan, Prediction FROM requests WHERE Patient_ID= %s",
            [id],
        )
        pdf = fpdf()
        pdf.add_page()
        pdf.set_font("Times", size=15)

        # Add MainPage Style
        pdf.image("asset\\report.png", x=0, y=0, w=219, h=300, type="PNG")

        # Add Doctor information
        pdf.set_xy(20, 45)
        DoctorName = f"Doctor {self.userName}"
        pdf.cell(180, 10, txt=DoctorName, ln=1, align="C")
        Doctortitle = (
            f"{self.userType} in Department of Respiratory Diseases at Live Healthy"
        )
        pdf.set_xy(20, 55)
        pdf.cell(180, 10, txt=Doctortitle, ln=0, align="C")

        # Add Patient information
        Name = f"Name: {patient.userName}"
        pdf.set_xy(10, 70)
        pdf.cell(200, 10, txt=Name, ln=1, align="L")

        Age = f"Age: {str(patient.CalcAge(patient.userAge))}"
        pdf.set_xy(10, 80)
        pdf.cell(200, 10, txt=Age, ln=2, align="L")

        Gender = f"Gender: {patient.userGender}"
        pdf.set_xy(40, 80)
        pdf.cell(200, 10, txt=Gender, ln=2, align="L")

        Date = f"Date: {date.today().day}/{date.today().month}/{date.today().year}"
        pdf.set_xy(85, 80)
        pdf.cell(180, 10, txt=Date, ln=2, align="L")

        Prediction = f"Prediction: {res[0][1]}"
        pdf.set_xy(130, 80)
        pdf.cell(180, 10, txt=Prediction, ln=1, align="L")

        pdf.set_xy(15, 85)
        pdf.cell(
            180,
            10,
            txt="_________________________________________________________________",
            ln=1,
            align="L",
        )

        pdf.set_xy(10, 100)
        # Medicine Section
        for pos, item in enumerate(Medicine):
            pdf.set_font("Times", size=14)
            Med = f"R/ {item}"
            pdf.cell(180, 10, txt=Med, ln=2, align="L")
            pdf.cell(180, 10, txt=MedicineComment[pos], ln=2, align="C")
        file = f"Data\Prescriptions\{patient.userName}.pdf"
        pdf.output(file)
        binaryFile = convertToBinaryData(file)
        UpdateQuery(
            "UPDATE prescriptions SET prescriptionPDF= %s, prescriptionDate = %s Where Patient_ID= %s",
            [binaryFile, date.today(), patient.userid],
        )

    def PrescriptionGenerated(self, id):
        res = SelectQuery("SELECT prescriptions.prescriptionPDF FROM prescriptions, chatdata WHERE prescriptions.Patient_ID= %s AND prescriptions.Doc_ID= %s AND DATE(prescriptions.prescriptionDate) >= DATE(chatdata.StartDate)",[id, self.userid])
        return len(res) != 0

    def EndChat(self, id, EndType):
        EndDate = date.today() 
        res = SelectQuery("SELECT Chat_Logs, StartDate FROM chatdata WHERE Patient_ID= %s",[id])
        InsertQuery("INSERT INTO oldchat (Patient_ID, Doc_ID, ChatLOGS, StartDate, EndDate, EndType) VALUES (%s, %s, %s, %s, %s, %s)",[id, self.userid, res[0][0], res[0][1], EndDate, EndType])
        DeleteQuery("DELETE FROM chatdata WHERE Patient_ID= %s",[id])
        DeleteQuery("DELETE FROM requests WHERE Patient_ID= %s",[id])

    def LoadWaitingPatientRequests(self):
        return SelectQuery(
            "SELECT requests.Patient_ID, requests.Request_Date, users.Name, users.Gender, users.DateOfBirth, users.Vip_Level FROM users, requests where users.ID = requests.Patient_ID and requests.Request_Status = %s ORDER BY users.Vip_Level DESC, DATE (requests.Request_Date) ASC",
            ["waiting"],
        )

    def AssignMePatient(self, id):
        # UPDATE requests SET Request_Status = "waiting"
        UpdateQuery(
            "UPDATE requests SET Request_Status = %s WHERE Patient_ID= %s",
            ["ongoing", id],
        )
        InsertQuery(
            "INSERT INTO chatdata (Patient_ID, Doc_ID, Chat_Status, StartDate) Values (%s,%s,%s,%s)",
            [id, self.userid, "ongoing", date.today()],
        )
        InsertQuery(
            "INSERT INTO prescriptions (Patient_ID, Doc_ID) Values (%s,%s)",
            [id, self.userid],
        )

class Radiologist(User):

    db = Database()  # Create connection with Database to access it

    def __init__(self, id):
        if id != -1:
            super().__init__(id)
            radiodata = SelectQuery("SELECT Center_ID FROM radiologists WHERE Radiologist_ID= %s",[self.userid], )[0][0]  # get the id for Radiology center
            self.CenterName = SelectQuery("SELECT Name FROM radiologycenters WHERE ID= %s", [radiodata])[0][0] 

    def SaveData(self):
        super().SaveData()
        centerID = SelectQuery("SELECT ID FROM radiologycenters WHERE Name LIKE %s", [self.CenterName])[0][0] 
        InsertQuery(
            "INSERT INTO radiologists (Radiologist_ID, Center_ID) VALUES (%s, %s)",
            [
                self.userid,
                centerID,
            ])
    
    @classmethod
    def CreateRadiologist(cls, name, Mail, Password, Utype, Phone, Age, Gender, CenterName):
        r = cls(-1)
        r.userid = r.GetMaxID() + 1 
        r.userName = name
        r.userMail = Mail
        r.userPassword = Password
        r.userType = Utype
        r.userPhone = Phone
        r.userAge = Age
        r.userGender = Gender
        r.userSystemApperanceMode = "System"
        r.userBalance = 0
        r.userVIPLevel = 0
        r.userVIPEnd = date(2001, 1, 1)
        r.CenterName = CenterName
        return r
    

    def PredictScanFolder(self, FolderPath):
        output = []
        m = ResNetModel()
        valid_images = [".jpg",".gif",".png",".tga",".jpeg"]
        for f in os.listdir(FolderPath):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            FullPath = os.path.join(FolderPath,f)
            imageName= os.path.splitext(f)[0]
            output.append((imageName, m.PredictScan(FullPath,True)))
        return output

    # Generate Excel file
    def createcsv(self, Path, out):
        loc = f"{Path}/Predictions.csv"
        with open(loc, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(out)

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
        MessageBox(master,"info","Suspension revoked for the patient")

    def ConfirmSuspension(self, master, id, update):
        DeleteQuery("DELETE FROM reports WHERE Issuer_ID = %s",[id])
        UpdateQuery("UPDATE suspended SET Suspention_Type= %s WHERE User_ID= %s",["Permanent",id])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been permanently suspended")
        update()
        MessageBox(master,"info","Patient permanently suspended")

    def getUnverifiedDoctors(self):
        return SelectQuery("SELECT doctordata.Doctor_ID, users.Name, doctordata.University, doctordata.ID_Card, doctordata.Prof_License FROM doctordata,users WHERE doctordata.Doctor_ID = users.ID AND doctordata.Verified =%s ORDER BY doctordata.Doctor_ID ASC",[0])

    def VerifyDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[1, id])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been verified successfully")
        update()
        MessageBox(master,"info","Doctor Verified")

    def BanDoctor(self, event, master, id, update):
        UpdateQuery("UPDATE doctordata SET Verified= %s WHERE Doctor_ID= %s",[-1, id])
        InsertQuery("INSERT INTO suspended (User_ID, Suspention_Type, Suspention_Date, Reason) VALUES (%s, %s, %s, %s)",[id, "Permanent",date.today(),"Register With Fake ID and License",])
        Mail = self.GetMail(id)
        self.SendMail(Mail, "Account Activation", "Your account has been suspended")
        update()
        MessageBox(master,"info","Doctor Suspended")

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

# User Factory
class UserFactory:
    @staticmethod
    def createUser(id, Type):
        
        if Type.lower() == "patient":
            from Patient import Patient
            return Patient(id)
        elif Type.lower() in ["doctor", "specialist", "consultant"]:
            from Doctor import Doctor
            return Doctor(id)
        elif Type.lower() == "radiologist":
            from Radiologist import Radiologist
            return Radiologist(id)
        elif Type.lower() == "admin":
            from Administrator import Administrator
            return Administrator(id)

# Starter Page
class Starter(ctk.CTk):
    # load Config dict
    config = SystemConfig()
    MovetoReg = False
    Moveto = False
    systemError = SystemErrors()
    def __init__(self):
        super().__init__()
        self.WindowSettings()
        self.login_gui()
        # Enter all your buttons,Entries here

    def WindowSettings(self):
        Title = "Welcome to Live Healthy"
        self.title(Title)

        # set Dimension of GUI
        center(
            self,
            self.config.get("FramesSizeWidth"),
            self.config.get("FramesSizeHeight"),
        )  # Get Frame size from config File and center the window
        self.resizable(False, False)

    def login_gui(self):
        self.backgroundFrame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            width=1255,
            height=710,
        )
        self.backgroundFrame.place(anchor="nw", relx=0.01, rely=0.011)


        
        bgImage = ctk.CTkLabel(self.backgroundFrame, text="", image=ctk.CTkImage(LoginBG, size=(1255, 710)))
        bgImage.place(anchor="nw", relx=0, rely=0)
        self.subbg = ctk.CTkFrame(
            self.backgroundFrame,
            fg_color="#F0F0F0",
            width=1230,
            height=694,
        )
        self.subbg.place(anchor="nw", relx=0.008, rely=0.01)

        logoImage = ctk.CTkLabel(self.backgroundFrame, text="", image=ctk.CTkImage(
            logo, size=(65, 65)), bg_color='#f0fafb', fg_color="#f0fafb")
        logoImage.place(anchor="nw", relx=0.018, rely=0.020)
        bgImage2 = ctk.CTkLabel(self.subbg, text="", image=ctk.CTkImage(
            LoginBG2, size=(1230, 694)))
        bgImage2.place(anchor="nw", relx=0, rely=0)


        self.SelectionFrame = ctk.CTkFrame(
            self.subbg,
            fg_color="#FFFAFA",
            width=1230,
            height=650,
        )
        self.SelectionFrame.place(anchor="nw", relx=0.5, rely=0.05)

        self.segbutton = ctk.CTkSegmentedButton(self.subbg,values=["Login","Sign Up"], command=self.ShowFrame)
        self.segbutton.place(anchor="nw", relx=0.7, rely=0.03)
        self.segbutton.set("Login")
        self.ShowLoginFrame()

    def ShowFrame(self, selection):
        with contextlib.suppress(Exception):
            for widget in self.SelectionFrame.winfo_children():
                widget.destroy()
        if selection == "Login":
            loginTimer= Timer(0.2, self.ShowLoginFrame) 
            loginTimer.start()
        else:
            RegisterTimer= Timer(0.2, self.mainRegister) 
            RegisterTimer.start()

    def ShowLoginFrame(self):
        welcomeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Welcome Back",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=40, weight='bold', slant='italic', family="Times New Roman")
        )
        welcomeLabel.place(anchor="nw", relx=0.06, rely=0.2)
        loginLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Login your account",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, family="Times New Roman")
        )
        loginLabel.place(anchor="nw", relx=0.061, rely=0.268)
        emailLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Email:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
        )
        emailLabel.place(anchor="nw", relx=0.045, rely=0.4)
        self.emailEntry = ctk.CTkEntry(
            self.SelectionFrame,
            placeholder_text="Your email...",
            fg_color="white",
            text_color="black",
            width=490,
            height=45,
        )
        self.emailEntry.place(anchor="nw", relx=0.061, rely=0.46)
        passwordLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Password:",
            text_color="#000000",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20, weight="bold", family="Times New Roman")
        )
        passwordLabel.place(anchor="nw", relx=0.061, rely=0.59)
        self.passwordEntry = ctk.CTkEntry(
            self.SelectionFrame,
            placeholder_text="Your password...",
            fg_color="white",
            text_color="black",
            width=490,
            height=45,
            bg_color="transparent",
            show="*"
        )
        self.passwordEntry.place(anchor="nw", relx=0.061, rely=0.65)
        forgotpassLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Forgot Password?",
            text_color="#808080",
            width=100,
            height=25,
            font=ctk.CTkFont(size=15, family="Aerial 18", underline=True),
            cursor="hand2",
        )
        forgotpassLabel.bind('<Button-1>', self.forgot_password)
        forgotpassLabel.place(anchor="nw", relx=0.065, rely=0.725)
        self.LoginButton = ctk.CTkButton(self.SelectionFrame,text="Login", width= 170, height=50,corner_radius=30,font=ctk.CTkFont(size=18, family="Aerial 18",weight='bold'), command=self.login_verify)
        self.LoginButton.place(anchor="nw", relx=0.061, rely=0.8)

    def login_verify(self):
        from User import User
        self.email = self.emailEntry.get()
        self.password = self.passwordEntry.get()
        if len(self.email) == 0 or len(self.password) == 0:
            return messagebox.showerror("Error", self.systemError.get(1), icon="error", parent=self.SelectionFrame)
        userinfo = User.Login(self.email, self.password)
        suspended = self.suspended(userinfo[0])
        if suspended != -1:
            return messagebox.showerror("Error", self.systemError.get(suspended), icon="error", parent=self.SelectionFrame)
        if userinfo != "ok":
            if userinfo[1] in ["Specialist","Consultant"]:
                res = SelectQuery("SELECT Verified FROM doctordata WHERE Doctor_ID=%s",[userinfo[0]])[0][0]
                if res == 0:
                    return messagebox.showerror("Error", self.systemError.get(15), icon="error", parent=self.SelectionFrame)
            self.MoveTo(userinfo)

    def forgot_password(self, event):
        mail = self.emailEntry.get()
        if len(mail) == 0:
            return messagebox.showerror("Error", self.systemError.get(14), icon="error", parent=self.SelectionFrame)

        password = SelectQuery("SELECT Password FROM users WHERE Mail LIKE %s",[mail])
        if len(password) == 0:
            return messagebox.showerror("Error", self.systemError.get(3), icon="error", parent=self.SelectionFrame)
        password = password[0][0]

        # Define email sender and receiver
        email_sender = 'livehealthy171@gmail.com'
        email_password = 'gowdfobqansntowb'
        email_receiver = mail

        # Set the subject and body of the email
        subject = 'Your Account Password'
        body = f"Here is your account password: {password}"

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
        messagebox.showinfo("Success", "Email Sent")

    def suspended(self, id):
        res = SelectQuery("SELECT COUNT(*) FROM suspended WHERE User_ID = %s",[id])[0][0]
        return 26 if res == 1 else -1

    # Start of Register Part 
    def mainRegister(self):
        FullNameLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Full Name*",
            fg_color="transparent",
            bg_color="transparent",
            text_color="black",
            width=100,
            height=25,
            font=ctk.CTkFont(size=20),
        )
        FullNameLabel.place(anchor="nw", relx=0.015, rely=0.06)

        self.FullNameEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Full Name...",
        border_color="black",
        text_color="black",
        placeholder_text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        width=250,
        height=35,
        )
        self.FullNameEntry.place(anchor="nw",relx=0.015,rely=0.10)

        MailLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Email*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        MailLabel.place(anchor="nw", relx=0.25, rely=0.06)

        self.MailEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Email...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.MailEntry.place(anchor="nw",relx=0.25,rely=0.10)



        PassLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PassLabel.place(anchor="nw",relx=0.015, rely=0.17)

        self.PassEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Password...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.PassEntry.place(anchor="nw",relx=0.015,rely=0.21)

        ConfirmPassLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Confirm Password*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        ConfirmPassLabel.place(anchor="nw",relx=0.25, rely=0.17)

        self.ConfirmPassEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Confirm Your Password...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35,
        show="*"
        )
        self.ConfirmPassEntry.place(anchor="nw",relx=0.25,rely=0.21)

        PhoneLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Phone Number*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        PhoneLabel.place(anchor="nw",relx=0.015, rely=0.28)

        self.PhoneEntry = ctk.CTkEntry(
        self.SelectionFrame,
        placeholder_text="Input Your Phone Number...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        placeholder_text_color="black",
        width=250,
        height=35
        )
        self.PhoneEntry.place(anchor="nw",relx=0.015,rely=0.32)

        

        AgeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Date of Birth*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        AgeLabel.place(anchor="nw",relx=0.25, rely=0.28)
        self.cal = Calendar(self.SelectionFrame,
        selectmode = 'day',
        year = 2001,
        month = 1,
        day = 1)
        self.cal.place(anchor="nw", relx=0.25,rely=0.32)


        GenderLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="Gender*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        GenderLabel.place(anchor="nw",relx=0.015, rely=0.39)

        self.GenderVar = tk.IntVar(value = -1)
        MaleRadio = ctk.CTkRadioButton(
            self.SelectionFrame,
            text="Male",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=1
        )
        MaleRadio.place(anchor="nw",relx=0.015, rely=0.45)
        FemaleRadio = ctk.CTkRadioButton(
            self.SelectionFrame,
            text="Female",
            text_color="black",
            hover_color="black",
            variable=self.GenderVar,
            value=2
        )
        FemaleRadio.place(anchor="nw",relx=0.1, rely=0.45)



        TypeLabel = ctk.CTkLabel(
            self.SelectionFrame,
            text="User Type*",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        TypeLabel.place(anchor="nw",relx=0.015, rely=0.5)

        self.TypeCombo = ctk.CTkOptionMenu(self.SelectionFrame,
        width=250,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Patient", "Radiologist", "Consultant", "Specialist"],
        command=self.UserType
        )
        self.TypeCombo.place(anchor="nw",relx=0.015, rely=0.55)
        self.patient()
        self.Registerbutton()

    def UserType(self, Utype):
        if Utype=="Patient":
            self.patient()
            self.Registerbutton()
        elif Utype in ["Consultant", "Specialist"]:
            self.doctor()
            self.Registerbutton()
        elif Utype=="Radiologist":
            self.radiologist()
            self.Registerbutton()

    def HoldFrame(self):
        with contextlib.suppress(Exception):
            self.Secondframe.destroy()

        self.Secondframe = ctk.CTkFrame(
            self.SelectionFrame,
            fg_color="transparent",
            width=520,
            height=300
        )
        self.Secondframe.place(anchor="nw",relx=0.015, rely=0.61)

    def patient(self):
        self.HoldFrame()
        HealthLabel = ctk.CTkLabel(
            self.Secondframe,
            text="Patient's Health Status",
            text_color="black",
            font=ctk.CTkFont(size=30),
        )
        HealthLabel.place(anchor="nw",relx=0.2, rely=0.04)
        self.patientsHealthCheck()

    def patientsHealthCheck (self):
        self.PatientHealthFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=520,
            height=300
        )
        self.PatientHealthFrame.place(anchor="nw",relx=0, rely=0.2)

        self.Heart = IntVar()
        HeartCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Heart Diseases",
            text_color="black",
            width=260,
            variable=self.Heart,
            onvalue=1,
            offvalue=0
        )
        HeartCheck.grid(row=1,column=0, pady=5)

        self.Diabetes = IntVar()
        DiabetesCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Diabetes",
            text_color="black",
            width=260,
            variable=self.Diabetes,
            onvalue=1,
            offvalue=0
        )
        DiabetesCheck.grid(row=1,column=1, pady=5)

        
        self.Cancer = IntVar()
        CancerCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Cancer",
            text_color="black",
            width=260,
            variable=self.Cancer,
            onvalue=1,
            offvalue=0
        )
        CancerCheck.grid(row=2,column=0, pady=5)

        self.Obesity = IntVar()
        ObesityCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Obesity",
            text_color="black",
            width=260,
            variable=self.Obesity,
            onvalue=1,
            offvalue=0
        )
        ObesityCheck.grid(row=2,column=1, pady=5)


        self.Smoker = IntVar()
        SmokerCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Smoker",
            text_color="black",
            width=260,
            variable=self.Smoker,
            onvalue=1,
            offvalue=0
        )
        SmokerCheck.grid(row=3,column=0, pady=5)

        self.Hypertension = IntVar()
        HypertensionCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Hypertension",
            text_color="black",
            width=260,
            variable=self.Hypertension,
            onvalue=1,
            offvalue=0
        )
        HypertensionCheck.grid(row=3,column=1, pady=5)

        self.Allergies = IntVar()
        AllergiesCheck = ctk.CTkCheckBox(
            self.PatientHealthFrame,
            text="Allergies",
            text_color="black",
            width=260,
            variable=self.Allergies,
            onvalue=1,
            offvalue=0
        )
        AllergiesCheck.grid(row=4,column=0, pady=5)

        BloodTypeLabel = ctk.CTkLabel(
            self.Secondframe,
            text="Blood Type:",
            text_color="black",
            height=25,
            font=ctk.CTkFont(size=14),
        )
        BloodTypeLabel.place(anchor="nw", relx=0.01, rely=0.7)

        self.BloodTypeCombo = ctk.CTkOptionMenu(
        self.Secondframe,
        width=100,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=["Unknown","O-","O+","B-","B+","A-","A+","AB-","AB+"],
        font = ctk.CTkFont(size =17)
        )
        self.BloodTypeCombo.place(anchor="nw", relx=0.186, rely=0.7)

    def doctor(self):
        self.HoldFrame()
        self.DoctorFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=600,
            height=580
        )
        self.DoctorFrame.place(anchor="nw",relx=0, rely=0)

        self.ImageFrame = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="transparent",
            fg_color="transparent",
            border_color="black",
            width=150,
            height=100
        )
        self.ImageFrame.place(anchor="nw",relx=0, rely=0.01)

        self.ImageFrame2 = ctk.CTkFrame(
            self.DoctorFrame,
            bg_color="transparent",
            fg_color="transparent",
            width=150,
            height=100
        )
        self.ImageFrame2.place(anchor="nw",relx=0.4, rely=0.01)

        ImportIDButton = ctk.CTkButton(self.DoctorFrame,text="Import ID", command=self.ImportID,width=50)
        ImportIDButton.place(anchor="nw", relx=0.26, rely=0.08)

        ImportLicenseButton = ctk.CTkButton(self.DoctorFrame,text="Import Prof. License", command=self.ImportLicense,width=100)
        ImportLicenseButton.place(anchor="nw", relx=0.653, rely=0.08)

        UniLabel = ctk.CTkLabel(
            self.DoctorFrame,
            text="University:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        UniLabel.place(anchor="nw",relx=0, rely=0.2)
        self.UniEntry = ctk.CTkEntry(
        self.DoctorFrame,
        placeholder_text="Input The University You Graduated From...",
        placeholder_text_color="black",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        width=300,
        height=30
        )
        self.UniEntry.place(anchor="nw",relx=0.2,rely=0.2)

    IDPath = ""
    def ImportID(self):
        self.IDPath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        IDImage = ctk.CTkLabel(self.ImageFrame,text="",image=ctk.CTkImage(Image.open(self.IDPath),size=(150,100)))
        IDImage.place(anchor="nw", relx=0, rely=0)

    LicensePath = ""
    def ImportLicense(self):
        self.LicensePath = askopenfilename(filetypes=(("Image File", ["*.png","*.jpg","*.jpeg"]),))
        LicenseImage = ctk.CTkLabel(self.ImageFrame2,text="",image=ctk.CTkImage(Image.open(self.LicensePath),size=(150,100)))
        LicenseImage.place(anchor="nw", relx=0, rely=0)

    def radiologist(self):
        self.HoldFrame()
        RadiologistFrame = ctk.CTkFrame(
            self.Secondframe,
            fg_color="transparent",
            width=600,
            height=580
        )
        RadiologistFrame.place(anchor="nw",relx=0, rely=0)

        RadioCenterLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Radiology Center:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        RadioCenterLabel.place(anchor="nw",relx=0, rely=0.05)

        res = SelectQuery("SELECT Name FROM radiologycenters")
        RadioCenters = [i[0] for i in res]
        self.RadioCenterCombo = ctk.CTkOptionMenu(
        RadiologistFrame,
        width=330,
        dropdown_text_color="#DCD427",
        dropdown_hover_color="#969696",
        values=RadioCenters,
        font=ctk.CTkFont(size = 20),
        )
        self.RadioCenterCombo.place(anchor="nw",relx=0.3, rely=0.05)

        RadioCenterCodeLabel = ctk.CTkLabel(
            RadiologistFrame,
            text="Center Verification Code:",
            text_color="black",
            width=65,
            height=20,
            font=ctk.CTkFont(size=20),
        )
        RadioCenterCodeLabel.place(anchor="nw",relx=0, rely=0.12)

        self.RadioCenterCodeEntry = ctk.CTkEntry(
        RadiologistFrame,
        placeholder_text="Input Your Center's Verification Code...",
        text_color="black",
        fg_color="transparent",
        bg_color="transparent",
        border_color="black",
        width=400,
        height=35
        )
        self.RadioCenterCodeEntry.place(anchor="nw",relx=0.2,rely=0.17)

    def Registerbutton(self,):
        RegisterButton = ctk.CTkButton(
        self.SelectionFrame,
        bg_color="#b3c7e5",
        text="Register",
        width= 150,
        height=80,
        font = ctk.CTkFont(size=23),
        command=self.fetchAllData
        )
        RegisterButton.place(anchor="nw", relx=0.35, rely=0.87)

    def fetchAllData(self):
        self.userName = self.FullNameEntry.get()
        self.Email = self.MailEntry.get()
        self.Phone = self.PhoneEntry.get()
        self.Password = self.PassEntry.get()
        self.ConfirmPassword = self.ConfirmPassEntry.get()
        self.DoB = datetime.strptime(self.cal.get_date(), '%m/%d/%y').date()
        self.Gender = "Male" if self.GenderVar.get() == 1 else "Female"
        self.UsType = self.TypeCombo.get()
        CheckData = self.dataValidator()
        
        if CheckData != -1:
            return messagebox.showerror("Error", self.systemError.get(CheckData), icon="error", parent=self.backgroundFrame)
        else:
            self.insertUserInfo()

    def dataValidator(self):  
        EmptyFields = self.emptyMainFields()
        if EmptyFields != -1:
            return EmptyFields
        
        ValidName = self.userNameChecker()
        
        if ValidName != -1:
            return ValidName
        
        if self.emailChecker():
            return 3
        
        PasswordValid = self.passwordChecker()
        if PasswordValid != -1:
            return PasswordValid
        
        PhoneValid = self.phoneChecker()
        if PhoneValid != -1:
            return PhoneValid
        
        genvalid = self.genderValid()
        if genvalid != -1:
            return genvalid
        
        AllVaild = self.fetchUserTypeData()
        if AllVaild != -1:
            return AllVaild
        
        return -1

    def emptyMainFields(self):
        if self.FullNameEntry.get() == "" or self.Phone == "" or self.Email == "" or self.Password == "" or self.ConfirmPassword == "" or self.Gender == 0:
            return 1
        else:
            return -1

    def userNameChecker(self):
        pattern = re.compile("^[a-zA-Z ]*$")
        return -1 if pattern.fullmatch(self.userName) is not None else 2
    
    def emailChecker(self):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        return not re.match(pat,self.Email)
    
    def passwordChecker(self):
        if self.Password != self.ConfirmPassword:
            return 6
        elif len(self.Password) < 8:
            return 7
        else:
            return -1
    
    def phoneChecker(self):
        if (not self.Phone.isnumeric()) or (len(self.Phone) < 11 or len(self.Phone) > 15):
            return 8
        else:
            return -1

    def genderValid(self):
        return 9 if self.GenderVar.get() == -1 else -1

    def CheckRadioCenter(self):
        res = SelectQuery("SELECT Registercode, Center_Limit FROM radiologycenters WHERE Name=%s",[self.radioCenter])
        limit = res[0][1]
        code = res[0][0]
        if self.radioCenterCode == code and limit > 0:
            limit -= 1
            UpdateQuery("UPDATE radiologycenters SET Center_Limit=%s WHERE Name=%s",[limit,self.radioCenter])
        if limit == 0:
            self.Valid = False
            return 4
        if self.radioCenterCode != code:
            self.Valid = False
            return 5
        return -1

    def fetchUserTypeData(self):
        # Function that fetches the user type data in SecondFrame
        if self.TypeCombo.get() == "Patient":
            self.heart = self.Heart.get()
            self.diabetes = self.Diabetes.get()
            self.cancer = self.Cancer.get()
            self.obesity = self.Obesity.get()
            self.smoker = self.Smoker.get()
            self.hypertension = self.Hypertension.get()
            self.allergies = self.Allergies.get()
            self.Blood = self.BloodTypeCombo.get()

        if self.TypeCombo.get() == "Radiologist":
            self.radioCenter = self.RadioCenterCombo.get()
            self.radioCenterCode = self.RadioCenterCodeEntry.get()
            RadiologyCenterVaild = self.CheckRadioCenter()
            if RadiologyCenterVaild != -1:
                return RadiologyCenterVaild

        if self.TypeCombo.get() in ["Specialist", "Consultant"]:
            if len(self.IDPath) == 0 and len(self.LicensePath) == 0: 
                return 13
            if len(self.IDPath) == 0:
                return 11
            if len(self.LicensePath) == 0:
                return 12
                
            if self.UniEntry.get() == "" :
                return 10
            self.uni = self.UniEntry.get()
            self.IDbinary = convertToBinaryData(self.IDPath)
            self.LicenseBinary = convertToBinaryData(self.LicensePath)
        return -1

    def insertUserInfo(self):
        # Function That calls abstract method to insert user info into database 
        if self.UsType == "Patient":
            pp = Patient.CreatePatient(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.heart, self.diabetes, self.cancer, self.obesity, self.smoker, self.hypertension, self.allergies, self.Blood)
            pp.SaveData()
        if self.UsType == "Radiologist":
            radiologistdata = Radiologist.CreateRadiologist(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.radioCenter)
            radiologistdata.SaveData()
        if self.UsType in ["Consultant", "Specialist"]:
            doctordata = Doctor.CreateDoctor(self.userName ,self.Email, self.Password, self.UsType, self.Phone, self.DoB, self.Gender, self.uni, self.IDbinary, self.LicenseBinary)
            doctordata.SaveData()
        messagebox.showinfo("✅ Success", " You have successfully registered a new account ✅ ", icon="info", parent=self.backgroundFrame)

    def MoveTo(self,UserInfo):
        self.destroy()
        
        id = str(UserInfo[0])
        from UserFactory import UserFactory
        if UserInfo[1].lower() == "patient": # sali@gmail.com       pw: 123
            from PatientGUI import PatGUI
            patient = PatGUI(id)
            patient.mainloop()
        if UserInfo[1].lower() == "radiologist": # salma@gmail.com     PW: 123
            from RadiologistGUI import RadioloGUI
            Radiologist = RadioloGUI(id)
            Radiologist.mainloop()
        if UserInfo[1].lower() == "administrator": # admin   PW: admin
            from AdministratorGUI import AdminGUI
            Admin = AdminGUI(id)
            Admin.mainloop()
        if UserInfo[1].lower() in ["specialist","consultant"]: # sherif_mohamed@gmail.com       pw: 123
            from DoctorGUI import DocGUI
            Doctor = DocGUI(id)
            Doctor.mainloop()

# Administrator GUI
class AdminGUI(ctk.CTk):
    # load Config dict
    configfile = SystemConfig()

    # Define the Admin
    

    Created = [
        True,
        True
    ]  # LoadVerifyDoctorsFrame, LoadHandleReportsFrame PREVENTS duplications

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
        with contextlib.suppress(OSError):
            shutil.rmtree("Data/images/")
        self.user.Logout(self)

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
        with contextlib.suppress(OSError):
            shutil.rmtree("Data/images/")
        self.destroy()

# Doctor GUI
class DocGUI(ctk.CTk):
    # load Config dict
    configfile = SystemConfig()
    systemError = SystemErrors()


    # Define the Doctor
    Created = [
        True,
        True,
        True,
        True,
    ]  # Active chat frame, Patient Req frame, Credits Frame, amount Frame in credits PREVENTS duplications

    def __init__(self, id):
        super().__init__()
        self.user = UserFactory.createUser(id, "doctor")  # 2 Khaled Cons   4 Amira Spec
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
        self.Active_chats_image = ctk.CTkImage(
            ActiveChats,
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
            text_color=self.configfile.get("TextColor"),
            width=100,
            height=20,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.DoctorName_label.grid(row=1, column=0)

        self.DoctorJob_label = ctk.CTkLabel(
            self.LeftSideBar_frame,
            text=self.user.userType,
            text_color=self.configfile.get("TextColor"),
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
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
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
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
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
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("BackgroundColor"),
            image=self.coin_image,
            anchor="w",
            command=self.Credits_button_event,
        )
        self.Credits_button.grid(row=6, column=0, sticky="ew")
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
        self.logoutbutton.grid(row=7, column=0, sticky="ew")
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
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def logout(self):
        with contextlib.suppress(Exception):
            shutil.rmtree("Data/PatientScans/")
            shutil.rmtree("Data/Prescriptions/")
            self.Userclient.end()
        self.user.Logout(self)
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
        frame = ctk.CTkScrollableFrame(
            self.Active_Chats_frame,
            corner_radius=0,
            width=230,
            fg_color=self.configfile.get("FrameColor"),
            scrollbar_button_color=self.configfile.get("FrameColor"), 
            scrollbar_button_hover_color=self.configfile.get("TextColor"),
            height=self.winfo_height() - 20,
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        if len(res)==0:
            NoData= ctk.CTkLabel(frame, text="No Patients Found!" , width=220, height=self.winfo_height() - 150, text_color=self.configfile.get("TextColor"))
            NoData.grid(row=0, column=0, pady=6)
        for pos, item in enumerate(res):
            self.AddtoChatMenu(frame, item[0], pos)

    def AddtoChatMenu(self, master, id, pos):
        output = SelectQuery("SELECT Name, Gender FROM users WHERE ID=%s", [id])
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
            text_color=self.configfile.get("TextColor"),
            hover_color=self.configfile.get("FrameColor"),
            image=Imagesrc,
            anchor="w",
            command=lambda m=id: self.openChat(m),
        )
        self.patientChat.grid(row=pos, column=0, pady=6)

    def openChat(self, id):
        # Chat window that will contain ChatFrame that show the chat for the doctor and chatbox where the doctor type in his chat
        # also send icon that will show the text in chatbox on ChatFrame for both patient and doctor
        with contextlib.suppress(Exception):
            os.mkdir("Data/PatientScans/")
            os.mkdir("Data/Prescriptions/")
            for widget in chatWindow.winfo_children():
                widget.destroy()
            self.Userclient.end()
        start_time = time.time()
        chatWindow = ctk.CTkFrame(
            self.Active_Chats_frame, corner_radius=0, width=840, fg_color="transparent"
        )
        chatWindow.grid(row=0, column=4, sticky="NSEW")

        self.ChatFrame = ctk.CTkScrollableFrame(
            chatWindow, fg_color=self.configfile.get("FrameColor"), width=550, height=385, scrollbar_button_color=self.configfile.get("FrameColor"), scrollbar_button_hover_color=self.configfile.get("TextColor")
        )
        self.ChatFrame.place(anchor="nw", relx=0.01, rely=0.005)

        # End Chat
        self.EndChatButton(chatWindow, id)

        # Report Patient
        self.ReportPatient(chatWindow, id)

        # Generate Prescription for a Patient
        self.GeneratePrescription(chatWindow, id)

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
        self.JoinChatServer(id)

    def ChatBoxBlock(self, master):
        self.chatbox = ctk.CTkTextbox(
            master, font=ctk.CTkFont(size=14, weight="bold"), width=520, height=25,fg_color= self.configfile.get("FrameColor"), text_color=self.configfile.get("TextColor"),border_color=self.configfile.get("TextColor"),border_width=1)
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
        PatientData = UserFactory.createUser(id, "patient")  # Get the patient Data

        if PatientData.userGender == "Male":
            Imagesrc = ctk.CTkImage(MaleImage, size=(100, 100))
        else:
            Imagesrc = ctk.CTkImage(FemaleImage, size=(100, 100))

        Patientinfo = ctk.CTkFrame(master,fg_color="transparent")
        Patientinfo.place(anchor="nw", relx=0.76, rely=0.005)

        PImage = ctk.CTkLabel(Patientinfo, height=40, text="", image=Imagesrc)
        PImage.grid(row=0, column=0)
        PName = ctk.CTkLabel(
            Patientinfo,
            text_color=self.configfile.get("TextColor"),
            height=10,
            text=PatientData.userName,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        PName.grid(row=1, column=0)

        PAge = ctk.CTkLabel(
            Patientinfo,
            text_color=self.configfile.get("TextColor"),
            height=10,
            text=PatientData.CalcAge(PatientData.userAge),
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PAge.grid(row=2, column=0)

        PBloodType = ctk.CTkLabel(
            Patientinfo,
            text_color=self.configfile.get("TextColor"),
            height=10,
            text=PatientData.Blood_Type,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        PBloodType.grid(row=3, column=0)

    def PatientHealthStatus(self, master, id):
        PatientData = UserFactory.createUser(id, "patient")  # Get the patient Data

        # Frame that holds all health Status of the patients as Checkbox if he has that status it will be checked
        HealthStatusFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            width=290,
            height=250,
            fg_color=self.configfile.get("FrameColor"),
        )
        HealthStatusFrame.place(anchor="nw", relx=0.01, rely=0.63)

        HealthStatusLabel = ctk.CTkLabel(
            HealthStatusFrame,
            height=10,
            text_color=self.configfile.get("TextColor"),
            text="Patient Health Status:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        HealthStatusLabel.place(anchor="nw", relx=0.2, rely=0.03)

        AllergiesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Allergies",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        AllergiesBox.place(anchor="nw", relx=0.03, rely=0.15)

        DiabetesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Diabetes",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        DiabetesBox.place(anchor="nw", relx=0.03, rely=0.35)

        CancerBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Cancer",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        CancerBox.place(anchor="nw", relx=0.03, rely=0.55)

        Heart_DiseasesBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Heart Diseases",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        Heart_DiseasesBox.place(anchor="nw", relx=0.03, rely=0.75)

        ObesityBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Obesity",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        ObesityBox.place(anchor="nw", relx=0.5, rely=0.15)

        SmokerBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Smoker",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"),
        )
        SmokerBox.place(anchor="nw", relx=0.5, rely=0.35)

        HypertensionBox = ctk.CTkCheckBox(
            HealthStatusFrame,
            text="Hypertension",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color_disabled=self.configfile.get("TextColor"))
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
        PatientData = UserFactory.createUser(id, "patient")  # Get the patient Data
        res = PatientData.RequestData()
        (
            X_ray_scan,
            Prediction,
            BotChat,
        ) = PatientData.fillindata(res)

        self.LoadBOTChatData(BotChat)
        # Scan Block will contain Patient X-ray Scan with the prediction made by the system
        if Prediction !="":
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
        PatientData = UserFactory.createUser(id, "patient")
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

    def GeneratePrescription(self, master, id):
        # Generate Prescription for a Patient
        GenerateReport = ctk.CTkLabel(
            master,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(GeneratePrescription, size=(40, 40)),
        )
        GenerateReport.place(anchor="nw", relx=0.83, rely=0.92)
        GenerateReport.bind(
            "<Button-1>", lambda event: self.user.HandlePrescription(event, id, self.FillMedication(id))
        )

    def FillMedication(self, id):
        patient = UserFactory.createUser(id, "patient")
        self.MedicineWindow = ctk.CTkToplevel()
        title = f"Fill Medication for Prescription of {patient.userName}"
        self.MedicineWindow.title(title)
        center(
            self.MedicineWindow, 720, 400
        )  # Open the window in the center of the Screen
        self.MedicineWindow.attributes('-topmost', 'true')
        self.MedicineWindow.resizable(False, False)
        self.MedicineWindow.configure(bg_color=self.configfile.get("BackgroundColor"))
        self.MedicineWindow.configure(fg_color=self.configfile.get("BackgroundColor"))



        Text = ctk.CTkLabel(
            self.MedicineWindow,
            text="Add Medications:",
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        Text.place(anchor="nw", relx=0.01, rely=0)

        self.loc = 0
        Add = ctk.CTkLabel(
            self.MedicineWindow, text="", image=(ctk.CTkImage(AddIcon, size=(25, 25)))
        )
        Add.place(anchor="nw", relx=0.9, rely=0.01)
        Add.bind("<Button-1>", self.AddNewMedication)

        delete = ctk.CTkLabel(
            self.MedicineWindow,
            text="",
            image=(ctk.CTkImage(DeleteIcon, size=(25, 25))),
        )
        delete.place(anchor="nw", relx=0.95, rely=0.01)
        delete.bind("<Button-1>", self.DelMedications)

        self.MedicineFrame = ctk.CTkScrollableFrame(
            self.MedicineWindow, fg_color=self.configfile.get("FrameColor"), width=690, height=300, scrollbar_button_color=self.configfile.get("FrameColor"), scrollbar_button_hover_color=self.configfile.get("TextColor")
        )
        self.MedicineFrame.place(anchor="nw", relx=0.01, rely=0.1)

        Show = ctk.CTkButton(
            self.MedicineWindow,
            text="Show",
            command=lambda: self.FinalizePrescription(id, "Show"),
            text_color=self.configfile.get("TextColor"), 
            fg_color=self.configfile.get("FrameColor"), 
            hover_color=self.configfile.get("FrameColor")
        )
        Show.place(anchor="nw", relx=0.75, rely=0.9)

        Save = ctk.CTkButton(
            self.MedicineWindow,
            text="Save",
            command=lambda: self.FinalizePrescription(id, "Save"),
            text_color=self.configfile.get("TextColor"), 
            fg_color=self.configfile.get("FrameColor"), 
            hover_color=self.configfile.get("FrameColor")
        )
        Save.place(anchor="nw", relx=0.55, rely=0.9)

    def AddNewMedication(self, event):
        MedicinEntry = ctk.CTkEntry(
            self.MedicineFrame,
            placeholder_text="Enter Medicine Name",
            text_color=self.configfile.get("TextColor"),
            placeholder_text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("TextColor"),
            fg_color=self.configfile.get("FrameColor"),
            border_width=1,
            width=300,
            height=40,
        )
        MedicinEntry.grid(row=self.loc, column=0,pady=5)

        MedicinEntry = ctk.CTkEntry(
            self.MedicineFrame,
            placeholder_text="Enter Medicine Note",
            text_color=self.configfile.get("TextColor"),
            placeholder_text_color=self.configfile.get("TextColor"),
            border_color=self.configfile.get("TextColor"),
            fg_color=self.configfile.get("FrameColor"),
            border_width=1,
            width=300,
            height=40,
        )
        MedicinEntry.grid(row=self.loc, column=1, padx=5,pady=5)
        self.loc += 1

    def DelMedications(self, event):
        with contextlib.suppress(Exception):
            self.loc = 0
            for widget in self.MedicineFrame.winfo_children():
                widget.destroy()

    def FinalizePrescription(self, id, type):
        patient = UserFactory.createUser(id, "patient")
        path = f"Data\Prescriptions\{patient.userName}.pdf"
        if len(self.MedicineFrame.winfo_children()) == 0:
            return messagebox.showerror("Error", self.systemError.get(20), icon="error", parent=self.MedicineFrame)
        Medicines = []
        MedicinesNotes = []
        for pos, widget in enumerate(
            self.MedicineFrame.winfo_children()
        ):
            if pos % 2 == 0:
                if len(widget.get()) == 0:
                    return messagebox.showerror("Error", self.systemError.get(21), icon="error", parent=self.MedicineFrame)
                else:
                    Medicines.append(widget.get())
            else:
                if len(widget.get()) == 0:
                    MedicinesNotes.append("")
                else:
                    MedicinesNotes.append(widget.get())
        self.user.MakePrescription(id, Medicines, MedicinesNotes)
        if type == "Show":
            subprocess.Popen([path], shell=True)  # Show the Prescription for the Doctor
        else:
            self.MedicineWindow.destroy()
            return MessageBox(self, "info", "Prescription Created")

    def JoinChatServer(self, id):
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
            )  # Send any message to the Patient
            writeThread.start()
        except Exception:
            messagebox.showerror("Error",self.systemError.get(29))

    def LoadBOTChatData(self, BotChat):
        # Load the chat of Patient with id
        msg = BotChat.split(
            "&,&"
        )  # split the chat as queue was saved as one string each item separated by &,&
        for i in msg: 
            self.ChatBlock(i)

    def LoadChatData(self, Patientid):
        # Load the chat of Patient with id
        res = SelectQuery(
            "SELECT Chat_Logs FROM chatdata WHERE Patient_ID= %s", [Patientid]
        )[0][0]
        msg = res.split(
            "&,&"
        )  # split the chat as queue was saved as one string each item separated by &,&
        for i in msg:  # put each message in two Queues
            self.LoaddedChat.put(i)  # Queue that will be Loaded at chat box
            self.ChatLOGS.put(i)  # Queue that will save old chat with the new chat

    def createScanBlock(self, master, name, x, y, w, h, scan, prediction):
        # Frame that will hold Scan Image and Label for its prediction
        blockFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            width=w,
            height=h,
            fg_color=self.configfile.get("FrameColor"),
        )
        blockFrame.place(anchor="nw", relx=x, rely=y)

        # save binary Data of image as an image named as PatientName.png
        scanImage = f"Data/PatientScans/{name}.png"

        write_file(scan, scanImage)

        X_ray = ctk.CTkLabel(
            blockFrame,
            height=10,
            text="",
            text_color=self.configfile.get("TextColor"),
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
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=12, weight="bold")
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
        ScanZoomWindow.attributes('-topmost', 'true')
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
        UpdateQuery(
            "UPDATE chatdata SET Chat_Logs= %s WHERE Patient_ID= %s", [textChat, id]
        )
    
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
        m_frame = ctk.CTkFrame(self.ChatFrame,fg_color="transparent")
        m_frame.pack(anchor="nw", pady=5)
        m_frame.columnconfigure(0, weight=1)

        m_label = ctk.CTkLabel(
            m_frame,
            wraplength=500,
            text=msg,
            height=20,
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont("lucida",size=14,weight="bold"),
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
        if self.user.PrescriptionGenerated(id):
            self.user.EndChat(id, "Done")
            self.LoadActiveChat()
            res = self.user.updateBalance(
                self, 100
            )  # add Credits to the doctor When he ends the chat
            # update button Balance
            if res != -1:
                self.UpdateBalanceButton("Credits added to your balance!")
        else:
            MessageBox(self, "warning", "Report Should be Generated")   

    def ReportReasonBlock(self, event, name, id):
        # Create New Window
        ReportWindow = ctk.CTkToplevel()
        center(ReportWindow, 720, 400)  # Open the window in the center of the Screen
        title = f"Report {name}"
        ReportWindow.title(title)
        ReportWindow.configure(bg_color=self.configfile.get("BackgroundColor"))
        ReportWindow.configure(fg_color=self.configfile.get("BackgroundColor"))
        ReportWindow.geometry("400x200")
        ReportWindow.resizable(False, False)
        ReportWindow.attributes('-topmost', 'true')
        self.reasonEntry = ctk.CTkEntry(
            ReportWindow, width=270, placeholder_text="Enter Reason",placeholder_text_color=self.configfile.get("TextColor"),text_color=self.configfile.get("TextColor"), border_color=self.configfile.get("TextColor"),fg_color=self.configfile.get("FrameColor"))
        self.reasonEntry.place(anchor="nw", relx=0.15, rely=0.3)

        ConfirmButton = ctk.CTkButton(
            ReportWindow, text="Report", command=lambda: self.ReportEvent(id),text_color=self.configfile.get("TextColor"), fg_color=self.configfile.get("FrameColor"), hover_color=self.configfile.get("FrameColor")
        )
        
        ConfirmButton.place(anchor="nw", relx=0.3, rely=0.6)

    def ReportEvent(self, id):
        Reason = self.reasonEntry.get()
        if len(Reason) == 0:
            return messagebox.showerror("Error", self.systemError.get(19), icon="error", parent=self.LeftSideBar_frame)
        self.user.ReportUser(id, Reason)
        self.user.EndChat(id, "Report")
        self.LoadActiveChat()
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
            text_color=self.configfile.get("TextColor"),
            width=100,
            height=50,
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        HeaderLabel.place(anchor="nw", relx=0.35, rely=0)

        res = self.user.LoadWaitingPatientRequests()
        # Scrollable frame that will hold all Available Patients with request status as waiting
        AvailablePatientsFrame = ctk.CTkScrollableFrame(
            self.PatientRequests_frame, fg_color=self.configfile.get("FrameColor"), width=1050, height=640,scrollbar_button_color=self.configfile.get("FrameColor"), scrollbar_button_hover_color=self.configfile.get("TextColor"))
        AvailablePatientsFrame.place(anchor="nw", relx=0.01, rely=0.08)
        if len(res)==0:
            Nodata = ctk.CTkLabel( AvailablePatientsFrame, text="No Patients Found!", width=1050, height=600, font=ctk.CTkFont(size=15, weight="bold"),text_color=self.configfile.get("TextColor"))
            Nodata.grid(row=0, column=0, pady=6)

        for i in range(len(res)):
            (
                Patient_ID,
                Patient_Req_Date,
                Patient_Name,
                Patient_Gender,
                Patient_Age,
                Patient_VIP,
            ) = self.user.fillindata(res[i])
            patient_border = ctk.CTkFrame(
                AvailablePatientsFrame,
                corner_radius=0,
                width=1050,
                height=100,
                fg_color=self.configfile.get("FrameColor"),
                border_color=self.configfile.get("TextColor"),
                border_width=2
            )
            patient_border.grid(row=i, column=0, padx=1, pady=6)

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
            Image_label.place(anchor="nw", relx=0, rely=0.25)

            NameLabel = ctk.CTkLabel(
                patient_border,
                text=Patient_Name,
                text_color=self.configfile.get("TextColor"),
                bg_color="transparent",
                fg_color="transparent",
                width=200,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            NameLabel.place(anchor="nw", relx=0.1, rely=0.35)


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
            VIP.place(anchor="nw", relx=0.27, rely=0.25)

            GenderLabel = ctk.CTkLabel(
                patient_border,
                text=Patient_Gender,
                bg_color="transparent",
                fg_color="transparent",
                text_color=self.configfile.get("TextColor"),
                width=100,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            GenderLabel.place(anchor="nw", relx=0.37, rely=0.35)

            AgeLabel = ctk.CTkLabel(
                patient_border,
                text=self.user.CalcAge(Patient_Age),
                bg_color="transparent",
                fg_color="transparent",
                text_color=self.configfile.get("TextColor"),
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
                text_color=self.configfile.get("TextColor"),
                width=100,
                height=20,
                font=ctk.CTkFont(size=15, weight="bold"),
            )
            ReqDateLabel.place(anchor="nw", relx=0.7, rely=0.35)

            AcceptButton = ctk.CTkButton(
                patient_border,
                text="Chat",
                text_color=self.configfile.get("TextColor"), 
                fg_color=self.configfile.get("FrameColor"), 
                hover_color=self.configfile.get("BackgroundColor"),
                corner_radius=0,
                width=100,
                height=20,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=lambda m=Patient_ID: self.AssignPatient(m),
            )
            AcceptButton.place(anchor="nw", relx=0.88, rely=0.35)

    def AssignPatient(self, id):
        # UPDATE requests SET Request_Status = "waiting"
        self.user.AssignMePatient(id)
        self.loadWaitingPatients()

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
            self.credits_frame, text="/", width=20, font=ctk.CTkFont(size=14), text_color=self.configfile.get("TextColor"))
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
            MessageBox(self, "warning", "CVV is not 3 digit")
        else:
            self.CardChecked = True

    def WithdrawBlock(self):
        self.WithdrawLabel = ctk.CTkLabel(
            self.credits_frame,
            text="Withdraw Credits",
            width=60,
            text_color=self.configfile.get("TextColor"),
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.WithdrawLabel.place(anchor="nw", relx=0.4, rely=0.45)

        self.QuickSelectionsFrame = ctk.CTkFrame(
            self.credits_frame, corner_radius=0, fg_color=self.configfile.get("FrameColor"), width=350
        )
        self.QuickSelectionsFrame.place(anchor="nw", relx=0.05, rely=0.65)

        self.Label = ctk.CTkLabel(
            self.QuickSelectionsFrame, text="Select Credits:", font=ctk.CTkFont(size=14), text_color=self.configfile.get("TextColor")
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
            text_color=self.configfile.get("TextColor"), 
            fg_color=self.configfile.get("FrameColor"), 
            hover_color=self.configfile.get("FrameColor"),
            command=self.Withdraw_button_event,
        )
        self.Withdraw_Button.place(anchor="nw", relx=0.66, rely=0.8)

    def AddOption(self, master, x, y, vari, txt, val, fun=True):
        option = ctk.CTkRadioButton(master, variable=vari, text=txt, value=val,text_color=self.configfile.get("TextColor"))
        option.place(anchor="w", relx=x, rely=y)
        if fun:
            option.bind("<Button-1>", self.RemoveAmount)  # Remove Entry Frame if found
        else:
            option.bind("<Button-1>", self.HandleAmount)  # Show Entry Frame if found
        return option

    def HandleAmount(self, event):
        if self.Created[3]:
            self.AmountFrame = ctk.CTkFrame(
                self.credits_frame, corner_radius=0, fg_color=self.configfile.get("FrameColor"), width=150
            )
            self.Created[3] = False
        self.AmountFrame.place(anchor="nw", relx=0.38, rely=0.65)

        self.clabel = ctk.CTkLabel(
            self.AmountFrame, text="Enter Credits:", font=ctk.CTkFont(size=14),text_color=self.configfile.get("TextColor")
        )
        self.clabel.place(anchor="w", relx=0.2, rely=0.1)

        self.Amount = ctk.CTkEntry(
            self.AmountFrame,
            placeholder_text="Amount",
            placeholder_text_color=self.configfile.get("TextColor"),
            text_color=self.configfile.get("TextColor"),
            fg_color=self.configfile.get("FrameColor"),
            border_color=self.configfile.get("TextColor"),
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

    def Withdraw_button_event(self):
        if self.CardChecked == False:  #
            return messagebox.showerror("Error", self.systemError.get(17), icon="error", parent=self.LeftSideBar_frame)
        else:
            if int(self.credit_val.get()) == -1:
                if (
                    self.Amount.get() == ""
                    or self.Amount.get().isalpha()
                    or int(self.Amount.get()) <= 0
                ):
                    return messagebox.showerror("Error", self.systemError.get(18), icon="error", parent=self.LeftSideBar_frame)
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
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.delType()
        self.Active_Chats_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Active_Chats" else "transparent"
        )
        self.PatientRequests_button.configure(
            fg_color=self.configfile.get("BackgroundColor")
            if name == "PatientRequests"
            else "transparent"
        )
        self.Credits_button.configure(
            fg_color=self.configfile.get("BackgroundColor") if name == "Credits" else "transparent"
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
        self.user.SetApperanceMode(new_appearance_mode)

    def exit_function(self):
        with contextlib.suppress(Exception):
            shutil.rmtree("Data/PatientScans/")
            shutil.rmtree("Data/Prescriptions/")
            self.Userclient.end()
        self.destroy()

# Patient GUI
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
        self.messages = [{"role": "system", "content": "You are an AI chatbot called Live Healthy Bot in a medical system that assists pulmonary by interacting with patients and ask them firstly whether they have recent x-ray scan for their lungs or not, if yes ask them to import it to the system so the system can check what pulmonary diseases they have. Secondly ask them to say their symptoms that they feel or have. Thirdly Ask the patients how long they have been experiencing these symptoms because This information will help you and our system to better understand the patient's condition and provide more accurate recommendations for treatment. Fourthly ask them if they take any current medication or if they have taken any medication regarding thier condition. Fifthly ask them if they have any extra information that may be helpful for you to give them a proper medical advice for them after getting all these information predict if the patient has one from five diseases which are Covid-19, Fibrosis, Tuberculosis, viral pneumonia and bacterial pneumonia or if the patient is not having any of these diseases, after that predict if the patient's health state is critical and then give them a proper medical advice and recommend treatments according to their case from the x-ray result and from what they have provided or answered and also recommend that they press on a button called Chat With Doctor which exists at the bottom right of the screen in the system in order to to chat with a doctor to help them. Finally, ask them whether they need anything else, if not thank them for using our system and remind them to live healthy which is also your name and then end the conversation politely. Be positive and calm the patient down, ask only one question at each time and not multiple questions at a time. Only answer medical-related questions, particularly those related to pulmonary health"}]
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

        if not Bot:
        # join Chat Server
            self.JoinChatServer()

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
            messagebox.showerror("Error",self.systemError.get(29))
            # messagebox.showerror("Error","Chat Server is offline")
            # print("Chat Server is offline")

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

# Radiologist GUI
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
        UpdateQuery(
            "UPDATE users SET Apperance_Mode = %s WHERE ID= %s",
            [new_appearance_mode, self.user.userid],
        )

if __name__ == "__main__":
    ErrorCodes = SystemErrors()
    code = Database.OnlineDB()
    if code != -100:
        app = Starter()
        app.mainloop()
    else:
        messagebox.showerror("Error", ErrorCodes.get(28), icon="error")