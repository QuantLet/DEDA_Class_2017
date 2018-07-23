from keras.datasets import mnist
from keras.utils import np_utils, plot_model
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.layers.normalization import BatchNormalization
import numpy as np
import time
from keras.layers import SimpleRNN, Activation, Dense
import matplotlib.pyplot as plt
from keras.models import load_model


def trainning_process(model_history):
    fig = plt.figure(figsize=(15, 5))
    # Accuracy Increasing
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), model_history.history['acc'], 'blue')
    plt.plot(range(1, epochs + 1), model_history.history['val_acc'], 'red')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy', fontsize=15)
    plt.yticks(fontsize=18)
    plt.xlabel('Epoch', fontsize=15)
    plt.xticks(np.arange(1, epochs + 1), fontsize=15)
    # Loss Decreasing
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs + 1), model_history.history['loss'], 'blue')
    plt.plot(range(1, epochs + 1), model_history.history['val_loss'], 'red')
    plt.title('Model Loss')
    plt.ylabel('Loss', fontsize=15)
    plt.xlabel('Epoch', fontsize=15)
    plt.xticks(np.arange(1, epochs + 1), fontsize=15)
    plt.show()
    return fig


# download the mnist to the path '~/.keras/datasets/' if it is the first time to be called
(X_train, y_train), (X_test, y_test) = mnist.load_data()

train_sample_size, row_size, col_size = X_train.shape
test_sample_size = X_test.shape[0]

print(f"Total Sample Size: {train_sample_size + test_sample_size}, "
      f"Training Sample Size: {train_sample_size},"
      f"Testing Sample Size: {test_sample_size}")
print(f"row pixel: {row_size}, column pixel: {col_size}")

# Parameter Specification
np.random.seed(123)  # for reproducibility
nb_filters = 32
pool_size = (2, 2)
kernel_size = (3, 3)
input_shape = (row_size, col_size, 1)
num_classes = 10
batch_size = 128
epochs = 12

# data pre-processing
X_train = X_train.reshape(train_sample_size, *input_shape).astype('float32')
X_test = X_test.reshape(test_sample_size, *input_shape).astype('float32')
# Normalize pixel data
X_train = X_train / 255
X_test = X_test / 255
# Transform label set into binary representation, or so called "One-hot encoding"
y_train = np_utils.to_categorical(y_train, num_classes=10)
y_test = np_utils.to_categorical(y_test, num_classes=10)

# build RNN model
model = Sequential()

# RNN model specification
model.add(Convolution2D(nb_filters, *kernel_size, border_mode='valid', input_shape=input_shape))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(Convolution2D(nb_filters, *kernel_size, border_mode='valid'))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=pool_size))  # Pool layer
model.add(Dropout(0.25))  # Randomly deactivate neurons
model.add(Flatten())  # Transform into 1 dimensional data
model.add(Dense(128))  # Full connected
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(BatchNormalization())
model.add(Activation("softmax"))

# Compile with defined parameters
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# training
start_time = time.time()
model_result = model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=epochs, verbose=1,
                         validation_data=(X_test, y_test))
end_time = time.time()
process_plot = trainning_process(model_result)
process_plot.savefig('trainning_process_plot.png', dpi=300)
print(
    f'Training takes {round((end_time - start_time)/60, 1)} minutes to complete')  # Takes about half an hour to finish
validation_acc = model_result.history['val_acc'][-1]
print(f'The final accuracy is {validation_acc*100}%')  # The final cross validation accuracy is 99.22%
model.save('cnn_model.h5')

# ============Load Trained Model=============
model_loaded = load_model('cnn_model.h5')
test_accu = model_loaded.evaluate(X_test, y_test)
print(f'Test Accuracy is: {test_accu[1]}')
