""" Testing the GCP Pub/Sub Inference system"""
import time

import numpy as np
import skimage.io as sk_io

import utils
from gcp_consumer import GCPImageConsumer
from gcp_producer import GCPImageProducer

CONFIG = utils.get_config()

MODEL = "baseline"
TEST_FILE = "png_data/0/1_tr.png"

# loop to test producer and consumer functions with a 3 second delay
while True:
    print("=========================================")

    img_array: np.ndarray = sk_io.imread(TEST_FILE)

    prod = GCPImageProducer()
    prod.send_image(img_array, MODEL, CONFIG["GoogleCloud"]["Topic"])

    cons = GCPImageConsumer()
    cons.initialise_consumer()  # replicates the .initialise_consumer() method

    time.sleep(3)
