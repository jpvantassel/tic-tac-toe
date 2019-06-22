"""
Update utility for both players, using all moves.
"""

import numpy as np
import unittest
from transform import board_transform
from inversetransform import board_itransform
from evalboard import nd3_to_tuple


def update_utility_winner(boards_played, game_boards, game_moves, winner, loser, reward, punishment):
    # Apply reward - to winner
    for key, move in zip(game_boards[winner], game_moves[winner]):
        boards_played[winner][key][move[0]][move[1]] += reward

    # Apply indirect punishment - to winner
    for key, move in zip(game_boards[loser], game_moves[loser]):
        found=False
        # Check if board (or transformation) exists
        for trans_number in range(8):
            trans_state = board_transform(np.array(key), trans_number)
            flip_trans_state = flip_player(trans_state)
            test_key = nd3_to_tuple(flip_trans_state)
            # If is does, update.
            if test_key in boards_played[winner]:
                boards_played[winner][test_key][move[0]][move[1]] += punishment
                found=True
                break
        # If not, append.
        if not found:
            delta = np.zeros((3,3))
            delta[move[0]][move[1]] += punishment
            boards_played[winner].update({test_key: delta})
    return boards_played

def update_utility_loser(boards_played, game_boards, game_moves, winner, loser, reward, punishment):
    # Apply punishment - to loser
    for key, move in zip(game_boards[loser], game_moves[loser]):
        boards_played[loser][key][move[0]][move[1]] += punishment

    # Apply indirect reward - to loser
    for key, move in zip(game_boards[winner], game_moves[winner]):
        found = False
        # Check if board (or transformation) exists
        for trans_number in range(8):
            trans_state = board_transform(np.array(key), trans_number)
            flip_trans_state = flip_player(trans_state)
            test_key = nd3_to_tuple(flip_trans_state)
            # If is does, update.
            if test_key in boards_played[loser]:
                boards_played[loser][test_key][move[0]][move[1]] += reward
                found = True
                break
        # If not, append.
        if not found:
            delta = np.zeros((3,3))
            delta[move[0]][move[1]] += reward
            boards_played[loser].update({test_key: delta})
    return boards_played

def flip_player(state, p1=1, p2=2):
    p1_rows, p1_cols = np.where(state == p1)
    p2_rows, p2_cols = np.where(state == p2)

    for row, col in zip(p1_rows, p1_cols):
        state[row][col] = p2

    for row, col in zip(p2_rows, p2_cols):
        state[row][col] = p1

    return state


class TestModuleImport(unittest.TestCase):
    def test_flip_player(self):
        state = np.array([[1, 2, 1], [2, 1, 2], [1, 2, 1]])
        flip_true = np.array([[2, 1, 2], [1, 2, 1], [2, 1, 2]])
        flip_test = flip_player(state, p1=1, p2=2)
        self.assertListEqual(flip_true.tolist(), flip_test.tolist())

    def test_update(self):
        boards_played = {1: {((1, 1, 0), (2, 0, 2), (1, 2, 1)): np.zeros((3, 3))},
                         2: {((1, 1, 0), (2, 0, 0), (1, 2, 1)): np.zeros((3, 3))}}
        game_boards = {1: [((1, 1, 0), (2, 0, 2), (1, 2, 1))],
                       2: [((1, 1, 0), (2, 0, 0), (1, 2, 1))]}
        game_moves = {1: [(0, 2)],
                      2: [(1, 2)]}
        winner = 1
        loser = 2
        reward = 1
        punishment = -1
        boards = update_utility_winner(boards_played, game_boards, game_moves,
                                winner, loser, reward, punishment)
        self.assertListEqual(boards[winner][game_boards[winner][0]].tolist(),
                             [[0, 0, 1], [0, 0, 0], [0, 0, 0]])
        self.assertListEqual(boards[winner][nd3_to_tuple(flip_player(np.array(game_boards[loser][0])))].tolist(),
                             [[0, 0, 0], [0, 0, -1], [0, 0, 0]])

        boards = update_utility_loser(boards_played, game_boards, game_moves,
                                winner, loser, reward, punishment)
        self.assertListEqual(boards[loser][game_boards[loser][0]].tolist(),
                             [[0, 0, 0], [0, 0, -1], [0, 0, 0]])
        self.assertListEqual(boards[loser][nd3_to_tuple(flip_player(np.array(game_boards[winner][0])))].tolist(),
                             [[0, 0, 1], [0, 0, 0], [0, 0, 0]])        


if __name__ == "__main__":
    unittest.main()
