"""
This function takes the current utility of the board 
(3x3 numpy array), and decides where the computer should play (i.e., 
the move will maximize utility).
"""

import numpy as np
import unittest

# TODO: Refactor this into two functions
def decideplay(utility, transform):
    # Find location of maximum utility
    rows, cols = np.where(utility == np.nanmax(utility))
    # Could have multiple locals with same utility, if so pick randomly
    rid = np.random.randint(1, len(rows)) if rows.size > 1 else 0
    cid = np.random.randint(1, len(cols)) if cols.size > 1 else 0
    # Select row and column
    tranrow = rows[rid]
    trancol = cols[cid]

    ex = np.zeros((3, 3))
    ex[tranrow][trancol] = 1
    # Define reverse transformations
    if transform is 0:
        ex = np.transpose(np.flip(ex, 1))
    elif transform is 1:
        ex = np.transpose(np.flip(np.flip(ex, 0), 1))
    elif transform is 2:
        ex = np.transpose(ex)
    elif transform is 3:
        ex = np.flip(np.flip(ex, 1), 0)
    elif transform is 4:
        ex = np.flip(ex, 1)
    elif transform is 5:
        ex = np.flip(ex, 0)
    elif transform is 6:
        ex = np.transpose(np.flip(ex, 0))
    elif transform is 7:
        ex = ex
    else:
        raise ValueError("transform {} is invalid.".format(transform))

    # Define transformed locations
    currow, curcol = np.where(ex == 1)
    return (currow[0], curcol[0], tranrow, trancol)


class TestModuleImport(unittest.TestCase):
    def test_knownmove(self):
        game = np.array([[-np.inf, -np.inf, 9], [0, 0, -np.inf], [2, 1, 0]])
        srow, scol, trow, tcol = decideplay(game, 7)
        self.assertEqual(srow, trow)
        self.assertEqual(scol, tcol)
        self.assertEqual(srow, 0)
        self.assertEqual(scol, 2)

    def test_randmove(self):
        game = np.array([[9, -np.inf, 1], [5, 9, 8], [-np.inf, 1, 2]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0, 1])
        self.assertIn(col, [0, 1])
        game = np.array([[7, 7, 7], [-np.inf, 2, 0], [0, 0, 1]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0, 1])
        self.assertIn(col, [0, 1, 2])
        game = np.array([[7, 7, 7], [7, 7, 7], [0, 0, 1]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0, 1, 2])
        self.assertIn(col, [0, 1, 2])
        game = np.array([[0, 7, 0], [0, 7, 0], [0, 7, 1]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0, 1, 2])
        self.assertIn(col, [1])
        game = np.array([[9, 0, 9], [0, 7, 0], [0, 7, 1]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0])
        self.assertIn(col, [0, 2])
        game = np.array([[9, 0, 0], [0, 7, 0], [9, 7, 1]])
        row, col, _, _ = decideplay(game, 7)
        self.assertIn(row, [0, 2])
        self.assertIn(col, [0])

    def test_transform(self):
        util = np.array([[5, 2, 1], [6, 3, 0], [7, 4, 9]])
        rrow, rcol, trow, tcol = decideplay(util, 0)
        self.assertEqual(rrow, 0)
        self.assertEqual(rcol, 2)
        self.assertEqual(trow, 2)
        self.assertEqual(tcol, 2)
        util = np.array([[5, 2, 1], [9, 3, 0], [7, 4, 0]])
        row, col, _, _ = decideplay(util, 1)
        self.assertEqual(row, 2)
        self.assertEqual(col, 1)
        row, col, _, _ = decideplay(util, 2)
        self.assertEqual(row, 0)
        self.assertEqual(col, 1)
        row, col, _, _ = decideplay(util, 3)
        self.assertEqual(row, 1)
        self.assertEqual(col, 2)
        row, col, _, _ = decideplay(util, 4)
        self.assertEqual(row, 1)
        self.assertEqual(col, 2)
        row, col, _, _ = decideplay(util, 5)
        self.assertEqual(row, 1)
        self.assertEqual(col, 0)
        row, col, _, _ = decideplay(util, 6)
        self.assertEqual(row, 0)
        self.assertEqual(col, 1)
        util = np.array([[5, 2, 1], [1, 3, 0], [7, 9, 0]])
        rrow, rcol, trow, tcol = decideplay(util, 5)
        self.assertEqual(rrow, 0)
        self.assertEqual(rcol, 1)
        self.assertEqual(trow, 2)
        self.assertEqual(tcol, 1)

if __name__ == "__main__":
    unittest.main()
