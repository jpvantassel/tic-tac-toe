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
    return the current boards probability values, as well as the
    tranformation if required.
    """
    # Check board and equvialents
    # Check 90deg: 0
    options = [np.flip(np.transpose(state), 1)]
    # flipud: 1
    options += [np.flip(np.flip(np.transpose(state), 1), 0)]
    # fliplr: 2
    options += [np.transpose(state)]
    # Check 180deg rotation: 3
    options += [np.flip(np.flip(state, 0), 1)]
    # flipud: 4
    options += [np.flip(state, 1)]
    # fliplr: 5
    options += [np.flip(state, 0)]
    # Check 270deg rotation: 6
    options += [np.flip(np.transpose(state), 0)]
    # Check as-is: 7
    options += [state]

    count = 0
    for option in options:
        key = nd3_to_tuple(option)
        if key in boards_played.keys():
            return (boards_played[key], key, count)
        count += 1
    return (setdiffuse(state, p1=p1, p2=p2),
            key,
            7,
            True,
            )


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
        known_util = np.array([[-np.inf, 0, -np.inf],
                               [-np.inf, -np.inf, 0],
                               [0, 0, 0]]
                              )
        test_util = setdiffuse(board, p1=1, p2=2)
        for known, test in zip(known_util.tolist(), test_util.tolist()):
            self.assertListEqual(known, test)

    def test_evalboard(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_prob = np.zeros((3, 3))
        known_key = nd3_to_tuple(board)
        a, b, c, d = evalboard(board, {}, p1=1, p2=2)
        self.assertListEqual(a.tolist(), known_prob.tolist())
        self.assertTupleEqual(b, known_key)

    def test_transform(self):
        board_1 = np.array([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        a1, b1, c1, d1 = evalboard(board_1, {}, p1=1, p2=2)

        self.assertEqual(c1, 0)
        self.assertTrue(d1)
        board_2 = np.array([[1, 0, 0], [1, 0, 0], [0, 0, 0]])
        _, _, c2 = evalboard(board_2, {b1: a1}, p1=1, p2=2)
        self.assertEqual(c2, 2)


if __name__ == "__main__":
    unittest.main()
