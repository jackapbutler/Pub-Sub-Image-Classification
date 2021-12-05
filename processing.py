""" Module for handling data loading and processing """

import os
import random
from typing import List, Tuple

import numpy as np
import skimage.io as sk_io
import skimage.util as sk_utils
import tensorflow.keras.utils as tf_utils

import utils

BATCH_SIZE = 20

LABELS = {
    "0": "T-shirt/top",
    "1": "Trouser",
    "2": "Pullover",
    "3": "Dress",
    "4": "Coat",
    "5": "Sandal",
    "6": "Shirt",
    "7": "Sneaker",
    "8": "Bag",
    "9": "Ankle boot",
}


class DataGenerator(tf_utils.Sequence):
    """
    DataGenerator Class for feeding images to CNN model.
    """

    def __init__(
        self,
        fileNames,
        doRandomize=False,
    ):
        self.fileNames: List[str] = fileNames
        self.batchSize: int = BATCH_SIZE
        self.doRandomize: bool = doRandomize
        self.numImages: int = len(self.fileNames)  # number of files
        self.on_epoch_end()

    def on_epoch_end(self):
        """
        Shuffle the data at the end of every epoch (if required)
        """
        if self.doRandomize:
            random.shuffle(self.fileNames)

    def _load_image_pair_(self, imageIndex: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Helper method used by `__getitem__` to handle loading image data.

        Args:
            imageIndex (int): An integer representing the sample index.

        """
        file = self.fileNames[imageIndex]

        img_sk = sk_io.imread(file)
        split_f = file.split("/")  # to get the 0 in data/0/sample.png

        return prep_image(img_sk), tf_utils.to_categorical(
            split_f[1], num_classes=utils.fcount(split_f[0])
        )

    def __len__(self) -> int:
        """Returns the number of batches"""
        return int(np.ceil(float(self.numImages) / float(self.batchSize)))

    def __getitem__(self, theIndex: int) -> Tuple[np.ndarray, np.ndarray]:
        """Gets "theIndex"-th batch from the training data"""
        X = []
        y = []
        bStart = max(theIndex * self.batchSize, 0)
        bEnd = min((theIndex + 1) * self.batchSize, self.numImages)

        for i in range(bStart, bEnd):
            [curImage, curGT] = self._load_image_pair_(i)
            X.append(curImage)
            y.append(curGT)

        return np.array(X), np.array(y)


def prep_image(img_array: np.ndarray) -> np.ndarray:
    """Scales and prepares a raw image array for the CNN model"""
    scaled_arr = img_array.astype("float32") / 255.0
    return sk_utils.img_as_float(scaled_arr)


def train_test_val_split(
    img_folder: str,
) -> Tuple[DataGenerator, DataGenerator, DataGenerator]:
    """
    Takes in the name of a directory storing images and returns training, validation and testing image lists.
    Data folder structure is expected in the format: `img_folder`/<image_label_digit>/<image.png>.
    It returns a instance of DataGenerator for each list of images.

    Args:
        img_folder (str): A folder name
    """
    all_filenames: List[str] = [
        os.path.join(root, name)
        for root, _, files in os.walk(img_folder)
        for name in files
        if name.endswith((".png", ".png"))
    ]

    random.shuffle(all_filenames)
    trainSet, testSet, valSet = np.split(
        all_filenames, [int(len(all_filenames) * 0.7), int(len(all_filenames) * 0.9)]
    )

    # sense check duplicates
    for pair in [[trainSet, testSet], [trainSet, valSet], [testSet, valSet]]:
        verdict = any(f in pair[0] for f in pair[1])

        if verdict is True:
            print("Duplicate values occur between ", pair[0], " and ", pair[1])

    return DataGenerator(trainSet), DataGenerator(testSet), DataGenerator(valSet)
