""" Module for consuming Kafka messages from the inference topic """
import kafka
import model_training as mtrain
import data_processing as dproc

TOPIC = "fashion-images"


def initialise_img_consumer(topic: str):
    """Initialise a consumer listening for byte-encoded images sent to a certain topics"""
    consumer = kafka.KafkaConsumer(
        topic,
        auto_offset_reset="earliest",
    )

    for message in consumer:
        model_name = message.key
        img_array = dproc.bytes_to_img(message.value)

        print(f"Received an image for model {model_name}")
        pred = perform_image_prediction(img_array, model_name)
        print(f"Predicted Result: {dproc.LABELS.get(pred)}")


def perform_image_prediction(img_array: bytes, model_name: str) -> str:
    """Takes in the bytes message and perfoms a classification prediction"""
    model, _ = mtrain.load_model_and_history(model_name)
    return model.predict(img_array)


if __name__ == "__main__":
    initialise_img_consumer(TOPIC)
