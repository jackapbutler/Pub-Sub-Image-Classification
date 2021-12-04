# Pub-Sub-Image-Classification

A Pub/Sub system for Fashion Image Classification.

# Setup

This repository uses Python 3.8.

The Python packages are stored in the `env.yml` file. These can be installed using `conda` by running:

- `conda env create -f env.yml`

  > This project was developed mainly on an M1 Macbook Air so some dependencies might not work.

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

## Pub Sub

Now that the model is trained we can setup the Kafka Pub-Sub architecture.

1. Install [Java](https://www.oracle.com/java/technologies/downloads/) in order to run the Kafka executables.
2. Download Kafka’s binaries from the official [download page](https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz) (this one is for v3.0.0).
3. Extract the tar files (inside of the appropriate directory): `tar -xvzf kafka_2.13-3.0.0.tgz`.
4. Run the servers:

   a) Run Zookeeper for state management: `bin/zookeeper-server-start.sh config/zookeeper.properties`

   b) Kafka for data storage and distribution: `bin/kafka-server-start.sh config/server.properties`

5. We will need to create one topic called `fashion-images` for this assignment.

- Create a topic by running `bin/kafka-topics.sh --create --topic fashion-images --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4`.

> List all created topics with `bin/kafka-topics.sh --list --bootstrap-server localhost:9092`.

> Describe a certain topic with `bin/kafka-topics.sh --describe --topic fasion-images --bootstrap-server localhost:9092`.

> Delete a topic with `bin/kafka-topics.sh --delete --topic fashion-images --bootstrap-server localhost:9092`

6. To setup Kafka you will need a [Producer](producer.py) and [Consumer](consumer.py).

- To setup the Consumer, open up a terminal instance and run `python3 consumer.py`
- The Producer will be controlled inside of `app.py` and does not need any prior setup.

## Inference

Now that we have a trained model and Kafka streaming service setup we can predict the label of an image.

1. Open up the `streamlit` application by running `streamlit run app.py`.

2. Choose the `Inference` option from the first select box.

3. Upload your chosen image to generate fashion clothing category prediction.

## Code Formatting

This respository uses `black` and `isort` for code and package import formatting.
To run these execute the following commands in the terminal;

- `black <file_name>` or `black .` for all files
- `isort <file_name>` or `isort .` for all files
