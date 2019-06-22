"""
Check if someone has won the game. 
True if some has won; false otherwise.
"""
import numpy as np
import unittest

def checkwin(state, p1=1, p2=2):
    # Null hypothesis
    win=False
    # Row information
    nrows = state.shape[0]
    last_row = nrows-1
    rows = range(nrows)
    # Column information
    ncols = state.shape[1]
    last_col = ncols-1
    cols = range(ncols)
    # Check each row
    for rid in rows:
        if state[rid][0] in [p1,p2]:
            test = state[rid][0] 
            for cid in cols:
                if state[rid][cid] != test:
                    break
                elif cid==last_col:
                    win=True
    # Check each column
    for cid in cols:
        if state[0][cid] in [p1,p2]:
            test = state[0][cid] 
            for rid in rows:
                if state[rid][cid] != test:
                    break
                elif rid==last_row:
                    win=True
    # Check first diagnol
    if state[0][0] in [p1, p2]:
        test = state[0][0]
        for did in rows:
            if state[did][did] != test:
                break
            elif did==last_row:
                win=True
    # Check second diagnol
    if state[0][last_col] in [p1, p2]:
        test = state[0][last_col]
        for cid, rid in zip(range(ncols-1,-1,-1), rows):
            if state[rid][cid] != test:
                break
            elif cid == 0:
                win=True
    return win

class TestModuleImport(unittest.TestCase):

    def test_win(self):
        # Win Bottom Row
        game = np.array([[1,0,2],[2,0,2],[1,1,1]])
        self.assertTrue(checkwin(game))
        # Win First Column
        game = np.array([[1,0,2],[1,2,2],[1,0,1]])
        self.assertTrue(checkwin(game))
        # Win Diagnol
        game = np.array([[1,0,1],[2,1,2],[2,0,1]])
        self.assertTrue(checkwin(game))
        # Win Second Diagnol
        game = np.array([[0,1,2],[0,2,1],[2,2,1]])
        self.assertTrue(checkwin(game))

    def test_nowin(self):
        # Default no-win
        game = np.array([[1,0,1],[2,0,2],[1,2,1]])
        self.assertFalse(checkwin(game))
        # All zeros
        game = np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.assertFalse(checkwin(game))
    
if __name__ == '__main__':
    unittest.main()