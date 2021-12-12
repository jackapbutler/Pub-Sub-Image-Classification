""" Module to handle instantiating and sending image data from a Kafka producer """
import kafka
import numpy as np

import utils

CONFIG = utils.get_config()


class KafkaImageProducer:
    """Kafka Producer class which can send and decode images"""

    def __init__(self, bootstrap_servers=CONFIG["Kafka"]["Host"]) -> None:
        self.bootstrap_servers: str = bootstrap_servers
        self.img_producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_image(
        self,
        img_array: np.ndarray,
        model_name: str,
        topic: str,
    ) -> None:
        """
        Sends a image as bytes to a certain Kafka topic
        """
        self.img_producer.send(
            topic,
            key=f"{model_name}".encode("utf-8"),
            value=utils.img_to_bytes(img_array),
        )
        self.img_producer.flush()
