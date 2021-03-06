"""Base consumer class for handling image messages"""
import abc
import json
from typing import Dict, Tuple

import numpy as np

import inference as infer


class BaseConsumer(abc.ABC):
    """Abstract base class for Consumers"""

    @abc.abstractmethod
    def initialise_consumer(self) -> None:
        """Start listening to a certain topic"""
        pass

    @staticmethod
    def decode_message(dict_data) -> Tuple[np.ndarray, str]:
        decoded_data = json.loads(dict_data.decode("utf-8"))

        return np.array(json.loads(decoded_data.get("img_data"))), decoded_data.get(
            "model"
        )

    @staticmethod
    def make_prediction(model_name: str, img_array: np.ndarray) -> None:
        """Helper method to predict the label of a given image array"""
        model, _ = infer.load_model_and_history(model_name)

        try:
            prediction = infer.perform_image_prediction(img_array, model)
            print(f"Predicted is complete with label: **{prediction}**")

        except Exception:
            print("Failed to get prediction for this message.")
