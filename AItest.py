import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers



def create_q_model():
  # Network defined by the Deepmind paper
  model = keras.models.Sequential()
  model.add(keras.layers.Flatten(input_shape=[16,2]))
  model.add(keras.layers.Dense(64, activation="relu"))
  model.add(keras.layers.Dense(64, activation="relu"))
  model.add(keras.layers.Dense(32, activation="relu"))
  model.add(keras.layers.Dense(2, activation="softmax"))


create_q_model()