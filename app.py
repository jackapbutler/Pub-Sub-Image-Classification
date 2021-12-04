import os
import numpy as np
import skimage.io as sk_io
import producer as prod
import streamlit as st

import data_processing as dproc
import model_training as mtrain

KAFKA_TOPIC = "sample"

st.title("CNN Classifier")
choice = st.selectbox(
    label="What do you want to do?", options=["Training", "Inference"]
)

if choice == "Training":
    file_path = st.text_input(
        label="Please enter the folder in the root directory which contains your image files."
    )
    mname = st.text_input(label="Please provide a name for this trained model.")
    start = st.button("Start")

    if start:
        st.title("Experiment Log...")

        if os.path.exists(file_path):
            st.write(
                f"Found the folder [{file_path}], splitting images into train, test and validation sets."
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
            st.write(f"Saved model to under name [{mname}]")

            mtrain.plot_training_history(mname, trainHistory)
            st.write(f"Plotted training history for model [{mname}]")

        else:
            st.write(
                f"Could not find the folder [{file_path}]. Please check this is where images are stored"
            )


elif choice == "Inference":
    mname = st.text_input(label="Please provide a name for this trained model.")
    image = st.file_uploader(label="Please upload your image to classify.")
    start = st.button("Start")

    if start:
        st.subheader("Your Image")
        st.write(image)
        st.image(image)

        img: np.ndarray = sk_io.imread(image)
        st.write(f"Sending message to Kafka topic {KAFKA_TOPIC}")
        prod.send_img_to_kafka(img, KAFKA_TOPIC)

        # model, history = mtrain.load_model_history(mname)
        st.write(f"Loaded model and training history for [{mname}]")
