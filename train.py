"""Module to train tic-tac-toe program."""

import numpy as np
import pickle
import os
from checkwin import checkwin
from decideplay import decideplay
from evalboard import recall_board, diffuse_utility, nd3_to_tuple, tuple_to_nd3
from transform import board_transform, board_itransform
from updateboard import make_move
from updateutility import update_utility, flip_player

#-----------------------------------------------------------------------
# Beginning of Inputs

# Player 1 (i.e. p1) and Player 2 (i.e. p2) numeric representation.
p1 = 1
p2 = 2

# Should training consider previously received rewards or punishments.
use_prob_p1 = False
use_prob_p2 = False

# Number of simulations to perform during training.
number_simulation = 10000

# Name of training file for p1 and p2
file_name_p1 = "training_p1_"+str(number_simulation)
file_name_p2 = "training_p2_"+str(number_simulation)

# Name of file for learning curve (i.e. LC) may be viewed using vis_training.ipynb.
file_name_lc = "LC_"+str(number_simulation)

# Reward for win and punishment for loss.
reward_win = 2
punish_loss = -1

# End of Inputs
#-----------------------------------------------------------------------

# Load previous training sets
boards_played = {}
fnames = {p1: file_name_p1, p2: file_name_p2}
for player in (p1, p2):
    if os.path.isfile(fnames[player]):
        with open(fnames[player], "rb") as f:
            boards_played[player] = pickle.load(f)
    else:
        boards_played[player] = {}

# Loop through a number of models
training_summary = []
for simulation in range(number_simulation):

    # Initialize new game
    state = np.zeros((3, 3))
    win = False
    draw = False
    current_game_boards = {p1: [], p2: []}
    current_game_move = {p1: [], p2: []}

    # Loop through a single game, at most 5 moves for a single player
    for game_move in range(5):
        # Switch between players
        for current_player in (p1, p2):

            # Check if board has been seen before
            seen_before, key, trans_number = recall_board(state,
                                                          boards_played[current_player],
                                                          p1=p1,
                                                          p2=p2)

            # Logic to decide if previous utility will be used
            if current_player == p1:
                use_prob = True if use_prob_p1 else False
            elif current_player == p2:
                use_prob = True if use_prob_p2 else False
            else:
                raise RuntimeError("Player unknown!")

            # If seen before and using past info -> recall
            # If seen before and not using prob -> set diffuse
            # If not seen before -> diffuse
            if seen_before:
                if use_prob:
                    board_state = boards_played[current_player][key]
                else:
                    board_state = diffuse_utility(tuple_to_nd3(key), p1=p1, p2=p2)
            else:
                board_state = diffuse_utility(state, p1=p1, p2=p2)
                boards_played[current_player].update({key: board_state})

            # Transformed gameboard key
            current_game_boards[current_player] += [key]

            # Decide the move
            true_move, tran_move = decideplay(board_state, trans_number)

            # Save tranformed movement
            current_game_move[current_player] += [tran_move]

            # Make the move, and update state
            state = make_move(state, true_move, current_player)

            # Check if there is a winner, after three moves, as none before.
            if game_move >= 2:
                win = checkwin(state, p1=p1, p2=p2)
                if win:
                    winning_player = current_player
                    losing_player = p1 if current_player == p2 else p2
                    break
                elif ((game_move == 4) & (current_player == p1)):
                    draw = True
                    break
            if win | draw:
                break
        if win | draw:
            break

    # Update utility
    if win:

        # Update player 1
        boards_played = update_utility(boards_played,
                                       current_game_boards,
                                       current_game_move,
                                       p1,
                                       winning_player,
                                       losing_player,
                                       reward_win,
                                       punish_loss,
                                       flag_indirect=True,
                                       )
        # Update player 2
        boards_played = update_utility(boards_played,
                                       current_game_boards,
                                       current_game_move,
                                       p2,
                                       winning_player,
                                       losing_player,
                                       reward_win,
                                       punish_loss,
                                       flag_indirect=True,
                                       )

    # Save training, win p1=1, win p2=2, tie=0
    training_summary += [winning_player] if win else [0]

# Save out boards played during training.
for player in (p1, p2):
    with open(fnames[player], "wb") as f:
        pickle.dump((boards_played[player]), f)

# Save win, loss, tie training information.
with open(file_name_lc, "wb") as f:
    pickle.dump(training_summary, f)
