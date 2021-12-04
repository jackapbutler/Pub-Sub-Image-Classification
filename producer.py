import numpy as np
from kafka import KafkaProducer

import data_processing as dproc

PRODUCER = KafkaProducer(bootstrap_servers="localhost:9092")


def send_img_to_kafka(img_array: np.ndarray, model: str, topic: str):
    """
    Sends a image as bytes to a certain Kafka topic
    """

    img_bytes = dproc.img_to_bytes(img_array)
    PRODUCER.send(topic, key=f"{model}".encode(), value=img_bytes)
    PRODUCER.flush()
