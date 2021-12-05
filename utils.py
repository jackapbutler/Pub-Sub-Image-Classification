""" General utility functions for streamlit and image processing"""
import os
from typing import List

import streamlit as st


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
