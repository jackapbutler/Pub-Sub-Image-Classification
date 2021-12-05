""" Module for consuming Kafka messages from the inference topic """
import kafka

TOPIC = "fashion-images"


def initialise_img_consumer(topic: str):
    """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
    return kafka.KafkaConsumer(
        topic,
        auto_offset_reset="earliest",
    )
