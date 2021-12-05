""" Module to handle instantiating and sending image data from a Kafka producer """
import kafka
import numpy as np

import utils

LOCAL_KAFKA_HOST = "localhost:9092"


def initialise_producer(bootstrap_servers: str) -> kafka.KafkaProducer:
    return kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)


def send_img_to_kafka(
    producer: kafka.KafkaProducer, img_array: np.ndarray, model_name: str, topic: str
):
    """
    Sends a image as bytes to a certain Kafka topic
    """
    producer.send(
        topic, key=f"{model_name}".encode(), value=utils.img_to_bytes(img_array)
    )
    producer.flush()
