""" Module for consuming Kafka messages from the inference topic """
import kafka

import utils
from consumers.base_consumer import BaseConsumer

CONFIG = utils.get_config()


class KafkaImageConsumer(BaseConsumer):
    """Kafka Consumer class which can be initialised to receive images"""

    def __init__(self, topic: str = CONFIG["Kafka"]["Topic"]) -> None:
        self.topic = topic

    def initialise_consumer(self):
        """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
        initialised_consumer = kafka.KafkaConsumer(
            self.topic,
            auto_offset_reset="earliest",
        )

        for message in initialised_consumer:
            img_array, model_name = self.decode_message(message.value)
            self.make_prediction(model_name, img_array)
