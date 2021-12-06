""" Module for handling model compilation and training """
import pickle
from typing import Tuple

import tensorflow.keras as keras
import tensorflow.python.keras.callbacks as cbacks

import processing as dproc

MODEL_DIR = "models"
TRAIN_EPOCHS = 50


def create_and_compile_model(D_x: int, D_y: int) -> keras.models.Sequential:
    """Compiles a baseline CNN model using ReLu activation and He Weight Initialization scheme"""
    theModel = keras.models.Sequential(
        [
            keras.layers.Conv2D(
                30,
                (3, 3),
                activation="relu",
                kernel_initializer="he_uniform",
                input_shape=(D_x, D_x, 1),
            ),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(20, activation="relu", kernel_initializer="he_uniform"),
            keras.layers.Dense(D_y, activation="softmax"),
        ]
    )

    theModel.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return theModel


def save_trained_model(
    model_name: str, theModel: keras.models.Sequential, trainHistory: cbacks.History
) -> None:
    """Saves a tensorflow model and training history to local file storage"""
    with open(f"{MODEL_DIR}/{model_name}/trainHistoryDict.p", "wb") as fp:
        pickle.dump(trainHistory.history, fp)
    theModel.save(f"{MODEL_DIR}/{model_name}")


def fit_cnn_model(
    model: keras.models.Sequential,
    trainGen: dproc.DataGenerator,
    valGen: dproc.DataGenerator,
) -> Tuple[keras.models.Sequential, cbacks.History]:
    """Train a compiled Tensorflow CNN model on GPU"""

    trainHistory = model.fit(
        trainGen,
        epochs=TRAIN_EPOCHS,
        verbose=1,
        callbacks=[
            cbacks.EarlyStopping(monitor="val_accuracy", mode="max", min_delta=1)
        ],
        validation_data=valGen,
    )
    return model, trainHistory
