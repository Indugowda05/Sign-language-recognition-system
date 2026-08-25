from function import *

from sklearn.model_selection import train_test_split

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard

import os
import numpy as np


# Create label map
label_map = {
    label: num
    for num, label in enumerate(actions)
}

print("Label Map:")
print(label_map)


# Create sequences and labels
sequences = []
labels = []


for action in actions:

    for sequence in range(no_sequences):

        window = []

        for frame_num in range(sequence_length):

            npy_path = os.path.join(
                DATA_PATH,
                action,
                str(sequence),
                "{}.npy".format(frame_num)
            )

            res = np.load(npy_path)

            window.append(res)

        sequences.append(window)
        labels.append(label_map[action])


# Convert to NumPy arrays
X = np.array(sequences)
y = to_categorical(labels).astype(int)


print("X shape:", X.shape)
print("y shape:", y.shape)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.05,
    random_state=42,
    stratify=y
)


# TensorBoard
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)


# Create model
model = Sequential()

model.add(
    LSTM(
        64,
        return_sequences=True,
        activation='relu',
        input_shape=(sequence_length, 63)
    )
)

model.add(
    LSTM(
        128,
        return_sequences=True,
        activation='relu'
    )
)

model.add(
    LSTM(
        64,
        return_sequences=False,
        activation='relu'
    )
)

model.add(
    Dense(
        64,
        activation='relu'
    )
)

model.add(
    Dense(
        32,
        activation='relu'
    )
)

# Output layer
model.add(
    Dense(
        actions.shape[0],
        activation='softmax'
    )
)


# Compile
model.compile(
    optimizer='Adam',
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)


# Train
model.fit(
    X_train,
    y_train,
    epochs=100,
    callbacks=[tb_callback],
    validation_data=(X_test, y_test)
)


# Evaluate
test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=1
)

print("Test Accuracy:", test_accuracy)


# Save model architecture
model_json = model.to_json()

with open("model.json", "w") as json_file:
    json_file.write(model_json)


# Save trained model
model.save("model.h5")

print("Model saved successfully!")