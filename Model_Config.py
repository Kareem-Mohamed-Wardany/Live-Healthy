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
    tensorboard = TensorBoard(
        log_dir=os.path.join(os.getcwd(), "logs"), histogram_freq=1, write_images=True
    )

    # Save a model checkpoint after every epoch
    checkpoint = ModelCheckpoint(
        "Data/ResNet.h5", monitor="val_accuracy", verbose=1, save_best_only=True
    )
    early = EarlyStopping(monitor="val_accuracy", min_delta=0, patience=30, verbose=1)

    # Add callbacks to list
    callbacks = [tensorboard, checkpoint, early]

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
