""" Module for consuming Kafka messages from the inference topic """
import kafka
import model_training as mtrain
import data_processing as dproc
import numpy as np

TOPIC = "fashion-images"


def initialise_img_consumer(topic: str):
    """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
    consumer = kafka.KafkaConsumer(
        topic,
        auto_offset_reset="earliest",
    )

    for message in consumer:
        mname_bytes: bytes = message.key
        img_bytes: bytes = message.value

        img_array = dproc.bytes_to_img(img_bytes)
        model_name = mname_bytes.decode()

        print(f"Received an image for model {model_name}")
        prediction = perform_image_prediction(img_array, model_name)
        print(f"Predicted Label: {prediction}")


def perform_image_prediction(img_array: bytes, model_name: str) -> str:
    """Takes in the bytes message and perfoms a classification prediction"""
    model, _ = mtrain.load_model_and_history(model_name)
    prepped_img = dproc.prep_image(img_array)
    final_img = prepped_img.reshape(1, prepped_img.shape[0], prepped_img.shape[1], 1)
    output = model.predict(final_img)
    pred = str(np.argmax(output))
    return dproc.LABELS.get(pred)


if __name__ == "__main__":
    initialise_img_consumer(TOPIC)
