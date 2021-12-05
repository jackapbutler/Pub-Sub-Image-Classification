""" Module for consuming Kafka messages from the inference topic """
from typing import Tuple
import kafka
import numpy as np
import io

DEFAULT_TOPIC = "fashion-images"


class KafkaImageConsumer:
    """Kafka Consumer class which can be initialised to receive images"""

    def __init__(self, topic: str = DEFAULT_TOPIC) -> None:
        self.topic = topic

    def initialise_consumer(self):
        """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
        return kafka.KafkaConsumer(
            self.topic,
            auto_offset_reset="earliest",
        )

    def decode_message(self, message) -> Tuple[np.ndarray, str]:
        """Decode a full message received from a producer"""
        mname_bytes: bytes = message.key
        img_bytes: bytes = message.value

        return self.bytes_to_img(img_bytes), mname_bytes.decode()

    @staticmethod
    def bytes_to_img(img_bytes: bytes) -> np.ndarray:
        """Decodes the bytes into the a NumPy array"""
        load_bytes = io.BytesIO(img_bytes)
        return np.load(load_bytes, allow_pickle=True)
