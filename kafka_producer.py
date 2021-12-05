""" Module to handle instantiating and sending image data from a Kafka producer """
import io

import kafka
import numpy as np

LOCAL_KAFKA_HOST = "localhost:9092"


class KafkaImageProducer:
    """Kafka Producer class which can send and decode images"""

    def __init__(self, bootstrap_servers=LOCAL_KAFKA_HOST) -> None:
        self.bootstrap_servers: str = bootstrap_servers
        self.img_producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_image(
        self,
        img_array: np.ndarray,
        model_name: str,
        topic: str,
    ):
        """
        Sends a image as bytes to a certain Kafka topic
        """
        self.img_producer.send(
            topic,
            key=f"{model_name}".encode("utf-8"),
            value=self.img_to_bytes(img_array),
        )
        self.img_producer.flush()

    @staticmethod
    def img_to_bytes(img_array: np.ndarray) -> bytes:
        """Convert image array into bytes"""
        np_bytes = io.BytesIO()
        np.save(np_bytes, img_array, allow_pickle=True)
        return np_bytes.getvalue()
