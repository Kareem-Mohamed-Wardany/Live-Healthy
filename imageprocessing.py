import cv2
from random import shuffle
import numpy as np
import os
from tensorflow import keras
from keras import utils
from Dataset import *
from Config import *


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
        print(filename, imagename)
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
