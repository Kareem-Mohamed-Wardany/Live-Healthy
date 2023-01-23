import os
import numpy as np
from sklearn.model_selection import train_test_split

class Dataset:

  def loadDataset(self): # load the gray data that was read before and labeled
    return np.load('Data/DatasetGray.npy', allow_pickle=True) # load dataset 


  def saveDataset(self, path, data): # save the data of images with labels to be used later
    np.save(path, data) 

  def loadTrainData(self):
    if (os.path.exists('Data/x_train.npy')):
      images = np.load('Data/x_train.npy', allow_pickle=True)
    if (os.path.exists('Data/y_train.npy')):
      labels = np.load('Data/y_train.npy', allow_pickle=True)
    return images, labels

  def loadTestData(self):
    if (os.path.exists('Data/x_test.npy')):
      images = np.load('Data/x_test.npy', allow_pickle=True)
    if (os.path.exists('Data/y_test.npy')):
      labels = np.load('Data/y_test.npy', allow_pickle=True)
    return images, labels

  def CreateValidData(self):
    x_train, y_train = self.loadTrainData()
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)
    return x_train, x_valid, y_train, y_valid