from typing import TypeVar, Generic
S = TypeVar('S')


class Game(Generic[S]):
    STATE: type

    def initial_state(self) -> S:
        'Returns the initial state of the game.'
        pass

    def num_actions(self) -> int:
        'Returns the number of valid actions.'
        pass

    def valid_action(self, state: S, action: int) -> bool:
        'Returns whether an action is valid in the given state or leads to the opponent winning.'
        pass

    def step(self, state: S, action: int) -> S:
        'Performs a valid action and returns the resulting state.'
        pass

    def winning_action(self, state: S, action: int) -> bool:
        'Returns whether a valid action leads to a winning state for the performing player.'
        pass

    def terminal_state(self, state: S) -> bool:
        'Returns whether a state is terminal.'
        pass

    def evaluate_state(self, state: S) -> int:
        'Returns -1 iff the current player won the game, 1 if the other player won the game or 0 otherwise.'
        pass
