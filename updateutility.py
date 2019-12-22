"""Functions to update board utility."""

import numpy as np
import unittest
from transform import board_transform, board_itransform
from evalboard import nd3_to_tuple


def update_utility(boards_played, game_boards, game_moves,
                   player, winner, loser, reward, punishment,
                   flag_indirect=True):
    # Apply direct reward/punishment to player
    for key, move in zip(game_boards[player], game_moves[player]):
        stimulis = reward if player is winner else punishment
        boards_played[player][key][move[0]][move[1]] += stimulis
    # Apply indirect reward/punishment based on opponent's movement
    if flag_indirect:
        opponent = loser if player is winner else winner
        stimulis = punishment if player is winner else reward
        for key, move in zip(game_boards[opponent], game_moves[opponent]):
            found = False
            # Check if board (or transformation) exists in player
            for trans_number in range(8):
                trans_state = board_transform(np.array(key), trans_number)
                flip_trans_state = flip_player(trans_state)
                test_key = nd3_to_tuple(flip_trans_state)
                # If it it, update.
                if test_key in boards_played[player]:
                    boards_played[player][test_key][move[0]][move[1]] += stimulis
                    found = True
                    break
            # If not, append.
            if not found:
                delta = np.zeros((3, 3))
                delta[move[0]][move[1]] += stimulis
                boards_played[player].update({test_key: delta})
    return boards_played


def flip_player(state, p1=1, p2=2):
    p1_rows, p1_cols = np.where(state == p1)
    p2_rows, p2_cols = np.where(state == p2)
    for row, col in zip(p1_rows, p1_cols):
        state[row][col] = p2
    for row, col in zip(p2_rows, p2_cols):
        state[row][col] = p1
    return state


class Test_UpdateUtility(unittest.TestCase):
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
        winner = 1; loser = 2; reward = 1; punishment = -1
        boards = update_utility(boards_played, game_boards, game_moves,
                                1, winner, loser, reward, punishment)
        self.assertListEqual(boards[winner][game_boards[winner][0]].tolist(),
                             [[0, 0, 1], [0, 0, 0], [0, 0, 0]])
        self.assertListEqual(boards[winner][nd3_to_tuple(flip_player(np.array(game_boards[loser][0])))].tolist(),
                             [[0, 0, 0], [0, 0, -1], [0, 0, 0]])

        boards = update_utility(boards_played, game_boards, game_moves,
                                2, winner, loser, reward, punishment)
        self.assertListEqual(boards[loser][game_boards[loser][0]].tolist(),
                             [[0, 0, 0], [0, 0, -1], [0, 0, 0]])
        self.assertListEqual(boards[loser][nd3_to_tuple(flip_player(np.array(game_boards[winner][0])))].tolist(),
                             [[0, 0, 1], [0, 0, 0], [0, 0, 0]])


if __name__ == "__main__":
    unittest.main()
