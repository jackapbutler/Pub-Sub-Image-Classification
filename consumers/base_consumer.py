"""Base consumer class for handling image messages"""
import abc
from typing import Tuple

import numpy as np

import inference as infer


class BaseConsumer(abc.ABC):
    """Abstract base class for Consumers"""

    @abc.abstractmethod
    def initialise_consumer(self) -> None:
        """Start listening to a certain topic"""
        pass

    @abc.abstractmethod
    def decode_message(self, message) -> Tuple[np.ndarray, str]:
        """Decoded a stream message"""
        pass

    def make_prediction(self, model_name: str, img_array: np.ndarray) -> None:
        """Helper method to predict the label of a given image array"""
        model, _ = infer.load_model_and_history(model_name)

        try:
            prediction = infer.perform_image_prediction(img_array, model)
            print(f"Predicted is complete with label: **{prediction}**")

        except Exception:
            print("Failed to get prediction for this message.")
