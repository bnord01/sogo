import numpy as np

from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Input, Concatenate, Lambda

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Layer

import tensorflow as tf

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

NUMBERED = np.array([[[[i*16+j*4 + k for k in range(0, 4)]
                       for j in range(0, 4)]for i in range(0, 4)]])

DIAG12 = np.array([[[[1 if i == j else 0 for k in range(0, 4)]
                     for j in range(0, 4)]for i in range(0, 4)]])

DIAG13 = np.array([[[[1 if i == k else 0 for k in range(0, 4)]
                     for j in range(0, 4)]for i in range(0, 4)]])

DIAG23 = np.array([[[[1 if j == k else 0 for k in range(0, 4)]
                     for j in range(0, 4)]for i in range(0, 4)]])

ANTIDIAG12 = np.array([[[[1 if i + j == 3 else 0 for k in range(0, 4)]
                         for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

ANTIDIAG13 = np.array([[[[1 if i + k == 3 else 0 for k in range(0, 4)]
                         for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

ANTIDIAG23 = np.array([[[[1 if j + k == 3 else 0 for k in range(0, 4)]
                         for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

FULLDIAG1 = np.array([[[[1 if i == j == k else 0 for k in range(0, 4)]
                        for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

FULLDIAG2 = np.array([[[[1 if i == j == 3 - k else 0 for k in range(0, 4)]
                        for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

FULLDIAG3 = np.array([[[[1 if i == 3 - j == k else 0 for k in range(0, 4)]
                        for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')

FULLDIAG4 = np.array([[[[1 if 3 - i == j == k else 0 for k in range(0, 4)]
                        for j in range(0, 4)]for i in range(0, 4)]], dtype='int32')


def greater3_on_axis(x, axis):
    x = K.sum(x, axis=axis)
    x = K.greater(x, 3)
    x = K.any(x)
    return x


def greater3(x):
    # x = K.print_tensor(x, 'input: ')
    x1 = greater3_on_axis(x, 1)
    x2 = greater3_on_axis(x, 2)
    x3 = greater3_on_axis(x, 3)
    x = K.stack([x1, x2, x3])
    # x = K.print_tensor(x, 'output: ')
    return K.any(x)


def diaggreater3_on_axis(x, i, j, k):
    assert j < k
    # x = tf.Print(x, [x], summarize=64, message='initial x:          ')
    diag = tf.diag([1, 1, 1, 1])
    # x = tf.Print(x, [diag], summarize=64, message='diagnonal:          ')
    diag = K.stack([diag, diag, diag, diag], axis=i)
    # x = tf.Print(x, [diag], summarize=64, message='diagnonal:          ')
    x = x * diag
    # x = tf.Print(x, [x], summarize=64, message='x * diag:           ')
    x = K.sum(x, axis=k+1)
    # x = tf.Print(x, [x], summarize=64, message='x after first sum:  ')
    x = K.sum(x, axis=j+1)
    # x = tf.Print(x, [x], summarize=64, message='x after second sum: ')
    x = K.greater(x, 3)
    x = K.any(x)
    return x


def diaggreater3(x):
    # x = K.print_tensor(x, 'input: ')
    x1 = diaggreater3_on_axis(x, 0, 1, 2)
    x2 = diaggreater3_on_axis(x, 1, 0, 2)
    x3 = diaggreater3_on_axis(x, 2, 0, 1)
    x = K.stack([x1, x2, x3])
    # x = tf.Print(x, [x], summarize=64, message='diagonals:   ')
    return K.any(x)


def antidiaggreater3(x):
    x1 = x * tf.constant(ANTIDIAG23)
    x1 = K.sum(x1, axis=2)
    x1 = K.sum(x1, axis=2)
    x1 = K.greater(x1, 3)
    x1 = K.any(x1)

    x2 = x * tf.constant(ANTIDIAG13)
    x2 = K.sum(x2, axis=2)
    x2 = K.sum(x2, axis=2)
    x2 = K.greater(x2, 3)
    x2 = K.any(x2)

    x3 = x * tf.constant(ANTIDIAG12)
    x3 = K.sum(x3, axis=2)
    x3 = K.sum(x3, axis=2)
    x3 = K.greater(x3, 3)
    x3 = K.any(x3)

    x = K.stack([x1, x2, x3])
    return K.any(x)


def fulldiaggreater3(x):
    xs = []
    for filt in [FULLDIAG1, FULLDIAG2, FULLDIAG3, FULLDIAG4]:
        x1 = x * tf.constant(filt)
        x1 = K.sum(x1, axis=1)
        x1 = K.sum(x1, axis=1)
        x1 = K.sum(x1, axis=1)
        x1 = K.greater(x1, 3)
        xs.append(x1)

    x = K.stack(xs)
    return K.any(x)


def is_winning(x):
    return K.any(K.stack([greater3(x), diaggreater3(x), fulldiaggreater3(x)]))


inputs = Input(shape=(4, 4, 4), dtype='int32')

assert Model(inputs, Lambda(greater3)(inputs)).predict(DIAG12)[0]
assert Model(inputs, Lambda(greater3)(inputs)).predict(DIAG13)[0]
assert Model(inputs, Lambda(greater3)(inputs)).predict(DIAG23)[0]

assert Model(inputs, Lambda(greater3)(inputs)).predict(ANTIDIAG12)[0]
assert Model(inputs, Lambda(greater3)(inputs)).predict(ANTIDIAG13)[0]
assert Model(inputs, Lambda(greater3)(inputs)).predict(ANTIDIAG23)[0]

assert not Model(inputs, Lambda(greater3)(inputs)).predict(FULLDIAG1)[0]
assert not Model(inputs, Lambda(greater3)(inputs)).predict(FULLDIAG2)[0]
assert not Model(inputs, Lambda(greater3)(inputs)).predict(FULLDIAG3)[0]
assert not Model(inputs, Lambda(greater3)(inputs)).predict(FULLDIAG4)[0]

assert Model(inputs, Lambda(diaggreater3)(inputs)).predict(DIAG12)[0]
assert Model(inputs, Lambda(diaggreater3)(inputs)).predict(DIAG13)[0]
assert Model(inputs, Lambda(diaggreater3)(inputs)).predict(DIAG23)[0]

assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(ANTIDIAG12)[0]
assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(ANTIDIAG13)[0]
assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(ANTIDIAG23)[0]

assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(FULLDIAG1)[0]
assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(FULLDIAG2)[0]
assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(FULLDIAG3)[0]
assert not Model(inputs, Lambda(diaggreater3)(inputs)).predict(FULLDIAG4)[0]

assert not Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(DIAG12)[0]
assert not Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(DIAG13)[0]
assert not Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(DIAG23)[0]

assert Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(ANTIDIAG12)[0]
assert Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(ANTIDIAG13)[0]
assert Model(inputs, Lambda(antidiaggreater3)(inputs)).predict(ANTIDIAG23)[0]

assert not Model(inputs, Lambda(antidiaggreater3)
                 (inputs)).predict(FULLDIAG1)[0]
assert not Model(inputs, Lambda(antidiaggreater3)
                 (inputs)).predict(FULLDIAG2)[0]
assert not Model(inputs, Lambda(antidiaggreater3)
                 (inputs)).predict(FULLDIAG3)[0]
assert not Model(inputs, Lambda(antidiaggreater3)
                 (inputs)).predict(FULLDIAG4)[0]

assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(DIAG12)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(DIAG13)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(DIAG23)[0]

assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(ANTIDIAG12)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(ANTIDIAG13)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(ANTIDIAG23)[0]

assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(FULLDIAG1)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(FULLDIAG2)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(FULLDIAG3)[0]
assert Model(inputs, Lambda(fulldiaggreater3)(inputs)).predict(FULLDIAG4)[0]
