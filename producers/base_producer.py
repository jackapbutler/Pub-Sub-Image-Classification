"""Base producer class for handling image messages"""
import abc

import numpy as np


class BaseProducer(abc.ABC):
    """Abstract base class for Producers"""

    @abc.abstractmethod
    def send_image(
        self,
        img_array: np.ndarray,
        model_name: str,
        topic: str,
    ) -> None:
        """Send an image array to a streaming topic"""
        pass
