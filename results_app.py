""" Application to start a Kafka consumer and watch image processing """
import streamlit as st

import utils
import consumer

CONFIG = utils.get_config()
CHOICE = CONFIG["BrokerChoice"]

st.title("Results/Prediction App")
st.markdown(
    f"This application will generate a Kafka consumer listening on the **{CONFIG[CHOICE]['Topic']}** topic for images sent by the producer in **model_app.py**."
)
st.markdown(
    "The message is parsed using the key as the **model name** to send the request to and the value as the **image data** in bytes"
)
st.markdown(
    "The bytes data is then transformed, the model is loaded from local storage and a prediction is made for fashion category."
)

start = utils.StartButton("Start Listening")

if start:
    img_consumer = consumer.instantiate_consumer(CHOICE)
    initialised = img_consumer.initialise_consumer()
