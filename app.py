import streamlit as st

st.title("CNN Classifier")

file_path = st.text_input("Please enter a local folder which contains your image files")

start = st.button("Start Training")

if start:
    st.title("Experiment Log...")
