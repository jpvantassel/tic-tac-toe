"""Define board transform and inverse transform."""

import numpy as np
import unittest


def board_transform(state, trans_number):
    """Perform board transform based on provided transform number
    (trans_number)."""

    if trans_number == 0:
        return state
    elif trans_number == 1:
        return np.flip(np.transpose(state), 1)
    elif trans_number == 2:
        return np.flip(np.flip(np.transpose(state), 1), 0)
    elif trans_number == 3:
        return np.transpose(state)
    elif trans_number == 4:
        return np.flip(np.flip(state, 0), 1)
    elif trans_number == 5:
        return np.flip(state, 1)
    elif trans_number == 6:
        return np.flip(state, 0)
    elif trans_number == 7:
        return np.flip(np.transpose(state), 0)
    else:
        raise ValueError("trans_number must be between 0 and 7.")


def board_itransform(state, trans_number):
    """Perform inverse board transform based on provided transform
    number (trans_number)."""

    if trans_number == 0:
        return state
    elif trans_number == 1:
        return np.transpose(np.flip(state, 1))
    elif trans_number == 2:
        return np.transpose(np.flip(np.flip(state, 0), 1))
    elif trans_number == 3:
        return np.transpose(state)
    elif trans_number == 4:
        return np.flip(np.flip(state, 1), 0)
    elif trans_number == 5:
        return np.flip(state, 1)
    elif trans_number == 6:
        return np.flip(state, 0)
    elif trans_number == 7:
        return np.transpose(np.flip(state, 0))
    else:
        raise ValueError("trans_number must be between 0 and 7.")


class Test_Transform(unittest.TestCase):
    def assertArrayEqual(self, array1, array2):
        self.assertListEqual(array1.tolist(), array2.tolist())

    def test_transform(self):
        state = np.array([[1, 2, 0], [2, 0, 1], [2, 2, 2]])

        # Transform #0
        known_state = np.array([[1, 2, 0], [2, 0, 1], [2, 2, 2]])
        test_state = board_transform(state, 0)
        self.assertArrayEqual(known_state, test_state)

        # Transform #1
        known_state = np.array([[2, 2, 1], [2, 0, 2], [2, 1, 0]])
        test_state = board_transform(state, 1)
        self.assertArrayEqual(known_state, test_state)

        # Transform #2
        known_state = np.array([[2, 1, 0], [2, 0, 2], [2, 2, 1]])
        test_state = board_transform(state, 2)
        self.assertArrayEqual(known_state, test_state)

        # Transform #3
        known_state = np.array([[1, 2, 2], [2, 0, 2], [0, 1, 2]])
        test_state = board_transform(state, 3)
        self.assertArrayEqual(known_state, test_state)

        # Transform #4
        known_state = np.array([[2, 2, 2], [1, 0, 2], [0, 2, 1]])
        test_state = board_transform(state, 4)
        self.assertArrayEqual(known_state, test_state)

        # Transform #5
        known_state = np.array([[0, 2, 1], [1, 0, 2], [2, 2, 2]])
        test_state = board_transform(state, 5)
        self.assertArrayEqual(known_state, test_state)

        # Transform #6
        known_state = np.array([[2, 2, 2], [2, 0, 1], [1, 2, 0]])
        test_state = board_transform(state, 6)
        self.assertArrayEqual(known_state, test_state)

        # Transform #7
        known_state = np.array([[0, 1, 2], [2, 0, 2], [1, 2, 2]])
        test_state = board_transform(state, 7)
        self.assertArrayEqual(known_state, test_state)

    def test_forwardtransform(self):
        state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        for value in range(8):
            reverse = board_itransform(state, value)
            forward = board_transform(reverse, value)
            self.assertArrayEqual(state, forward)

    def test_inversetransform(self):
        state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        for value in range(8):
            forward = board_transform(state, value)
            reverse = board_itransform(forward, value)
            self.assertArrayEqual(state, reverse)


if __name__ == "__main__":
    unittest.main()
