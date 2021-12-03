""" Module for handling model compilation and training """
import tensorflow.keras as keras


def create_and_compile_model(D_x: int, D_y: int) -> keras.models.Sequential:
    theModel = keras.models.Sequential(
        [
            keras.layers.Flatten(input_shape=(D_x, D_x)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(D_y),
        ]
    )

    theModel.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return theModel
