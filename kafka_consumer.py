""" Module for consuming Kafka messages from the inference topic """
from typing import Tuple

import kafka
import numpy as np

import utils
from base_consumer import BaseConsumer

CONFIG = utils.get_config()


class KafkaImageConsumer(BaseConsumer):
    """Kafka Consumer class which can be initialised to receive images"""

    def __init__(self, topic: str = CONFIG["Kafka"]["Host"]) -> None:
        self.topic = topic

    def initialise_consumer(self):
        """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
        initialised_consumer = kafka.KafkaConsumer(
            self.topic,
            auto_offset_reset="earliest",
        )

        for message in initialised_consumer:
            img_array, model_name = self.decode_message(message)
            self.make_prediction(model_name, img_array)

    def decode_message(self, message) -> Tuple[np.ndarray, str]:
        """Decode a full message received from a producer and returns the image array and model name"""
        mname_bytes: bytes = message.key
        img_bytes: bytes = message.value

        return utils.bytes_to_img(img_bytes), mname_bytes.decode("utf-8")
