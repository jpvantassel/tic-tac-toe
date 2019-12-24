"""Determine probability distribution of current board by:
1) Check if the current board (or any equivalent) has been seen before.
2) If so, load previous probability.
3) If not, make diffuse assumption.
4) Pass on the transformed board's probability. 
"""

import numpy as np
import unittest
from transform import board_transform


def recall_board(state, boards_played, p1=1, p2=2):
    """Determine if board (or equvialent) has been seen before."""

    # Check if the board (or eqivalent) has been seen before.
    for trans_number in range(8):
        trans_state = board_transform(state, trans_number)
        key = nd3_to_tuple(trans_state)

        # If it is found return key representing transformed board.
        if key in boards_played:
            return (True, key, trans_number)

    # Otherwise return current board.
    return (False, nd3_to_tuple(state), 0)


def diffuse_utility(state, p1=1, p2=2):
    """Use diffuse assumption to assign utility."""
    # Set all values not equal to p1 or p2 to diffuse utility
    row, col = np.where((state != p1) & (state != p2))
    utility = np.ones((3, 3))*-np.inf
    diffuse_utility = 0
    for rid, cid in zip(row, col):
        utility[rid][cid] = diffuse_utility

    # Check that do not overwrite utility value
    for util_val, state_val in zip(utility.flatten(), state.flatten()):
        if state_val == -np.inf:
            assert(util_val==-np.inf)

    return utility


def nd3_to_tuple(array):
    """Take ndarray and convert to tuples (i.e., immutable type)"""
    return (tuple(array[0]), tuple(array[1]), tuple(array[2]))


def tuple_to_nd3(key):
    """Transform key (i.e., immutable type) back to ndarray."""
    return np.array(key)


class Test_EvalBoard(unittest.TestCase):
    def assertArrayEqual(self, array1, array2):
        self.assertListEqual(array1.tolist(), array2.tolist())

    def test_diffuse(self):
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        known_util = np.zeros((3, 3))
        self.assertListEqual(diffuse_utility(board, p1=1, p2=2).tolist(),
                             known_util.tolist(),
                             )

        board = np.array([[1, 0, 1], [2, 1, 0], [0, 0, 0]])
        known_util = np.array([[-np.inf, 0, -np.inf],
                               [-np.inf, -np.inf, 0],
                               [0, 0, 0]]
                              )
        test_util = diffuse_utility(board, p1=1, p2=2)
        self.assertArrayEqual(known_util, test_util)

    def test_tuple_to_nd3(self):
        expected = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        tpl = nd3_to_tuple(expected)
        found = tuple_to_nd3(tpl)
        self.assertArrayEqual(expected, found)

    def test_recall_board(self):
        # Initial Board
        board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        seen_before, key, trans_number = recall_board(board, {}, p1=1, p2=2)

        self.assertFalse(seen_before)
        self.assertArrayEqual(board, tuple_to_nd3(key))
        self.assertEqual(0, trans_number)

        # Later move
        board = np.array([[0, 2, 0], [2, 1, 2], [1, 1, 0]])
        util = np.array([[1, -np.inf, 3],
                         [-np.inf, -np.inf, -np.inf],
                         [-np.inf, -np.inf, 9]])
        key = nd3_to_tuple(board)
        seen_before, received_key, trans_number = recall_board(np.flip(board, 0),
                                                               {key: util},
                                                               p1=1, p2=2)
        self.assertTrue(seen_before)
        self.assertArrayEqual(board, tuple_to_nd3(received_key))
        self.assertEqual(6, trans_number)

        # Later move
        board = np.array([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        seen_before, key, trans_number = recall_board(board, {}, p1=1, p2=2)
        util = np.array([[-np.inf, -np.inf, 0],
                         [0, 0, 0],
                         [0, 0, 0]])
        
        self.assertFalse(seen_before)
        self.assertArrayEqual(board, tuple_to_nd3(key))
        self.assertEqual(0, trans_number)
        
        # Later move
        board = np.array([[1, 0, 0], [1, 0, 2], [0, 0, 2]])
        key = nd3_to_tuple(np.transpose(board))
        seen_before, key, trans_number = recall_board(board, {key:diffuse_utility(board)}, p1=1, p2=2)
        self.assertTrue(seen_before)
        self.assertEqual(3, trans_number)


if __name__ == "__main__":
    unittest.main()
