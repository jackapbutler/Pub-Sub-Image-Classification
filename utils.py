""" General utility functions for streamlit and image processing"""

import configparser
import io
import json
import os
from typing import List

import numpy as np
import streamlit as st

CONFIG_PATH = "config.ini"


def ModelInput() -> str:
    """Adds a model name text input box for trained models"""
    return st.text_input(label="Please provide a name for this trained model.")


def StartButton(name: str) -> str:
    """Adds a button with a name label"""
    return st.button(label=name)


def ImageUpload() -> str:
    """Adds a file upload with an image label text"""
    return st.file_uploader(label="Please upload your image to classify.")


def FilePath() -> str:
    """Adds a file path text input box for image data"""
    return st.text_input(
        label="Please enter the folder in the root directory which contains your image files."
    )


def ViewChoice(options: List[str]) -> str:
    """Adds a view choice select box for different options"""
    return st.selectbox(label="What do you want to do?", options=options)


def fcount(path: str) -> int:
    """Counts the number of folders inside a certain folder"""
    count1 = 0
    for _, dirs, _ in os.walk(path):
        count1 += len(dirs)

    return count1


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def img_to_bytes(img_array: np.ndarray) -> bytes:
    """Convert image array into bytes"""
    np_bytes = io.BytesIO()
    np.save(np_bytes, img_array, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_img(img_bytes: bytes) -> np.ndarray:
    """Decodes the bytes into a NumPy array"""
    load_bytes = io.BytesIO(img_bytes)
    return np.load(load_bytes, allow_pickle=True)


def get_config() -> configparser.ConfigParser:
    """Read from the config.ini file for backend configuration variables"""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["GoogleCloud"][
        "CredentialsPath"
    ]
    return config
