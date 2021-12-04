import numpy as np
from kafka import KafkaProducer

import data_processing as dproc

PRODUCER = KafkaProducer(bootstrap_servers="localhost:9092")


def send_img_to_kafka(img_array: np.ndarray, topic: str):
    """Sends a certain image file to a Kafka topic as bytes"""

    img_bytes = dproc.img_to_bytes(img_array)
    PRODUCER.send(topic, key=b"inference_img", value=img_bytes)
    PRODUCER.flush()
