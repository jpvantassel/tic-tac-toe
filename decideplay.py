"""
This function takes the current utility of the board 
(3x3 numpy array), and decides where the computer should play (i.e., 
the move will maximize utility).
"""

import numpy as np
import unittest
from transform import board_itransform

def decideplay(utility, trans_number):
    # Find location of maximum utility, rows and cols are an np.array 
    # both are the same length and have the row_id, col_id of the values
    rows, cols = np.where(utility == np.max(utility))

    # Could have multiple locals with same max utility.
    # If we do, we'll pick randomly.
    rand_id = np.random.randint(1, len(rows)) if rows.size > 1 else 0
    tran_row = rows[rand_id]
    tran_col = cols[rand_id]
    
    # tran_row and tran_col are locations on the transformed board, and not on the
    # current game board, so we need to transform them back.
    ex = np.zeros((3, 3))
    ex[tran_row][tran_col] = 1
    ex = board_itransform(ex, trans_number)
    true_row, true_col = np.where(ex == 1)
    
    # Return true_row and true_col for plotting and updating the board.
    # Return tran_row and tran_col for saving and updating game moves.
    return ( (true_row[0], true_col[0]) , (tran_row, tran_col) )


class Test_DecidePlay(unittest.TestCase):
    def test_knownmove(self):
        game = np.array([[-np.inf, -np.inf, 9], [0, 0, -np.inf], [2, 1, 0]])
        true_move, tran_move = decideplay(game, 7)
        self.assertTupleEqual(true_move, tran_move)
        self.assertTupleEqual(true_move, (0,2))

    def test_randmove(self):
        game = np.array([[9, -np.inf, 1], [5, 9, 8], [-np.inf, 1, 2]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0, 1])
        self.assertIn(true_move[1], [0, 1])

        game = np.array([[7, 7, 7], [-np.inf, 2, 0], [0, 0, 1]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0])
        self.assertIn(true_move[1], [0, 1, 2])

        game = np.array([[7, 7, 7], [7, 7, 7], [0, 0, 1]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0, 1])
        self.assertIn(true_move[1], [0, 1, 2])

        game = np.array([[0, 7, 0], [0, 7, 0], [0, 7, 1]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0, 1, 2])
        self.assertIn(true_move[1], [1])

        game = np.array([[9, 0, 9], [0, 7, 0], [0, 7, 1]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0])
        self.assertIn(true_move[1], [0, 2])

        game = np.array([[9, 0, 0], [0, 7, 0], [9, 7, 1]])
        true_move, _ = decideplay(game, 7)
        self.assertIn(true_move[0], [0, 2])
        self.assertIn(true_move[1], [0])

    def test_transform(self):
        util = np.array([[5, 2, 1], [6, 3, 0], [7, 4, 9]])
        true_move, tran_move = decideplay(util, 0)
        self.assertTupleEqual(true_move, (0,2))
        self.assertTupleEqual(tran_move, (2,2))

        true_move, tran_move = decideplay(util, 1)
        self.assertTupleEqual(true_move, (0,0))

        true_move, tran_move = decideplay(util, 2)
        self.assertTupleEqual(true_move, (2,2))
        
        true_move, tran_move = decideplay(util, 3)
        self.assertTupleEqual(true_move, (0,0))

        true_move, tran_move = decideplay(util, 4)
        self.assertTupleEqual(true_move, (2,0))

        true_move, tran_move = decideplay(util, 5)
        self.assertTupleEqual(true_move, (0,2))

        true_move, tran_move = decideplay(util, 6)
        self.assertTupleEqual(true_move, (2,0))
      

if __name__ == "__main__":
    unittest.main()
