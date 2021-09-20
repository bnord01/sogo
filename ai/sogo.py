import numpy as np


def valid_moves(white, black):
    moves = []
    rewards = []
    for i in range(0, 4):
        for j in range(0, 4):
            k = int(sum(white[i, j]) + sum(black[i, j]))
            if k < 4:
                move = np.zeros((4, 4, 4))
                move[i, j, k] = 1
                move = np.stack((white, black, move), axis=3)
                moves.append(move)
                rewards.append(move_wins(white, i, j, k))
    if len(moves) > 0:
        return np.stack(moves), rewards
    else:
        return np.zeros((0, 4, 4, 4, 3)), rewards


directions = [np.array((i, j, k)) for i in [-1, 0, 1]
              for j in [-1, 0, 1] for k in [-1, 0, 1]]


def move_wins(white, i, j, k):
    x0 = np.array((i, j, k))
    for d in directions:
        for s in range(-3, 0):
            n = 0
            for t in range(s, s+4):
                x = x0 + t*d
                if t == 0:
                    n = n + 1
                elif min(x) > -1 and max(x) < 4:
                    n = n + white[x[0], x[1], x[2]]
            if n > 3:
                return 1
    return 0