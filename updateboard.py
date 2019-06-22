"""
Update the current board using a coordinate pair and the current player.
"""

import numpy as np
import unittest


def updateboard(state, coord, currentplayer):
    state[coord[0]][coord[1]] = currentplayer
    return state


class TestModuleImport(unittest.TestCase):
    def test_movep1(self):
        before = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        after = np.array([[1, 1, 1], [2, 1, 0], [0, 0, 0]])
        self.assertListEqual(updateboard(
            before, (0, 1), 1).tolist(), after.tolist())

    def test_movep2(self):
        before = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        after = np.array([[1, 2, 1], [2, 1, 0], [0, 0, 0]])
        self.assertListEqual(updateboard(
            before, (0, 1), 2).tolist(), after.tolist())


if __name__ == "__main__":
    unittest.main()
