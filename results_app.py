""" Application to start a Kafka consumer and watch image processing """
import logging

import streamlit as st
import tensorflow.keras as keras

import inference as infer
from kafka_consumer import KafkaImageConsumer, DEFAULT_TOPIC
import utils

st.title("Results/Prediction App")
st.markdown(
    f"This application will generate a Kafka consumer listening on the **{DEFAULT_TOPIC}** topic for images sent by the producer in **model_app.py**."
)
st.markdown(
    "The message is parsed using the key as the **model name** to send the request to and the value as the **image data** in bytes"
)
st.markdown(
    "The bytes data is then transformed, the model is loaded from local storage and a prediction is made for fashion category."
)

start = utils.StartButton("Start Listening")

if start:
    kafka_consumer = KafkaImageConsumer()
    initialised = kafka_consumer.initialise_consumer()

    for message in initialised:
        st.subheader(f"Message Received")

        img_array, model_name = kafka_consumer.decode_message(message)

        st.write("A prediction is required for this image:")
        st.image(img_array)
        st.markdown(f"The message has key value of **{model_name}**.")

        st.markdown(f"Loading model **{model_name}** from local storage.")
        model, trainHistory = infer.load_model_and_history(model_name)

        if isinstance(model, keras.models.Sequential):
            st.write("Model has been loaded successfully from local storage.")
            st.write("Performing image prediction now.")

            try:
                prediction = infer.perform_image_prediction(img_array, model)
                st.markdown(f"Predicted is complete with label: **{prediction}**")

            except Exception as ex:
                msg = "Failed to get prediction for this message."
                logging.error(msg)
                st.write(msg)

        else:
            st.write("Failed to load model from local storage.")
            st.write(f"Loaded object as type: {type(model)}")
