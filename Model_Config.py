import os
from Dataset import *
import tensorflow
from tensorflow import keras
from keras.optimizers import schedules, SGD
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping


def model_configuration():
    # Dataset size
    dsM = Dataset()
    x_train, x_valid, y_train, y_valid = dsM.CreateValidData()
    TrainSize = len(y_train)
    ValidationSize = len(y_valid)

    # basic config
    width, height, channels = 512, 512, 1
    NumberofClasses = 6
    RepeateofBlocks = 3
    verbose = 1
    BatchSize = 128
    initialNumberofFilters= 16

    # Set layer init
    initializer = tensorflow.keras.initializers.HeNormal()

    # Define loss function
    loss = tensorflow.keras.losses.CategoricalCrossentropy(from_logits=True)

    # Define optimizer
    OptimizerMomentum = 0.9
    optimizer_additional_metrics = ["accuracy"]
    optimizer = SGD(learning_rate=LearningRateSchedule, momentum=OptimizerMomentum)

    # Number of steps per epoch is dependent on batch size
    MaximumIterations = 64000  # per the He et al. paper

    stepsPerEpoch = tensorflow.math.floor(TrainSize / BatchSize)  # calculating Number of steps per epoch

    ValidationStepsPerEpoch = tensorflow.math.floor(ValidationSize / BatchSize)

    epochs = tensorflow.cast(tensorflow.math.floor(MaximumIterations / stepsPerEpoch),dtype=tensorflow.int64)

    # Learning rate config per the He et al. paper
    boundaries = [32000, 48000]
    values = [0.1, 0.01, 0.001]
    LearningRateSchedule = schedules.PiecewiseConstantDecay(boundaries, values)

    # Save a model checkpoint after every epoch
    early = EarlyStopping(monitor="val_accuracy", min_delta=0, patience=30, verbose=1)
    checkpoint = ModelCheckpoint("Data/ResNet.h5", monitor="val_accuracy", verbose=1, save_best_only=True)

    # Add callbacks to list
    callbacks = [checkpoint, early]

    return {
        "width": width,
        "height": height,
        "dim": channels,
        "BatchSize": BatchSize,
        "NumberofClasses": NumberofClasses,
        "verbose": verbose,
        "RepeatofBlocks": RepeateofBlocks,
        "initialNumberofFilters": initialNumberofFilters,
        "TrainSize": TrainSize,
        "TrainingStepsPerEpoch": stepsPerEpoch,
        "ValidationStepsPerEpoch": ValidationStepsPerEpoch,
        "epochs": epochs,
        "loss": loss,
        "optimizer": optimizer,
        "LearningRateSchedule": LearningRateSchedule,
        "OptimizerMomentum": OptimizerMomentum,
        "optimizer_additional_metrics": optimizer_additional_metrics,
        "initializer": initializer,
        "callbacks": callbacks,
    }
