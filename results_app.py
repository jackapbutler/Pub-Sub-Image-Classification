""" Application to start a Kafka consumer and watch image processing """
import kafka_consumer as consumer
import processing as dproc
import logging
import inference as infer
import streamlit as st
import utils

st.title("Results/Prediction App")
st.markdown(
    f"This application will generate a Kafka consumer listening on the **{consumer.TOPIC}** topic for images sent by the producer in **model_app.py**."
)
st.markdown(
    "The message is parsed using the key as the **model name** to send the request to and the value as the **image data** in bytes"
)
st.markdown(
    "The bytes data is then transformed, the model is loaded from local storage and a prediction is made for fashion category."
)

start = utils.StartButton("Start Listening")

if start:
    kafka_consumer = consumer.initialise_img_consumer(consumer.TOPIC)

    for message in kafka_consumer:
        st.subheader(f"Message Received")

        mname_bytes: bytes = message.key
        img_bytes: bytes = message.value

        img_array = dproc.bytes_to_img(img_bytes)
        model_name = mname_bytes.decode()

        st.write("A prediction is required for this image:")
        st.image(img_array)
        st.markdown(f"The message has key value of **{model_name}**.")

        st.markdown(f"Loading model **{model_name}** from local storage.")
        model, _ = infer.load_model_and_history(model_name)
        st.write(f"Model has been loaded successfully from local storage.")

        st.write("Performing image prediction now.")
        try:
            prediction = infer.perform_image_prediction(img_array, model_name)
        except Exception as ex:
            logging.exception(ex)
            st.write("Producer message was not suitable for prediction.")
            st.write(img_array)
            prediction = None

        if prediction:
            st.markdown(f"Predicted is complete with label: {prediction}")
        else:
            st.markdown("No valid prediction for this message.")
