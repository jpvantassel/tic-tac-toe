"""Functions to update the board state."""

import numpy as np
import unittest


def make_move(state, coord, currentplayer):
    """Update the current board using a coordinate pair and the current
    player."""
    row, col = coord

    if state[row, col] == -np.inf:
        raise RuntimeError("Attempted to overwrite, occupied cell.")
    
    state[row, col] = currentplayer
    return state


class Test_UpdateBoard(unittest.TestCase):
    def assertArrayEqual(self, array1, array2):
        self.assertListEqual(array1.tolist(), array2.tolist())

    def test_movep1(self):
        before = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        expected = np.array([[1, 1, 1], [2, 1, 0], [0, 0, 0]])
        self.assertArrayEqual(expected, make_move(before, (0, 1), 1))

    def test_movep2(self):
        before = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        expected = np.array([[1, 2, 1], [2, 1, 0], [0, 0, 0]])
        self.assertArrayEqual(expected, make_move(before, (0, 1), 2))


if __name__ == "__main__":
    unittest.main()
