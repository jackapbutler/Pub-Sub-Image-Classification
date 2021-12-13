"""Instantiating different producer types based on user input"""
from typing import Literal, Union

import producers.gcp_producer as gcp_producer
import producers.kafka_producer as kafka_producer

PRODUCERS = {
    "Kafka": kafka_producer.KafkaImageProducer(),
    "GCP Pub/Sub": gcp_producer.GCPImageProducer(),
}


def instantiate_producer(
    type: Literal["Kafka", "GCP Pub/Sub"]
) -> Union[kafka_producer.KafkaImageProducer, gcp_producer.GCPImageProducer]:
    """Instantiate an image producer using a certain backend, default to KafkaImageProducer"""
    if type in list(PRODUCERS.keys()):
        producer = PRODUCERS.get(type)

    else:
        print(f"Could not find a consumer with type {type}, defaulting to Kafka.")
        producer = kafka_producer.KafkaImageProducer()

    return producer
