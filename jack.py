import model_training as mtrain
import data_processing as dproc

trainGen, testGen, valGen = dproc.train_test_val_split("png_data")

print("Creating and compiling Model.")
ex, yv = trainGen._load_image_pair_(0)
model = mtrain.create_and_compile_model(D_x=ex.shape[0], D_y=yv.shape[0])
model.summary()
print("Compiled Model successfully.")

print("Starting to train Model.")
model, trainHistory = mtrain.fit_cnn_model(model, trainGen, valGen)
print("Finished training the Model")

mtrain.save_trained_model("baseline", model, trainHistory)
print("Saved model to under name baseline")

mtrain.plot_training_history("baseline", trainHistory)
print("Plotted training history for model baseline")
