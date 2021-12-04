""" Module for consuming Kafka messages from the inference topic """
import kafka
import data_processing as dproc


def initialise_img_consumer(topic: str):
    """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
    consumer = kafka.KafkaConsumer(
        "sample",
        auto_offset_reset="earliest",
        group_id=None,
    )
    for message in consumer:
        img_bytes = message.value
        img_array = dproc.bytes_to_img(img_bytes)

        # make prediction


if __name__ == "__main__":
    TOPIC = "sample"
    initialise_img_consumer(TOPIC)
