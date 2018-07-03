import numpy as np

from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Input, Concatenate, Lambda

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Layer


# Data
WIN_IN_1_1 = np.array([[
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
]])

WIN_IN_1_2 = np.array([[
    [[0, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
]])

WIN_IN_2_1 = np.array([[
    [[1, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
]])


inputs = Input(shape=(4, 4, 4, 3))


def greater3_on_axis(x, axis):
    print(x)
    x = K.sum(x, axis=axis)
    x = K.greater(x, 3)
    x = K.any(x)
    return x


def greater3(x):
    x = K.print_tensor(x, 'input: ')
    x1 = greater3_on_axis(x, 1)
    x2 = greater3_on_axis(x, 2)
    x3 = greater3_on_axis(x, 3)
    x = K.stack([x1, x2, x3])
    x = K.print_tensor(x, 'output: ')
    return K.any(x)


model = Model(inputs, Lambda(greater3)(inputs))

model.predict(np.array([[
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[1, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
]]))

assert model.predict(WIN_IN_1_1)[0]
assert model.predict(WIN_IN_1_2)[0]
assert model.predict(WIN_IN_2_1)[0]

