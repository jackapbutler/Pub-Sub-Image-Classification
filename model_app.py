""" Application to train models and perform inference on certain pretrained models """
import os

import numpy as np
import skimage.io as sk_io
import streamlit as st

import kafka_consumer as consumer
import kafka_producer as producer
import modelling as mtrain
import processing as dproc
import utils

TRAIN = "Training"
INFER = "Inference"


st.title("CNN Classifier")
choice = utils.ViewChoice(options=[TRAIN, INFER])

if choice == TRAIN:
    file_path = utils.FilePath()
    mname = utils.ModelInput()
    start = utils.StartButton("Start Training")

    if start:
        st.title("Experiment Log...")

        if os.path.exists(file_path):
            st.markdown(
                f"Found the folder **{file_path}**, splitting images into train, test and validation sets."
            )
            trainGen, testGen, valGen = dproc.train_test_val_split(file_path)

            st.write("Creating and compiling Model.")
            ex, yv = trainGen._load_image_pair_(0)
            model = mtrain.create_and_compile_model(D_x=ex.shape[0], D_y=yv.shape[0])
            model.summary(print_fn=lambda x: st.write(x + "\n"))

            st.write("Compiled Model successfully.")

            st.write("Starting to train Model.")
            model, trainHistory = mtrain.fit_cnn_model(model, trainGen, valGen)
            st.write("Finished training the Model")

            mtrain.save_trained_model(mname, model, trainHistory)
            st.markdown(f"Saved model to under name **{mname}**")

        else:
            st.markdown(
                f"Could not find the folder **{file_path}]**. Please check this is where images are stored"
            )

elif choice == INFER:
    mname = utils.ModelInput()
    image = utils.ImageUpload()
    start = utils.StartButton("Send Image")

    if start:
        st.subheader("Your Image")
        st.write(image)
        st.image(image)
        img: np.ndarray = sk_io.imread(image)

        st.write("Initialising a Kafka producer.")
        kafka_producer = producer.initialise_producer(producer.LOCAL_KAFKA_HOST)
        st.write(f"Initialised a Kafka producer at {producer.LOCAL_KAFKA_HOST}.")

        st.markdown(f"Sending message to Kafka topic **{consumer.TOPIC}**")
        producer.send_img_to_kafka(kafka_producer, img, mname, consumer.TOPIC)
        st.markdown(f"Message has been sent to Kafka topic **{consumer.TOPIC}**")

        st.markdown(
            "Check the Consumer of this topic at **results_app.py** for a prediction!"
        )
