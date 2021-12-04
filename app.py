import os

import numpy as np
import skimage.io as sk_io
import streamlit as st

import kafka.consumer as consumer
import data_processing as dproc
import model_training as mtrain
import kafka.producer as producer

TRAIN = "Training"
INFER = "Inference"


def ModelInput() -> str:
    return st.text_input(label="Please provide a name for this trained model.")


def StartButton() -> str:
    return st.button("Start")


def ImageUpload() -> str:
    return st.file_uploader(label="Please upload your image to classify.")


def FilePath() -> str:
    return st.text_input(
        label="Please enter the folder in the root directory which contains your image files."
    )


def ViewChoice() -> str:
    return st.selectbox(label="What do you want to do?", options=[TRAIN, INFER])


st.title("CNN Classifier")
choice = ViewChoice()

if choice == TRAIN:
    file_path = FilePath()
    mname = ModelInput()
    start = StartButton()

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
    mname = ModelInput()
    image = ImageUpload()
    start = StartButton()

    if start:
        st.subheader("Your Image")
        st.write(image)
        st.image(image)

        img: np.ndarray = sk_io.imread(image)
        st.markdown(f"Sending message to Kafka topic **{consumer.TOPIC}**")
        producer.send_img_to_kafka(img, mname, consumer.TOPIC)
        st.markdown(f"Message has been sent to Kafka topic **{consumer.TOPIC}**")
        st.write("Check the Consumer of this topic for a prediction!")
