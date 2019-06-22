"""
Perform inverse board transformation, and return transformed board.
"""


import numpy as np
import unittest
from transform import board_transform
   
def board_itransform(state, trans_number):
    # Define reverse transformations
    if trans_number is 0:
        return np.transpose(np.flip(state, 1))
    elif trans_number is 1:
        return np.transpose(np.flip(np.flip(state, 0), 1))
    elif trans_number is 2:
        return np.transpose(state)
    elif trans_number is 3:
        return np.flip(np.flip(state, 1), 0)
    elif trans_number is 4:
        return np.flip(state, 1)
    elif trans_number is 5:
        return np.flip(state, 0)
    elif trans_number is 6:
        return np.transpose(np.flip(state, 0))
    elif trans_number is 7:
        return state
    else:
        raise ValueError("trans_number must be between 0 and 7.")

class TestModuleImport(unittest.TestCase):
    def test_inversetransform(self):
        state = np.array([[1,2,3],[5,6,7],[8,9,10]])
        for value in range(8):
            forward = board_transform(state, value)
            reverse = board_itransform(forward, value)
            self.assertListEqual(state.tolist(), reverse.tolist())

if __name__ == "__main__":
    unittest.main()