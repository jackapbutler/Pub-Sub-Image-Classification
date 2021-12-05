# Model Training

This app handles all of training of the CNN models.

I have used a basic CNN model defined inside of [`modelling`.py](../modelling.py). You can add more layers, hidden neurons, convolutional filters or change any other model configuration elements inside of the `create_and_compile_model()` function.

Once you are satisfied with the model architecture follow the steps below:

1. Open up the [`streamlit`](https://streamlit.io/) application by running `streamlit run model_app.py` in a terminal.

2. Choose the `Model Training` option from the **What do you want to do?** select box.

3. Enter the folder where the extracted `.png` image files are stored.

   > See [data extraction](DATA.md) for more information on extracting the image files.

4. Enter a unique `model name` you want to assign this model (e.g. cnn_10_filters).

5. Click the **Start Training** button to begin training the model!
