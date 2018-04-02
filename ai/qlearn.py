from sogo import valid_moves, move_wins

import numpy as np
import random
from collections import deque
import json

from keras.models import Sequential
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam
import h5py

BOARDX = 4
BOARDY = 4
BOARDZ = 4
ACTIONS = 1

GAMMA = 0.90
OBSERVE = 3200
EXPLORE = 3000000
FINAL_EPSILON = 0.0001
INITIAL_EPSILON = 0.1
REPLAY_MEMORY = 50000
BATCH = 1000
LEARNING_RATE = 1e-4

def make_model():
    model = Sequential()
    model.add(Dense(64, activation='tanh', input_shape=(BOARDX,BOARDY,BOARDZ,3)))
    model.add(Flatten())
    model.add(Dense(512, activation='tanh'))
    model.add(Dense(1024, activation='tanh'))
    model.add(Dense(512, activation='tanh'))
    model.add(Dense(64, activation='tanh'))
    model.add(Dense(ACTIONS))

    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    return model

def train_network(model):
    D = deque()
    white = np.zeros((4,4,4))
    black = np.zeros((4,4,4))
    t = 0
    epsilon = INITIAL_EPSILON
    round = 1
    while(True):
        actions, rewards = valid_moves(white, black)
        if random.random() <= epsilon:
            action_index = random.randrange(len(actions))

        else:
            qs = model.predict(actions)
            action_index = np.argmax(qs.flatten())

        action = actions[action_index]
        reward = rewards[action_index]

        D.append((action,reward))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        if t > OBSERVE and t % (BATCH/2) == 0:
            minibatch = random.sample(D,BATCH)
            train_on_batch(model,minibatch)

        if reward > 0:
            print(f"{'white' if round%2==1 else 'black'} wins after {round} rounds.")
            print(white+black*8+action[:,:,:,2]*4)
            assert round == sum(action.flatten()), \
                f"Round {round},{sum(action.flatten())} actions: \n{np.array2string(action, separator=',')}"
            white = np.zeros((4,4,4))
            black = np.zeros((4,4,4))
            round = 1
        elif round == 63:
            print('No winner after 64 rounds.')
            print(white+black*8+action[:,:,:,2]*4)
            white = np.zeros((4,4,4))
            black = np.zeros((4,4,4))
            round = 1
        else:
            black, white = white + action[:,:,:,2], black
            round = round + 1
        t = t + 1

        if t % 10000 == 0:
            model.save_weights(f"models/model{int(t/1000)}.h5", overwrite=True)
            with open(f"models/model{int(t/1000)}.json", "w") as outfile:
                outfile.write(model.to_json())

def train_on_batch(model,minibatch):
    inputs = np.zeros((BATCH,BOARDX,BOARDY,BOARDZ,3))
    targets = np.zeros((BATCH,1))
    for i in range(0, len(minibatch)):
        action = minibatch[i][0]
        reward = minibatch[i][1]
        inputs[i] = action
        if reward > 0:
            targets[i] = reward
        else:
            white = action[:,:,:,0] + action[:,:,:,2]
            black = action[:,:,:,1]
            actions,rewards = valid_moves(black,white)
            if sum(rewards) > 0:
                targets[i] = -1
            elif len(rewards) == 0:
                targets[i] = 0
            else:
                qs = model.predict(actions)
                targets[i] = - GAMMA*np.max(qs.flatten())
    return model.train_on_batch(inputs,targets)

train_network(make_model())
