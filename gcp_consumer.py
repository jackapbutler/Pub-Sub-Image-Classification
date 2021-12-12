""" Module for consuming GCP messages from the inference topic """
import json
from typing import Dict, Tuple

import numpy as np
from google.api_core import retry
from google.cloud import pubsub_v1

import utils
from base_consumer import BaseConsumer

CONFIG = utils.get_config()


class GCPImageConsumer(BaseConsumer):
    """GCP Pub/Sub Consumer class which can be initialised to receive images"""

    def __init__(
        self,
        subscription_topic=CONFIG["GoogleCloud"]["TopicSub"],
        project=CONFIG["GoogleCloud"]["Project"],
    ) -> None:
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path: str = self.subscriber.subscription_path(
            project, subscription_topic
        )

    def initialise_consumer(self) -> None:
        """Open the streaming channel to receive messages from a certain topic"""

        while True:
            with self.subscriber:
                response = self.subscriber.pull(
                    request={
                        "subscription": self.subscription_path,
                        "max_messages": CONFIG["GoogleCloud"]["MaxMessages"],
                    },
                    retry=retry.Retry(deadline=CONFIG["GoogleCloud"]["MaxSeconds"]),
                )

                ack_ids = []
                for message in response:
                    img_array, model_name = self.decode_message(message)
                    self.make_prediction(model_name, img_array)

            # Acknowledges the received messages so they will not be sent again.
            self.subscriber.acknowledge(
                request={"subscription": self.subscription_path, "ack_ids": ack_ids}
            )
            print(
                f"Received and acknowledged {len(response.received_messages)} messages from {self.subscription_path}."
            )

    def decode_message(
        self, message: pubsub_v1.subscriber.message.Message
    ) -> Tuple[np.ndarray, str]:
        print("Received Message")
        dict_data: Dict = message.data
        decoded_data = json.loads(dict_data.decode("utf-8"))

        return np.array(json.loads(decoded_data.get("img_data"))), decoded_data.get(
            "model"
        )
