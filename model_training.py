""" Module for handling model compilation and training """
import pickle
from typing import Tuple
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import tensorflow.python.keras.callbacks as cbacks

MODEL_DIR = "models/"


def create_and_compile_model(D_x: int, D_y: int) -> keras.models.Sequential:
    """Compiles a baseline CNN model using ReLu activation and He Weight Initialization scheme"""
    theModel = keras.models.Sequential(
        [
            keras.layers.Conv2D(
                10,
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
    with open(f"{MODEL_DIR}{model_name}_trainHistoryDict.p", "wb") as fp:
        pickle.dump(trainHistory.history, fp)
    theModel.save(model_name)


def load_model_history(
    model_name: str,
) -> Tuple[keras.models.Sequential, cbacks.History]:
    """Loads a training tensorflow model and training history from local file storage"""
    model = keras.models.load_model(f"{MODEL_DIR}{model_name}")
    trainHistory = pickle.load(
        open(f"{MODEL_DIR}{model_name}_trainHistoryDict.p", "rb")
    )
    return model, trainHistory


def plot_training_history(trainHistory: cbacks.History) -> None:
    metric_names = list(trainHistory.keys())
    for name in metric_names:
        plt.plot(trainHistory[name])
        plt.legend(metric_names)
    plt.show()
