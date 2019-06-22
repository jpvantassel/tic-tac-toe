"""
Perform board transformation, and return transformed board.
"""


import numpy as np
import unittest


def board_transform(state, trans_number):
    # 90deg: 0
    if trans_number is 0:
        return np.flip(np.transpose(state), 1)
    # 90deg + flipud: 1
    elif trans_number is 1:
        return np.flip(np.flip(np.transpose(state), 1), 0)
    # 90deg + fliplr: 2
    elif trans_number is 2:
        return np.transpose(state)
    # 180deg: 3
    elif trans_number is 3:
        return np.flip(np.flip(state, 0), 1)
    # 180deg + flipud: 4
    elif trans_number is 4:
        return np.flip(state, 1)
    # 180deg + fliplr: 5
    elif trans_number is 5:
        return np.flip(state, 0)
    # 270deg: 6
    elif trans_number is 6:
        return np.flip(np.transpose(state), 0)
    # 0deg
    elif trans_number is 7:
        return state
    else:
        raise ValueError("trans_number must be between 0 and 7.")


class TestModuleImport(unittest.TestCase):
    def test_transform(self):
        state = np.array([[1, 2, 3], [7, 8, 9], [4, 5, 6]])

        known_state = np.array([[4, 7, 1], [5, 8, 2], [6, 9, 3]])
        test_state = board_transform(state, 0)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[6, 9, 3], [5, 8, 2], [4, 7, 1]])
        test_state = board_transform(state, 1)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[1, 7, 4], [2, 8, 5], [3, 9, 6]])
        test_state = board_transform(state, 2)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[6, 5, 4], [9, 8, 7], [3, 2, 1]])
        test_state = board_transform(state, 3)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[3, 2, 1], [9, 8, 7], [6, 5, 4]])
        test_state = board_transform(state, 4)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[4, 5, 6], [7, 8, 9], [1, 2, 3]])
        test_state = board_transform(state, 5)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        known_state = np.array([[3, 9, 6], [2, 8, 5], [1, 7, 4]])
        test_state = board_transform(state, 6)
        self.assertListEqual(known_state.tolist(), test_state.tolist())

        test_state = board_transform(state, 7)
        self.assertListEqual(state.tolist(), test_state.tolist())


if __name__ == "__main__":
    unittest.main()
