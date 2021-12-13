"""Instantiating different consumer types based on user input"""
from typing import Literal, Union

import consumers.gcp_consumer as gcp_consumer
import consumers.kafka_consumer as kafka_consumer

CONSUMERS = {
    "Kafka": kafka_consumer.KafkaImageConsumer(),
    "GCP Pub/Sub": gcp_consumer.GCPImageConsumer(),
}


def instantiate_consumer(
    type: Literal["Kafka", "GCP Pub/Sub"]
) -> Union[kafka_consumer.KafkaImageConsumer, gcp_consumer.GCPImageConsumer]:
    """Instantiate an image consumer using a certain backend, default to KafkaImageConsumer"""
    if type in list(CONSUMERS.keys()):
        consumer = CONSUMERS.get(type)

    else:
        print(f"Could not find a consumer with type {type}, defaulting to Kafka.")
        consumer = kafka_consumer.KafkaImageConsumer()

    return consumer
