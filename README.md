# Pub-Sub-Image-Classification

A Pub/Sub system for Fashion Image Classification.

# Setup

This repository uses Python 3.8.

The Python packages are stored in the `env.yml` file. These can be installed using `conda` by running:

- `conda env create -f env.yml`

  > For Linux operating system.

- `conda env create -f m1.yml`
  > For M1 Macbook operating system.

## Data Extraction

The main dataset used is the Fasion MNIST benchmark dataset.

I used the `fmnist_to_png.py` file to convert the `.gz` folders from Fashion MNIST into an easier to use `.png`.

1. Download the raw `.gz` dataset from [zalandoresearch/fashion-mnist](https://github.com/zalandoresearch/fashion-mnist)

2. After downloading you should move the files to replicate the folder structure below:

```
data
├── train-images-idx3-ubyte.gz
├── train-labels-idx1-ubyte.gz
├── t10k-images-idx3-ubyte.gz
└── t10k-labels-idx1-ubyte.gz
mnist_to_png.py
```

3. Now run `python3 fmnist_to_png.py` to extract the images as `.png` files.

- This will unzip, parse and save the images to a `png_data/` folder where each subfolder refers to their label.
  > See `LABELS` module level variable in [`fmnist_to_png.py`](fmnist_to_png.py`) for an explanation of these labels.

## Model Training

There is a web application called `app.py` which is written using [`streamlit`](https://streamlit.io/). This app handles all of the CNN model training and inference for this small scale assignment.

To start the app run: `streamlit run app.py`.

You will then be met with two choices [`Model Training` or `Inference`]:

- Follow the instructions in `Model Training` to train a new CNN model defined in `model_training.py` on image data from a certain folder.
- Follow the instructions in `Inference` to obtain a prediction for a new image sample from the existing model.

## Code Formatting

This respository uses `black` and `isort` for code and package import formatting.
To run these execute the following commands in the terminal;

- `black <file_name>` or `black .` for all files
- `isort <file_name>` or `isort .` for all files
