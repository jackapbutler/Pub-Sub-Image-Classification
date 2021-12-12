import json
import time
from typing import Dict

import numpy as np
from google.cloud import pubsub_v1

import utils

CONFIG = utils.get_config()


class GCPImageProducer:
    """GCP Pub/Sub Producer class which can send and decode images"""

    def __init__(self, project: str = CONFIG["GoogleCloud"]["Project"]) -> None:
        self.img_producer: pubsub_v1.PublisherClient = pubsub_v1.PublisherClient()
        self.project: str = project

    def send_image(
        self,
        img_array: np.ndarray,
        model_name: str,
        topic: str,
    ) -> None:
        """Sends an image to a certain GCP Pub/Sub topic"""
        topic_path = self.img_producer.topic_path(self.project, topic)
        data = self.prepare_payload(model_name, img_array)
        self.img_producer.publish(topic_path, data)

    def send_message(self, msg: str, topic: str) -> None:
        """Sends basic string message to consumer"""
        topic_path = self.img_producer.topic_path(self.project, topic)
        payload = {"Message": msg}
        print(f"Sending payload {payload}")
        data = json.dumps(payload).encode("utf-8")
        self.img_producer.publish(topic_path, data)

    @staticmethod
    def prepare_payload(model_name: str, img_array: np.ndarray) -> Dict:
        """Prepare payload to be sent to GCP Pub/Sub"""
        payload = {
            "model": model_name,
            "img_data": json.dumps(img_array, cls=utils.NumpyArrayEncoder),
            "time": time.time(),
        }
        return json.dumps(payload).encode("utf-8")
