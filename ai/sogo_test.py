import unittest

import numpy as np

from sogo import Sogo


class SogoTest(unittest.TestCase):
    def test(self):
        sogo = Sogo()
        s0 = sogo.initial_state()
        for action in [0,1,0,1,0,1,0]:
            s0 = sogo.step(s0, action)
            print(sogo.terminal_state(s0), sogo.evaluate_state(s0))
