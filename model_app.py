""" Application to train models and perform inference on certain pretrained models """
import os

import numpy as np
import skimage.io as sk_io
import streamlit as st

import modelling as mtrain
import processing as dproc
import producer
import utils

CONFIG = utils.get_config()
CHOICE = CONFIG["BrokerChoice"]["Type"]

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
        producer = producer.instantiate_producer(CHOICE)

        st.markdown(f"Sending message to Kafka topic **{CONFIG[CHOICE]['Topic']}**")
        producer.send_image(img, mname, CONFIG[CHOICE]["Topic"])
        st.markdown(
            f"Message has been sent to Kafka topic **{CONFIG[CHOICE]['Topic']}**"
        )

        st.markdown(
            "Check the Consumer of this topic at **results_app.py** for a prediction!"
        )
