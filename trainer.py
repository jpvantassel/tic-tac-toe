import numpy as np
import pickle
import os
from checkwin import checkwin
from decideplay import decideplay
from evalboard import evalboard, setdiffuse, nd3_to_tuple
from updateboard import updateboard

# Input
p1 = 1
p2 = 2
number_simulation = 1
file_name_p1 = "training_p1_"+str(number_simulation)
file_name_p2 = "training_p2_"+str(number_simulation)
reward_win = 1
punish_loss = -1

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
            board_state = evalboard(state, 
                                    boards_played[current_player],
                                    p1=p1,
                                    p2=p2,
                                   )
            # Transformed gameboard key
            current_game_boards[current_player] += [board_state[1]]

            # Add entry to the boards_played, if new
            if len(board_state) > 3:
                boards_played[current_player].update(
                    {board_state[1]: board_state[0]})

            # Decide the move
            srow, scol, trow, tcol = decideplay(board_state[0], 
                                                board_state[2],
                                                )
            current_game_move[current_player] += [(srow, scol)]

            # Make the move, and update state
            state = updateboard(state, (trow, tcol), current_player)

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
        for key, move in zip(current_game_boards[winning_player], current_game_move[winning_player]):
            delta = np.zeros((3, 3))
            delta[move[0]][move[1]] += reward_win
            boards_played[winning_player][key] += delta

        for key, move in zip(current_game_boards[losing_player], current_game_move[losing_player]):
            delta = np.zeros((3, 3))
            delta[move[0]][move[1]] += punish_loss
            boards_played[losing_player][key] += delta

# Save out training
for player in (p1, p2):
    with open(fnames[player], "wb") as f:
        pickle.dump((boards_played[player]), f)