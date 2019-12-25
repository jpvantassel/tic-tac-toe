"""Functions to update board utility."""

import numpy as np
import unittest
from transform import board_transform, board_itransform
from evalboard import diffuse_utility, nd3_to_tuple, tuple_to_nd3


def update_utility(boards_played, game_boards, game_moves,
                   player, winner, loser, reward, punishment,
                   flag_indirect=True):

    # Apply direct reward/punishment to player
    for key, move in zip(game_boards[player], game_moves[player]):
        stimulis = reward if player is winner else punishment
        boards_played[player][key][move[0]][move[1]] += stimulis

    # Apply indirect reward/punishment based on opponent's movement
    if flag_indirect:
        opponent = loser if player == winner else winner
        stimulis = punishment if player == winner else reward
        for key, move in zip(game_boards[opponent], game_moves[opponent]):
            row, col = move
            # Check if board (or transformation) exists in player
            for trans_number in range(8):
                trans_state = board_transform(tuple_to_nd3(key), trans_number)
                flip_trans_state = flip_player(trans_state)
                test_key = nd3_to_tuple(flip_trans_state)
                # If it it, update.
                if test_key in boards_played[player]:
                    boards_played[player][test_key][row][col] += stimulis
                    break
            # If not, append.
            else:
                state = tuple_to_nd3(key)
                flipped_state = flip_player(state)
                utility = diffuse_utility(flipped_state, p1=player, p2=opponent)
                utility[row][col] += stimulis
                boards_played[player].update({nd3_to_tuple(flipped_state): utility})

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
    def assertArrayEqual(self, array1, array2):
        self.assertListEqual(array1.tolist(), array2.tolist())

    def test_flip_player(self):
        state = np.array([[1, 2, 1], [2, 1, 2], [1, 2, 1]])
        flip_true = np.array([[2, 1, 2], [1, 2, 1], [2, 1, 2]])
        flip_test = flip_player(state, p1=1, p2=2)
        self.assertArrayEqual(flip_true, flip_test)

    def test_update(self):
        x = -1*np.inf
        boards_played = {1: {((1, 2, 0),
                              (2, 0, 0),
                              (1, 2, 1)): np.array([[x, x, 0],
                                                    [x, 0, 0],
                                                    [x, x, x]])},
                         2: {((1, 2, 0),
                              (2, 0, 1),
                              (1, 2, 1)): np.array([[x, x, 0],
                                                    [x, 0, x],
                                                    [x, x, x]])}}

        game_boards = {1: [((1, 2, 0), (2, 0, 0), (1, 2, 1))],
                       2: [((1, 2, 0), (2, 0, 1), (1, 2, 1))]}
        game_moves = {1: [(1, 2)],
                      2: [(1, 1)]}
        winner = 2
        loser = 1
        reward = 1
        punishment = -1

        # Update utlity for player 1 -> i.e. the loser
        boards = update_utility(boards_played, game_boards, game_moves,
                                1, winner, loser, reward, punishment, flag_indirect=True)
        # Check loss was punished.
        self.assertArrayEqual(boards[loser][game_boards[loser][0]],
                             np.array([[x, x, 0], [x, 0, -1], [x, x, x]]))
        # Check that observed win was rewarded.
        winning_board = nd3_to_tuple(flip_player(np.array(game_boards[winner][0])))
        self.assertArrayEqual(boards[loser][winning_board],
                             np.array([[x, x, 0], [x, 1, x], [x, x, x]]))


        # Update utility for player 2 -> i.e. the winner
        updated_boards_played = update_utility(boards_played, game_boards, game_moves,
                                               2, winner, loser, reward, punishment, flag_indirect=True)
        # Check win was rewarded.
        self.assertArrayEqual(updated_boards_played[winner][game_boards[winner][0]],
                              np.array([[x, x, 0], [x, 1, x], [x, x, x]]))
        # Check that observed loss was punished.
        losing_board = nd3_to_tuple(flip_player(tuple_to_nd3(game_boards[loser][0])))
        self.assertArrayEqual(updated_boards_played[winner][losing_board],
                              np.array([[x, x, 0], [x, 0, -1], [x, x, x]]))



if __name__ == "__main__":
    unittest.main()
