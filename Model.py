import os
import sys
from Dataset import *
from imageprocessing import *
from Model_Config import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow
from keras import Model
from keras.layers import (Activation, Add, BatchNormalization, Conv2D, Dense,
                          Flatten, GlobalAveragePooling2D, Input, Lambda)
from keras.models import load_model


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
        x = trained_resnet.predict(img)
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
    
# m = ResNetModel()
# prediction = m.PredictScan("TestFolder\COVID-992.png",True)
# print(prediction)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)