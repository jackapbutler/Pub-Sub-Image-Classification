""" Module for handling model compilation and training """
import tensorflow.keras as keras


def create_and_compile_model(D_x: int, D_y: int) -> keras.models.Sequential:
    """ Compiles a baseline CNN model using ReLu activation and He Weight Initialization scheme"""
    theModel = keras.models.Sequential(
        [
            keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(D_x, D_x, 1)),
            keras.layers.MaxPooling2D((2, 2)),
	        keras.layers.Flatten(),
	        keras.layers.Dense(100, activation='relu', kernel_initializer='he_uniform'),
	        keras.layers.Dense(D_y, activation='softmax'),
        ]
    )

    theModel.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return theModel
