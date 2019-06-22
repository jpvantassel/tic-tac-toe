"""
Determine probability distribution of current board by:
1) Check if the current board (or any equivalent) has been seen before.
2) If so, load previous probability.
3) If not, make diffuse assumption.
4) Pass on the transformed board's probability. 
"""

import numpy as np
import unittest
from transform import board_transform


def evalboard(state, boards_played, p1=1, p2=2):
    # Check if the board (or eqivalent) has been seen before
    for trans_number in range(8):
        trans_state = board_transform(state, trans_number)
        key = nd3_to_tuple(trans_state)

    # If it is found return boards utility
        if key in boards_played.keys():
            return (boards_played[key], key, trans_number)

    # If not set diffuse condition
    return (set_diffuse(state, p1=p1, p2=p2), key, 7, True)


def set_diffuse(state, p1=1, p2=2):
    # Set all values not equal to p1 or p2 to diffuse utility
    row, col = np.where((state != p1) & (state != p2))
    utility = np.ones((3, 3))*-np.inf
    diffuse_utility = 0
    for rid, cid in zip(row, col):
        utility[rid][cid] = diffuse_utility
    return utility


def nd3_to_tuple(array):
    return (tuple(array[0]), tuple(array[1]), tuple(array[2]))


class TestModuleImport(unittest.TestCase):
    def test_setdiffuse(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_util = np.zeros((3, 3))
        self.assertListEqual(set_diffuse(board, p1=1, p2=2).tolist(),
                             known_util.tolist(),
                             )

        board = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        known_util = np.array([[-np.inf, 0, -np.inf],
                               [-np.inf, -np.inf, 0],
                               [0, 0, 0]]
                              )
        test_util = set_diffuse(board, p1=1, p2=2)
        for known, test in zip(known_util.tolist(), test_util.tolist()):
            self.assertListEqual(known, test)

    def test_evalboard_initial(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_util = np.zeros((3, 3))
        known_key = nd3_to_tuple(board)
        a, b, c, d = evalboard(board, {}, p1=1, p2=2)
        self.assertListEqual(a.tolist(), known_util.tolist())
        self.assertTupleEqual(b, known_key)
        self.assertEqual(c, 7)
        self.assertTrue(d)

    def test_evalboard_second(self):
        board = np.array([[0, 2, 0], [2, 1, 2], [1, 1, 0]])
        util = np.array([[1, -np.inf, 3],
                         [-np.inf, -np.inf, -np.inf],
                         [-np.inf, -np.inf, 9]])
        key = nd3_to_tuple(board)
        a, b, c = evalboard(np.flip(board, 0), {key: util}, p1=1, p2=2)
        self.assertListEqual(a.tolist(), util.tolist())
        self.assertTupleEqual(b, key)
        self.assertEqual(c, 5)

    def test_transform(self):
        board_1 = np.array([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        a1, b1, c1, d1 = evalboard(board_1, {}, p1=1, p2=2)
        util = np.array([[-np.inf, -np.inf, 0],
                         [0, 0, 0],
                         [0, 0, 0]])
        self.assertListEqual(a1.tolist(), util.tolist())
        key = nd3_to_tuple(board_1)
        self.assertTupleEqual(b1, key)
        self.assertEqual(c1, 7)
        self.assertTrue(d1)

        board_2 = np.array([[1, 0, 0], [1, 0, 0], [0, 0, 0]])
        a2, b2, c2 = evalboard(board_2, {b1: a1}, p1=1, p2=2)
        self.assertListEqual(a2.tolist(), a1.tolist())
        self.assertTupleEqual(b2, b1)
        self.assertEqual(c2, 2)


if __name__ == "__main__":
    unittest.main()
