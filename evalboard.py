"""
Determine probability distribution of current board by:
1) Check if the current board has been seen before.
2) If so, load previous probaility.
3) If not, make diffuse assumption.
4) Pass on the board's probability. 
"""

import numpy as np
import unittest


def evalboard(state, boards_played, p1=1, p2=2):
    """
    Check if board, or any equvalent version has been seen before, and
    return the current boards probability values.
    """
    # Check board and equvialents
    # Check as-is
    options = [state]
    # # Check 90deg:
    # options += [np.flip(np.transpose(state), 1)]
    # # flipud
    # options += [np.flip(np.flip(np.transpose(state), 1), 0)]
    # # fliplr
    # options += [np.transpose(state)]
    # # Check 180deg rotation
    # options += [np.flip(np.flip(state, 0), 1)]
    # # flipud
    # options += [np.flip(state, 1)]
    # # fliplr
    # options += [np.flip(state, 0)]
    # # Check 270deg rotation
    # options += [np.flip(np.transpose(state), 0)]

    for option in options:
        key = nd3_to_tuple(option)
        if key in boards_played.keys():
            return (boards_played[key], key)
    return (setdiffuse(state, p1=p1, p2=p2), key, True)


def setdiffuse(state, p1=1, p2=2):
    # Set all values not equal to p1 or p2 to diffuse utility
    row, col = np.where((state != p1) & (state != p2))
    prob = np.ones((3, 3))*-np.inf
    dif_prob = 0
    for rid, cid in zip(row, col):
        prob[rid][cid] = dif_prob
    return prob


def nd3_to_tuple(array):
    return (tuple(array[0]), tuple(array[1]), tuple(array[2]))


class TestModuleImport(unittest.TestCase):
    def test_setdiffuse(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_util = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertListEqual(
            setdiffuse(board, p1=1, p2=2).tolist(), known_util.tolist())

        board = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        known_util = np.array(
            [[-np.inf, 0, -np.inf], [-np.inf, -np.inf, 0], [0, 0, 0]])
        test_util = setdiffuse(board, p1=1, p2=2)
        for known, test in zip(known_util.tolist(), test_util.tolist()):
            self.assertListEqual(known, test)

    def test_evalboard(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_prob = np.zeros((3, 3))
        known_key = nd3_to_tuple(board)
        b, d, c = evalboard(board, {}, p1=1, p2=2)
        self.assertListEqual(b.tolist(), known_prob.tolist())
        self.assertTupleEqual(d, known_key)


if __name__ == "__main__":
    unittest.main()
