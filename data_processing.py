""" Module for handling data loading and processing """

import os
import random
from typing import List, Tuple

import numpy as np
import skimage.io as skim_io
import tensorflow.keras.utils as tf_utils


class DataGenerator(tf_utils.Sequence):
    """
    DataGenerator Class for feeding images to CNN model.
    """

    def __init__(
        self, fileNames, imgPath, gtPath, doRandomize=False, batchSize=10,
    ):
        self.imgPath: str = imgPath
        self.gtPath: str = gtPath
        self.fileNames: List[str] = fileNames
        self.batchSize: int = batchSize
        self.doRandomize: bool = doRandomize
        self.numImages: int = len(self.fileNames)  # number of files
        self.on_epoch_end()

    def on_epoch_end(self):
        """
        Shuffle the data at the end of every epoch (if required)  
        """
        if self.doRandomize:
            random.shuffle(self.fileNames)

    def _load_image_pair_(self, imageIndex: int):
        """
        Helper method used by `__getitem__` to handle loading image data.

        Args:
            imageIndex (int): An integer representing the sample index.

        """
        file = self.fileNames[imageIndex]

        img_sk = skim_io.imread(os.path.join(self.imgPath, file))
        gt_sk = skim_io.imread(os.path.join(self.gtPath, file))

        theImage = skim_io.img_as_float(img_sk)
        gtImage = tf_utils.to_categorical(gt_sk)

        return theImage, gtImage

    def __len__(self):
        """ Returns the number of batches """
        return int(np.ceil(float(self.numImages) / float(self.batchSize)))

    def __getitem__(self, theIndex: int):
        """ Gets "theIndex"-th batch from the training data """
        X = []
        y = []
        bStart = max(theIndex * self.batchSize, 0)
        bEnd = min((theIndex + 1) * self.batchSize, self.numImages)

        for i in range(bStart, bEnd):
            [curImage, curGT] = self._load_image_pair_(i)
            X.append(curImage)
            y.append(curGT)
        return np.array(X), np.array(y)


def train_test_split(img_folder: str) -> Tuple(List[str], List[str], List[str]):
    """
    Takes in the name of a directory storing images and returns 3 
    mutually exclusive training, validation and testing image lists.

    Args:
        img_folder (str): A folder name
    """
    filenames: List[str] = os.listdir(img_folder)

    random.shuffle(filenames)
    trainSet, testSet, valSet = np.split(
        filenames, [int(len(filenames) * 0.7), int(len(filenames) * 0.9)]
    )

    # sense check duplicates
    for pair in [[trainSet, testSet], [trainSet, valSet], [testSet, valSet]]:
        verdict = any(f in pair[0] for f in pair[1])

        if verdict is True:
            print("Duplicate values occur between ", pair[0], " and ", pair[1])

    return trainSet, testSet, valSet
