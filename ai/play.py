from sogo import valid_moves, move_wins

import numpy as np

from tensorflow.python.keras.models import model_from_json


class Play:

    def __init__(self, path):
        self.model = self.make_player(path)
        self.reset()

    def make_player(self, path):
        with open(f"{path}.json", 'r') as file:
            model = model_from_json(file.read())
        model.load_weights(f"{path}.h5")
        return model

    def make_move(self, i, j, k):
        move = np.zeros((4, 4, 4))
        move[i, j, k] = 1

        if move_wins(self.white, i, j, k):
            return (-1, -1, -1, "white wins")

        self.white = self.white + move
        actions, rewards = valid_moves(self.black, self.white)

        if len(rewards) == 0:
            return (-1, -1, -1, "draw")

        qs = self.model.predict(actions)
        action_index = np.argmax(qs.flatten())

        action = actions[action_index]
        reward = rewards[action_index]

        self.black = self.black + action[:, :, :, 2]

        i, j, k = np.nonzero(action[:, :, :, 2])
        i, j, k = i[0], j[0], k[0]

        if reward == 1:
            return (i, j, k, "black won")
        else:
            return (i, j, k, "open")

    def reset(self):
        self.white = np.zeros((4, 4, 4))
        self.black = np.zeros((4, 4, 4))
