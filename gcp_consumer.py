import logging
from typing import Dict
import json
import utils
import numpy as np
from google.cloud import pubsub_v1
import inference as infer

GCP_CONFIG = utils.set_gcp_config()


class GCPImageConsumer:
    """GCP Pub/Sub Consumer class which can be initialised to receive images"""

    def __init__(
        self,
        topic=GCP_CONFIG["topic"],
        subscription_topic=GCP_CONFIG["topic_sub"],
        project=GCP_CONFIG["project"],
    ) -> None:
        self.subscriber = pubsub_v1.SubscriberClient()
        self.topic: str = topic
        self.subscription_topic: str = subscription_topic
        self.project: str = project

    def open_listening_channel(self) -> None:
        """Open the streaming channel to receive messages from a certain topic"""
        subscription_path = self.subscriber.subscription_path(
            self.project, self.subscription_topic
        )
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=self.process_message
        )
        print(f"Listening for messages on {subscription_path}..\n")

        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with self.subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=None)

            except TimeoutError as te:
                logging.exception(f"Timeout error occurred: {te}")
                streaming_pull_future.cancel()
                streaming_pull_future.result()

    def initialise_consumer(self) -> None:
        """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
        while True:
            self.open_listening_channel()

    def process_message(self, message: pubsub_v1.subscriber.message.Message) -> None:
        print("Received Message")
        dict_data: Dict = message.data
        decoded_data = json.loads(dict_data.decode("utf-8"))

        model_name: str = decoded_data.get("model")
        img_array: np.ndarray = np.array(json.loads(decoded_data.get("img_data")))

        model, _ = infer.load_model_and_history(model_name)
        print(infer.perform_image_prediction(img_array, model))

        message.ack()
