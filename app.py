import streamlit as st
import os

import data_processing as dproc
import model_training as mtrain

st.title("CNN Classifier")
choice = st.selectbox(
    label="What do you want to do?", options=["Training", "Inference"]
)

if choice == "Training":
    file_path = st.text_input(
        label="Please enter the folder in the root directory which contains your image files."
    )
    start = st.button("Start")

    if start:
        st.title("Experiment Log...")

        if os.path.exists(file_path):
            st.write(
                f"Found the folder [{file_path}], splitting images into train, test and validation sets."
            )
            trainGen, testGen, valGen = dproc.train_test_val_split(file_path)

            st.write("Creating and compiling CNN model.")
            ex, yv = trainGen._load_image_pair_(0)
            model = mtrain.create_and_compile_model(D_x=ex.shape[0], D_y=yv.shape[0])
            model.summary(print_fn=lambda x: st.write(x + "\n"))

            st.write("Compiled Model successfully, starting to train CNN model")

            model.fit(
                trainGen,
                steps_per_epoch=int(trainGen.numImages / 10),
                epochs=10,
                verbose=1,
                callbacks=None,
                validation_data=valGen,
            )

        else:
            st.write(
                f"Could not find the folder [{file_path}]. Please check this is where images are stored"
            )

