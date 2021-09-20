import numpy as np

from game import Game

from tf_sogo import evaluate


class Sogo(Game[np.ndarray]):
    @staticmethod
    def action_x(num: int):
        return num % 4

    @staticmethod
    def action_y(num: int):
        return num // 4

    @staticmethod
    def action_z(state: np.ndarray, x: int, y: int):
        z = 0
        while state[x, y, z, 0] or state[x, y, z, 1]:
            z += 1
        return z

    def initial_state(self) -> np.ndarray:
        'Returns the initial state of the game.'
        return np.zeros((4, 4, 4, 3), dtype=np.int32)

    def num_actions(self) -> int:
        'Returns the number of valid actions.'
        return 17

    def valid_action(self, state: np.ndarray, action: int) -> bool:
        'Returns whether an action is valid in the given state or leads to the opponent winning.'
        return action == 16 or \
            not state[self.action_x(action), self.action_y(action), 3, 0] and \
            not state[self.action_x(action), self.action_y(action), 3, 1]

    def step(self, state: np.ndarray, action: int) -> np.ndarray:
        'Performs a valid action and returns the resulting state.'
        new_state = np.copy(state)
        player = state[0, 0, 0, 2]
        new_state[:, :, :, 2] = 1 - player
        if action < 16:
            x = self.action_x(action)
            y = self.action_y(action)
            z = self.action_z(state, x, y)
            new_state[x, y, z, player] = 1
        return new_state

    def winning_action(self, state: np.ndarray, action: int) -> bool:
        'Returns whether a valid action leads to a winning state for the performing player.'
        pass

    def terminal_state(self, state: np.ndarray) -> bool:
        'Returns whether a state is terminal.'
        return np.sum(state[..., 0:2]) == 64 or not self.evaluate_state(state) == 0

    def evaluate_state(self, state: np.ndarray) -> int:
        'Returns -1 iff the current player won the game, 1 if the other player won the game or 0 otherwise.'        
        player = state[0, 0, 0, 2]
        if evaluate(state[np.newaxis, :, :, :, 0]):
            return 1 if player else -1
        if evaluate(state[np.newaxis, :, :, :, 1]):
            return -1 if player else 1
        return 0
        
        