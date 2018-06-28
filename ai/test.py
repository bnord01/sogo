import numpy as np
from tensorflow.python.keras.models import model_from_json

from sogo import valid_moves


def make_player(path):
    with open(f"{path}.json", 'r') as file:
        model = model_from_json(file.read())
    model.load_weights(f"{path}.h5")
    return model


def play(player1, player2):
    model1 = player1
    model2 = player2
    white = np.zeros((4, 4, 4))
    black = np.zeros((4, 4, 4))
    white[0, 0, 0] = 0
    white[2, 1, 0] = 0
    black[1, 2, 0] = 0
    black[1, 1, 0] = 0

    round = 1
    while(True):
        actions, rewards = valid_moves(white, black)

        qs = model1.predict(actions)
        action_index = np.argmax(qs.flatten())

        action = actions[action_index]
        reward = rewards[action_index]

        if reward > 0:
            print(f"{'white' if round%2==1 else 'black'} wins after {round} rounds.")
            print(white+black*8+action[:, :, :, 2]*4)
            return
        elif round == 63:
            print('No winner after 64 rounds.')
            print(white+black*8+action[:, :, :, 2]*4)
            return
        else:
            black, white = white + action[:, :, :, 2], black
            model1, model2 = model2, model1
            round = round + 1


player1 = make_player("models/model380")
player2 = make_player("models/model50")
play(player1, player2)
