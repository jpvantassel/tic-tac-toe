"""
This function takes the current utility of the board 
(3x3 numpy array), and decides where the computer should play (i.e., 
the move will maximize utility).
"""

import numpy as np
import unittest


def decideplay(utility):
    # Find location of maximum utility
    row, col = np.where(utility == np.nanmax(utility))
    # Could have multiple locals with same utility, if so pick randomly
    if row.size > 1:
        vid = np.random.randint(1, len(row))
    else:
        vid = 0
    return (row[vid], col[vid])


class TestModuleImport(unittest.TestCase):
    def test_knownmove(self):
        game = np.array([[-np.inf, -np.inf, 9], [0, 0, -np.inf], [2, 1, 0]])
        row, col = decideplay(game)
        self.assertEqual(row, 0)
        self.assertEqual(col, 2)

    def test_randmove(self):
        game = np.array([[9, -np.inf, 1], [5, 9, 8], [-np.inf, 1, 2]])
        row, col = decideplay(game)
        self.assertIn(row, [0, 1])
        self.assertIn(col, [0, 1])
        game = np.array([[7, 7, 7], [-np.inf, 2, 0], [0, 0, 1]])
        row, col = decideplay(game)
        self.assertIn(row, [0])
        self.assertIn(col, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
