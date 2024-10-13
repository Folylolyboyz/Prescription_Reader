from keras import layers
from keras.models import Model

from mltu.tensorflow.model_utils import residual_block

def trainModel(inputDim, outputDim, activation="leaky_relu", dropout=0.2):
    inputs = layers.Input(shape = inputDim, name = "input")
    input = layers.Lambda(lambda x : x / 255)(inputs)
    
    x1 = residual_block(input, 16, activation = activation, skip_conv = True, strides = 1, dropout = dropout)
    
    x2 = residual_block(x1, 16, activation = activation, skip_conv = True, strides = 2, dropout = dropout)
    x3 = residual_block(x2, 16, activation = activation, skip_conv = False, strides = 1, dropout = dropout)
    
    x4 = residual_block(x3, 32, activation=activation, skip_conv=True, strides=2, dropout=dropout)
    x5 = residual_block(x4, 32, activation=activation, skip_conv=False, strides=1, dropout=dropout)

    x6 = residual_block(x5, 64, activation=activation, skip_conv=True, strides=2, dropout=dropout)
    x7 = residual_block(x6, 64, activation=activation, skip_conv=True, strides=1, dropout=dropout)

    x8 = residual_block(x7, 64, activation=activation, skip_conv=False, strides=1, dropout=dropout)
    x9 = residual_block(x8, 64, activation=activation, skip_conv=False, strides=1, dropout=dropout)

    squeezed = layers.Reshape((x9.shape[-3] * x9.shape[-2], x9.shape[-1]))(x9)

    blstm = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(squeezed)
    blstm = layers.Dropout(dropout)(blstm)

    output = layers.Dense(outputDim + 1, activation='softmax', name="output")(blstm)

    model = Model(inputs=inputs, outputs=output)
    return model