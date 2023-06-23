import os
import sys
from Dataset import *
from imageprocessing import *
from Model_Config import *
from sklearn.metrics import accuracy_score, precision_score, recall_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow
from keras import Model
from keras.layers import (Activation, Add, BatchNormalization, Conv2D, Dense,
                          Flatten, GlobalAveragePooling2D, Input, Lambda)
from keras.models import load_model


class ResNetModel:
    modelConfig = None
    def ResidualBlock(self, x, number_of_filters, match_filter_size=False):
        self.modelConfig = model_configuration()
        # Retrieve initializer
        initializer = self.modelConfig.get("initializer")

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
        if match_filter_size:
            x_skip = Lambda(lambda x: tensorflow.pad(x[:, ::2, ::2, :],tensorflow.constant([[0,0],[0, 0],[0, 0],[number_of_filters // 4, number_of_filters // 4]]),mode="CONSTANT",))(x_skip)

        # Add the skip connection to the regular mapping
        x = Add()([x, x_skip])

        # Nonlinearly activate the result
        x = Activation("relu")(x)

        # Return the result
        return x

    def Blocks(self, x):
        self.modelConfig = model_configuration()
        # Set initial filter size
        filter_size = self.modelConfig.get("initialNumberofFilters")
        # Paper: "Then we use a stack of 6n layers (...) with 2n layers for each feature map size. 6n/2n = 3, so there are always 3 groups.
        for Group in range(self.modelConfig.get("RepeatofBlocks")):
            # Each block in our code has 2 weighted layers, and each group has 2n such blocks, so 2n/2 = n blocks per group.
            for block in range(self.modelConfig.get("RepeatofBlocks")):
                if Group > 0 and block == 0:
                    filter_size *= 2
                    x = self.ResidualBlock(x, filter_size, match_filter_size=True)
                else:
                    x = self.ResidualBlock(x, filter_size)
        return x

    def WholeModel(self, shp):
        self.modelConfig = model_configuration()
        # Get number of classes from model configuration
        initializer = self.modelConfig.get("initializer")
        # Define model structure
        inputs = Input(shape=shp)
        x = Conv2D(
            self.modelConfig.get("initialNumberofFilters"),
            kernel_size=(3, 3),
            strides=(1, 1),
            kernel_initializer=initializer,
            padding="same",
        )(inputs)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = self.Blocks(x)
        x = GlobalAveragePooling2D()(x)
        x = Flatten()(x)
        outputs = Dense(self.modelConfig.get("num_classes"), kernel_initializer=initializer)(x)

        return inputs, outputs

    def ModelCompile(self): 
        self.modelConfig = model_configuration()
        # Get model base
        inputs, outputs = self.WholeModel((self.modelConfig.get("width"), self.modelConfig.get("height"), self.modelConfig.get("dim")))
        # Initialize and compile model
        model = Model(inputs, outputs)
        model.compile(loss=self.modelConfig.get("loss"),optimizer=self.modelConfig.get("optimizer"),metrics=self.modelConfig.get("optimizer_additional_metrics"))
        return model

    def ModelTrain(self, model, x_train, x_valid, y_train, y_valid):
        self.modelConfig = model_configuration()
        # Fit data to model
        model.fit(x_train,y_train,batch_size=self.modelConfig.get("BatchSize"),epochs=self.modelConfig.get("epochs"),verbose=self.modelConfig.get("verbose"),callbacks=self.modelConfig.get("callbacks"),steps_per_epoch=self.modelConfig.get("TrainingStepsPerEpoch"),validation_data=(x_valid, y_valid),validation_steps=self.modelConfig.get("ValidationStepsPerEpoch"))
        return model

    def ModelEvaluate(self, model, xtest, ytest):
        self.modelConfig = model_configuration()
        # Evaluate model
        score = model.evaluate(xtest, ytest, verbose=1)
        print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')

        # Predict labels
        y_pred = model.predict(xtest)
        y_pred = np.argmax(y_pred, axis=1)
        ytest = np.argmax(ytest, axis=1)
        print(y_pred)
        print(ytest)
        precision = precision_score(ytest, y_pred, average='weighted')
        print("Precision:", precision)

        # Calculate recall
        recall = recall_score(ytest, y_pred, average='weighted')
        print("Recall:", recall)

        # Calculate F1 score
        classes = ["Normal", "COVID", "Bacterial PNEUMONIA", "Viral PNEUMONIA", "Fibrosis", "Tuberculosis"]
        self.plot_confusion_matrix(ytest, y_pred, classes)

    def plot_confusion_matrix(self, y_true, y_pred, classes):
        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)

        # Normalize the confusion matrix
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        # Create a figure and axes
        plt.figure(figsize=(8, 6))
        ax = plt.gca()

        # Plot the confusion matrix
        sns.heatmap(cm, annot=True, cmap='Blues', fmt='.2f', cbar=False, ax=ax)

        # Set the axis labels and title
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title('Confusion Matrix')

        # Set the x-axis and y-axis ticks
        tick_marks = np.arange(len(classes))
        ax.set_xticks(tick_marks + 0.5)
        ax.set_yticks(tick_marks + 0.5)
        ax.set_xticklabels(classes, rotation=45)
        ax.set_yticklabels(classes, rotation=45)

        # Show the plot
        plt.tight_layout()
        plt.show()

    def TrainingProcess(self, ev=False):
        # load test and train data
        dsM = Dataset()
        x_test, y_test = dsM.loadTestData()
        x_train, x_valid, y_train, y_valid = dsM.CreateValidData()
        resnet = self.ModelCompile()
        trained_resnet = self.ModelTrain(resnet, x_train, x_valid, y_train, y_valid)
        if ev:
            self.ModelEvaluate(trained_resnet, x_test, y_test)
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
        x = trained_resnet.predict(img, verbose=0)
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