""" Module for handling model compilation and training """
import numpy as np
import tensorflow.keras as keras

from data_processing import DataGenerator


def create_and_compile_model() -> keras.models.Sequential:
    theModel = keras.models.Sequential(
        [
            keras.layers.Conv2D(
                8, (3, 3), activation="relu", padding="same", input_shape=(64, 64, 3)
            ),
            keras.layers.MaxPooling2D((2, 2), padding="same"),
            keras.layers.Conv2D(
                64, (3, 3), activation="relu", padding="same", input_shape=(32, 32, 8)
            ),
            keras.layers.Conv2D(
                32, (2, 2), activation="relu", padding="same", input_shape=(32, 32, 64)
            ),
            keras.layers.MaxPooling2D((1, 1), padding="same"),
            keras.layers.Conv2D(
                32, (3, 3), activation="relu", padding="same", input_shape=(32, 32, 32)
            ),
            keras.layers.Conv2D(
                16, (2, 2), activation="relu", padding="same", input_shape=(32, 32, 16)
            ),
            keras.layers.UpSampling2D((2, 2)),
            keras.layers.Conv2D(3, (3, 3), activation="softmax", padding="same"),
        ]
    )

    theModel.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return theModel


def train_cnn(
    trainSet: np.ndarray, trainGenerator: DataGenerator, valGenerator: DataGenerator,
):
    """ Compile and train the CNN model above """
    model = create_and_compile_model()
    model.fit(
        trainGenerator,
        steps_per_epoch=len(trainSet) / 10,
        epochs=100,
        verbose=1,
        callbacks=None,
        validation_data=valGenerator,
    )
