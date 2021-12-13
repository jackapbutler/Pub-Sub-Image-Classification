""" Module for handling model loading and inference functionality """
import pickle
from typing import Tuple

import numpy as np
import tensorflow.keras as keras
import tensorflow.keras.callbacks as cbacks

import processing as dproc
import utils

CONFIG = utils.get_config()


def load_model_and_history(
    model_name: str,
) -> Tuple[keras.models.Sequential, cbacks.History]:
    """Loads a training tensorflow model and training history from local file storage"""
    model = keras.models.load_model(f"{CONFIG['Modelling']['ModelDir']}/{model_name}")
    trainHistory = pickle.load(
        open(f"{CONFIG['Modelling']['ModelDir']}/{model_name}/trainHistoryDict.p", "rb")
    )
    return model, trainHistory


def perform_image_prediction(
    img_array: np.ndarray, model: keras.models.Sequential
) -> str:
    """Takes in the NumPy array of image data and a keras model to perfom classification"""
    prepped_img = dproc.prep_image(img_array)
    final_img = prepped_img.reshape(1, prepped_img.shape[0], prepped_img.shape[1], 1)
    output = model.predict(final_img)
    pred = str(np.argmax(output))
    return dproc.LABELS.get(pred)
