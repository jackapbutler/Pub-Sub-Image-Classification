# Data Extraction

The main dataset used is the Fasion MNIST benchmark dataset.

I used the [`fmnist_to_png.py`](../fmnist_to_png.py) file to convert the `.gz` folders from Fashion MNIST into an easier to use `.png`.

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
  > See `LABELS` module level variable in [`proccessing.py`](../processing.py`) for an explanation of these labels.
