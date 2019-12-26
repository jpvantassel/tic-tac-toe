"""This file contains functions for plotting out the current board
state and utility."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import unittest


def determinecell(board, pt, bounds_x, bounds_y):
    # Determine X cell
    for col in range(len(bounds_x)-1):
        if ((pt[0] > bounds_x[col]) & (pt[0] < bounds_x[col+1])):
            break
    # Determine Y cell
    for row in range(len(bounds_y)-1):
        if ((pt[1] > bounds_y[row]) & (pt[1] < bounds_y[row+1])):
            break
    # Check if cell is empty and its a allowable move
    good_move = True if board[row][col] == 0 else False
    return (row, col, good_move)


def updateplot(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()


def plot_state(board, ax=None):
    x = [1, 2, 3]
    y = [3, 2, 1]

    ax_was_provided = True if ax is not None else False
    if ax == None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
        fig.canvas.manager.window.wm_geometry("+500+100")

    # Show current board state
    cmap = plt.get_cmap("plasma")
    # colors = [["#deeaee"], #violet
    #           ["#b1cbbb"], # pink
    #           ["#eea29a"]] # green
    # colors = tuple(int(colors[i:i+2], 16) for i in (0, 2, 4)))
    # cmap = mpl.colors.ListedColormap(colors)

    ax.imshow(board, cmap=cmap)
    linewidth = 5
    ax.plot([0.5, 0.5], [-0.5, 2.5], '-k', linewidth=linewidth)
    ax.plot([1.5, 1.5], [-0.5, 2.5], '-k', linewidth=linewidth)
    ax.plot([-.5, 2.5], [0.5, 0.5], '-k', linewidth=linewidth)
    ax.plot([-.5, 2.5], [1.5, 1.5], '-k', linewidth=linewidth)

    # Loop over data dimensions and create text showing the values.
    for row in range(len(x)):
        for col in range(len(y)):
            if board[row][col] == 1:
                txt = 'X'
            elif board[row][col] == 2:
                txt = 'O'
            else:
                txt = ' '
            ax.text(col, row, txt, ha="center", va="center",
                    color="k", size=50)
    ax.axis('off')
    return (ax) if ax_was_provided else (fig, ax)


def plot_utility(utility, ax=None):
    x = [1, 2, 3]
    y = [3, 2, 1]

    if ax is None:
        _, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

    cmap = plt.get_cmap("winter")
    ax.imshow(utility, cmap=cmap)
    # Loop over data dimensions and create text showing the value.
    for row in range(len(y)):
        for col in range(len(x)):
            if utility[row, col] == -np.inf:
                txt = ' '
            else:
                txt = int(utility[row, col])
            ax.text(col, row, txt, ha="center", va="center",
                    color="k", size=30)
    ax.set_title("Board Utility")
    ax.axis('off')
    return ax


def plotforhuman(board, current_player):
    bounds_x = [-0.5, 0.5, 1.5, 2.5]
    bounds_y = [-0.5, 0.5, 1.5, 2.5]
    _, ax = plot_state(board)

    updateplot('Click Anywhere to Begin')
    plt.waitforbuttonpress()
    good_move = False
    txt = 'X' if current_player == 1 else 'O'

    while True:
        updateplot('Select the Desired Cell')
        while not good_move:
            pt = plt.ginput(1, timeout=-1)
            if len(pt) == 0:
                good_move = False
            else:
                row, col, good_move = determinecell(board, pt[-1],
                                                    bounds_x, bounds_y)
            if not good_move:
                updateplot('Move is not Allowed. Select Again')

        text = ax.text(col, row, txt, ha="center", va="center",
                       color="k", size=50)
        updateplot('Happy with Move? Key=Yes, Mouse=No.')
        if plt.waitforbuttonpress():

            break
        text.remove()
        good_move = False

    return (row, col)


def view_state_and_utility(state, utility):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    plot_state(state, axs[0])
    plot_utility(utility, axs[1])
    fig.tight_layout()
    plt.show()


class Test_Plot(unittest.TestCase):
    def test_determinecell(self):
        bounds_x = [-0.5, 0.5, 1.5, 2.5]
        bounds_y = [-0.5, 0.5, 1.5, 2.5]
        board = np.array([[1, 2, 0], [0, 0, 0], [1, 2, 2]])
        pt = (0, 0)
        row, col, good = determinecell(board, pt, bounds_x, bounds_y)
        self.assertEqual(row, 0)
        self.assertEqual(col, 0)
        self.assertFalse(good)
        pt = (1, 1)
        row, col, good = determinecell(board, pt, bounds_x, bounds_y)
        self.assertEqual(row, 1)
        self.assertEqual(col, 1)
        self.assertTrue(good)
        pt = (2, 2)
        row, col, good = determinecell(board, pt, bounds_x, bounds_y)
        self.assertEqual(row, 2)
        self.assertEqual(col, 2)
        self.assertFalse(good)

    def test_plotforhuman(self):
        # Test move for player 1
        board = np.array([[1, 2, 0], [0, 0, 0], [1, 2, 2]])
        row, col = plotforhuman(board, 1)
        self.assertEqual(row, 1)
        self.assertEqual(col, 0)

        # Test move for player 2
        board = np.array([[1, 2, 0], [0, 0, 0], [1, 2, 2]])
        row, col = plotforhuman(board, 2)
        self.assertEqual(row, 1)
        self.assertEqual(col, 1)


if __name__ == "__main__":
    unittest.main()
