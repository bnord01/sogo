'''Monte Carlo Tree Search'''

import math

from typing import List, Deque, Callable

from collections import deque

import numpy as np


class MCTS(object):
    '''Node in an Monte Carlo Tree Search'''

    def __init__(self, action: int, probability: float, value: float):
        self.state: np.ndarray = None
        self.visited: int = 1
        self.action: int = action
        self.probability: float = probability
        self.value: float = value
        self.children: List[MCTS] = None

    def upper_confidence_bound(self) -> float:
        'Computes the upper confidence bound used during search'
        return self.value/self.visited + self.probability/(1+self.visited)*100

    def expand(self, state: np.ndarray, predictions: np.ndarray):
        '''Expands this node, setting it's state and children'''
        self.state = state
        self.children = [MCTS(action, probability, value)
                         for action, (probability, value) in enumerate(predictions)]
        self.value = sum((child.value for child in self.children))

    def update_value(self, value: float):
        'Updates value by the given amount and increments visited'
        self.value += value
        self.visited += 1


def search(root: MCTS) -> Deque[MCTS]:
    '''Find the '''
    path: Deque[MCTS] = deque()
    path.append(root)
    while root.children:
        high_child = None
        max_bound = -math.inf
        for child in root.children:
            if child.upper_confidence_bound() > max_bound:
                high_child = child
                max_bound = child.upper_confidence_bound()
            root = high_child
            path.append(root)
    return path


def perform_mcts(state: np.ndarray, num_steps: int, predict: Callable[[np.ndarray], np.ndarray],
                 make_step: Callable[[np.ndarray, int], np.ndarray]) -> np.ndarray:
    '''Performs an monte carlo tree search'''
    root = MCTS(0, 0, 0)
    root.expand(state, predict(state))

    while num_steps > 0:
        path = search(root)
        leaf = path.pop()
        state = path[-1].state
        leaf.expand(make_step(state, leaf.action), predict(state))
        value = leaf.value
        for node in path:
            node.update_value(value)
        num_steps -= 1

    return [child.visited for child in root.children]
