from sogo import valid_moves, move_wins

import numpy as np
import random
from collections import deque
import pickle

import tensorflow as tf

from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Input, Dense, Conv3D, BatchNormalization, Activation, Concatenate, Flatten
from tensorflow.python.keras.optimizers import Adam

GAMMA = 0.90
OBSERVE = 3200
EXPLORE = 3000000
FINAL_EPSILON = 0.0001
INITIAL_EPSILON = 0.1
REPLAY_MEMORY = 50000
BATCH = 1000
LEARNING_RATE = 1e-4


def make_model():

    num_4x1 = 32
    num_4x4 = 64

    inputs = Input(shape=(4, 4, 4, 3))
    t = inputs

    t144 = Flatten()(Conv3D(num_4x1, (4, 1, 1), padding='valid')(t))
    t414 = Flatten()(Conv3D(num_4x1, (1, 4, 1), padding='valid')(t))
    t441 = Flatten()(Conv3D(num_4x1, (1, 1, 4), padding='valid')(t))

    t114 = Flatten()(Conv3D(num_4x4, (4, 4, 1), padding='valid')(t))
    t141 = Flatten()(Conv3D(num_4x4, (4, 1, 4), padding='valid')(t))
    t411 = Flatten()(Conv3D(num_4x4, (1, 4, 4), padding='valid')(t))

    t = Concatenate()([t144, t414, t441, t114, t141, t411, Flatten()(t)])
    t = BatchNormalization()(t)
    t = Activation('relu')(t)

    t = Dense(2048)(t)
    t = BatchNormalization()(t)
    t = Activation('relu')(t)

    t = Dense(512)(t)
    t = BatchNormalization()(t)
    t = Activation('relu')(t)

    t = Dense(1)(t)
    t = Activation('tanh')(t)

    model = Model(inputs, t)
    model.load_weights("models/model50.h5")
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse', optimizer=adam)
    return model


def train_network(model):
    D = deque()
    white = np.zeros((4, 4, 4))
    black = np.zeros((4, 4, 4))
    t = 0
    epsilon = INITIAL_EPSILON
    round = 1
    while(True):
        actions, rewards = valid_moves(white, black)
        if random.random() <= epsilon or round <= 2 and random.random() <= 0.5:
            action_index = random.randrange(len(actions))
        elif random.random() <= 0.5:
            qs = model.predict(actions).flatten()
            action_index = np.argmax(qs)
        else:
            qs = model.predict(actions).flatten()
            print(qs)
            ps = qs + 1
            ps = ps/sum(ps)
            action_index = np.random.choice(range(len(ps)), p=ps)

        action = actions[action_index]
        reward = rewards[action_index]

        D.append((action, reward))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        if t > OBSERVE and t % (BATCH/2) == 0:
            minibatch = random.sample(D, BATCH)
            train_on_batch(model, minibatch)

        if reward > 0:
            print(
                f"{'white' if round%2==1 else 'black'} wins after {round} rounds. (total {t})")
            print(white+black*8+action[:, :, :, 2]*4)
            assert round == sum(action.flatten()), \
                f"Round {round},{sum(action.flatten())} actions: \n{np.array2string(action, separator=',')}"
            white = np.zeros((4, 4, 4))
            black = np.zeros((4, 4, 4))
            round = 1
        elif round == 63:
            print('No winner after 64 rounds.')
            print(white+black*8+action[:, :, :, 2]*4)
            white = np.zeros((4, 4, 4))
            black = np.zeros((4, 4, 4))
            round = 1
        else:
            black, white = white + action[:, :, :, 2], black
            round = round + 1
        t = t + 1

        if t % 10000 == 0:
            print("Saving weights")
            model.save_weights(f"models/model{int(t/1000)}.h5", overwrite=True)
            with open(f"models/model{int(t/1000)}.json", "w") as outfile:
                outfile.write(model.to_json())

        if t % REPLAY_MEMORY == 0:
            print("Saving runs")
            with open(f"data/runs{t/REPLAY_MEMORY}.bin", "w") as outfile:
                pickle.dump(D, outfile)


def train_on_batch(model, minibatch):
    inputs = np.zeros((BATCH, 4, 4, 4, 3))
    targets = np.zeros((BATCH, 1))
    for i in range(0, len(minibatch)):
        action = minibatch[i][0]
        reward = minibatch[i][1]
        inputs[i] = action
        if reward > 0:
            targets[i] = reward
        else:
            white = action[:, :, :, 0] + action[:, :, :, 2]
            black = action[:, :, :, 1]
            actions, rewards = valid_moves(black, white)
            if sum(rewards) > 0:
                targets[i] = -1
            elif len(rewards) == 0:
                targets[i] = 0
            else:
                qs = model.predict(actions)
                targets[i] = - GAMMA*np.max(qs.flatten())
    return model.train_on_batch(inputs, targets)


train_network(make_model())
