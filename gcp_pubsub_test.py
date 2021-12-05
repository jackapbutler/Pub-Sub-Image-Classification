import numpy as np

""" Testing the GCP Pub/Sub Inference system"""
import time

import skimage.io as sk_io

import utils
from gcp_consumer import GCPImageConsumer
from gcp_producer import GCPImageProducer

GCP_CONFIG = utils.set_gcp_config()
MODEL = "baseline"
TEST_FILE = "png_data/0/1_tr.png"

# loop to test producer and consumer functions with a 3 second delay
while True:
    print("=========================================")

    img_array: np.ndarray = sk_io.imread(TEST_FILE)

    prod = GCPImageProducer()
    prod.send_image(img_array, MODEL, GCP_CONFIG["topic"])

    cons = GCPImageConsumer()
    cons.open_listening_channel()

    time.sleep(3)
