import unittest

import numpy as np

from mcts import perform_mcts


class MCTSTest(unittest.TestCase):
    def test(self):
        def predict(something):
            return np.asarray([((x+1)/15, x % 2) for x in range(5)])

        def make_step(state, action):
            return np.zeros(5)

        print(perform_mcts(None, 5000, predict, make_step))
        self.assertEqual(4, 4)
