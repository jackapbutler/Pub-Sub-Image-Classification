# Pub-Sub-Image-Classification

A Pub/Sub system for Fashion Image Classification.

In order to setup the entire application;

- Install the appropriate Python environment.
- Follow the steps outlined in the table of contents below.

## Python Environment

This repository uses Python 3.8.

The Python packages are stored in the `env.yml` file. These can be installed using `conda` by running:

```shell
conda env create -f env.yml
```

## Contents

1. [Data Extraction](docs/DATA.md)
2. [Model Training](docs/MODEL.md)
3. [Pub/Sub Architecture](docs/PUBSUB.md)
4. [Inference](docs/INFER.md)

## Code Formatting

This respository uses `black` and `isort` for code and package import formatting.
To run these execute the following commands in the terminal;

- `black <file_name>` or `black .` for all files.
- `isort <file_name>` or `isort .` for all files.
