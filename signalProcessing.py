# This file uses the model that is trained to process sensor data
# Basic file to get started with

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from serial import Serial

# Adjust this to your Arduino's serial port name and baud rate
ser = Serial('COM3', 2400)

# Define the model
def create_model():
    model = Sequential()
    model.add(Dense(48, input_dim=24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Load the model and its pre-trained weights
model = create_model()
model.load_weights('model_weights.h5')

try:
    while True:
        # Read a line from serial
        line = ser.readline().decode('utf-8').strip()

        # Convert the comma-separated string to a list of integers
        data = list(map(int, line.split(',')))

        # Print the entire array
        input_data = np.array(data).reshape(1, -1)
        model.predict(input_data)[0][0]

        # Do something with processed user input

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
