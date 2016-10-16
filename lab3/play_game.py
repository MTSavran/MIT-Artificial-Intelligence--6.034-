#!/usr/bin/env python2

# MIT 6.034 Lab 3: Games

# To play against your Connect Four implementation, run this file
# from your lab3 directory.
# Wrapper written by Hunter Gatewood.

from game_api import *
from boards import *
from lab3 import *

TESTING = False
QUIT = ['q', 'Q', 'quit', 'Quit', 'QUIT']
YES = ['y', 'yes', 'Y', 'Yes', 'YES']
NO = ['n', 'no', 'N', 'No', 'NO']


def new_state(snap=None):
    board = ConnectFourBoard() if snap is None else snap
    state_starting_connectfour = AbstractGameState(
        snapshot=board,
        is_game_over_fn=is_game_over_connectfour,
        generate_next_states_fn=next_boards_connectfour,
        endgame_score_fn=endgame_score_connectfour_faster)
    return state_starting_connectfour


def start_game():
    print "\n\n\n"
    state = new_state()
    if TESTING:
        player_name = 'Hunter'
        player_goes_first = True
        depth_limit = 4
    else:
        player_name, player_goes_first, depth_limit = say_hi()
    players_move = player_goes_first
    cont = True
    while cont:
        # Print the board state, then have someone take a turn
        if players_move:
            print_board_state(state)
            state, cont = player_turn(state)
        else:
            state = ai_turn(state, depth_limit)

        # If the player wants to exit
        if cont is False:
            print_end(cont, player_name)
        # If the game is over, print who wins and decide if a new game should be started
        elif state.is_game_over():
            cont = print_endgame(state, players_move)
            state = new_state()
            print_end(cont, player_name)

        # Switch whose turn it is
        players_move = not players_move


def get_player_move(state):
    print "Into which column [0-6] would you like to place a piece?"
    player_response = None
    while player_response is None:
        inp = raw_input(">>> ")

        # Allow the player to quit gracefully
        if inp in QUIT:
            player_response = None
            break
        try:
            player_response = int(inp)
        except:
            pass
        if player_response not in xrange(7):
            player_response = None
            print "Oops, please pick a column between 0 and 6, inclusive"
        if player_response is not None and state.snapshot.is_column_full(player_response):
            player_response = None
            print "Oops, that column's full"
    return player_response


def player_turn(state):
    player_move = get_player_move(state)
    cont = player_move is not None
    if cont:
        snapshot = state.get_snapshot().add_piece(player_move)
        state = new_state(snapshot)
    return state, cont


def print_ai_move(state):
    description = state.describe_previous_move()
    print '\nAI move:', description


def ai_turn(state, depth_limit):
    alphabeta_ret = minimax_search_alphabeta(
        state, -INF, INF, heuristic_connectfour, depth_limit)
    new_state = alphabeta_ret[0][1]
    print_ai_move(new_state)
    return new_state


def was_a_draw(state):
    for chain in state.snapshot.get_all_chains():
        if len(chain) >= 4:
            return False
    return True


def print_endgame(state, players_move):
    # If the player won
    print_board_state(state, game_over=True)
    if was_a_draw(state):
        print "Nice, it was a draw!"
    elif players_move:
        print "Congrats! You win!"
    else:
        print "Darn! You lost. Better luck next time!"

    print "Want to play again?"
    play_again = raw_input(">>> ") in YES
    return play_again


def print_end(cont, player_name):
    if cont:
        print "\n\n\nOkay, let's start a new game."
    else:
        print "\n\nThanks for playing, " + player_name + "!"


def print_board_state(state, game_over=False):
    if game_over:
        print "\n"*30 + "Final board state:"
    else:
        print "\n\nCurrent board state:"
    print state.snapshot
    print "0 1 2 3 4 5 6"
    print ""


def say_hi():
    print "ARE YOU SMARTER THAN YOUR 034 BOT?"
    print "Wrapper implemented by Hunter Gatewood"
    print "\nWelcome!"
    print "First, let's get your name"
    name = raw_input(">>> ")
    print "\nOkay, do you want to go first?"
    first = None
    while first is None:
        inp = raw_input(">>> ")
        if inp in YES:
            first = True
        elif inp in NO:
            first = False
        if first is None:
            print "Oops, please type either 'yes' or 'no'."
    print "\nAnd, finally, choose the depth limit for the bot's search"
    print "(Picking values larger than 4 or 5 could result in long wait times,"
    print " while picking 1 would make for a mostly trivial game)"
    depth_limit = None
    while depth_limit is None:
        inp = raw_input(">>> ")
        try:
            depth_limit = int(inp)
        except:
            pass
        if depth_limit is None or depth_limit < 1:
            depth_limit = None
            print "Oops, please give an integer value >= 1."
    print "\nCool. Type 'q' at any point to quit (or <Ctrl-c>)"
    print "Let's play Connect 4!"
    print "\n\n"
    return name, first, depth_limit


if __name__ == '__main__':
    start_game()
