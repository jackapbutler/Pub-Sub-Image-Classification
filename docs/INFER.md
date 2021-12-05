# Model Inference

The app `model_app.py` handles all inference for the CNN models.

Now that we have a trained model and stream processing service setup we can try to predict the label of an image.

To perform a prediction on a new image follow the steps below:

1. Open up the `streamlit` application by running `streamlit run model_app.py` in a terminal.

2. Choose the `Inference` option from the **What do you want to do?** select box.

3. Enter the `model name` you want to perform the prediction.

   > The model name is placed as a key which the Kafka Consumer uses to know which model should perform the prediction.

4. Upload your chosen Fashion clothing image.

5. Click the **Start** button to get a prediction!
