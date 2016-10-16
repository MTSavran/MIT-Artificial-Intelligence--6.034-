# MIT 6.034 Lab 3: Games

from tester import make_test, get_tests
from game_api import *
from boards import *
from lab3 import (next_boards_connectfour, is_game_over_connectfour,
                  endgame_score_connectfour, endgame_score_connectfour_faster,
                  minimax_search)
INF = float('inf')



## is_game_over_connectfour

#has chain len 4 -> True
def is_game_over_connectfour_0_getargs() :  #TEST 1
    return [PLAYER_ONE1_WON]
def is_game_over_connectfour_0_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_0_getargs,
          testanswer = is_game_over_connectfour_0_testanswer,
          expected_val = "True",
          name = 'is_game_over_connectfour')

#all chains len < 4, board full -> True
def is_game_over_connectfour_1_getargs() :  #TEST 2
    return [BOARD_FULL_TIED]
def is_game_over_connectfour_1_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_1_getargs,
          testanswer = is_game_over_connectfour_1_testanswer,
          expected_val = "True",
          name = 'is_game_over_connectfour')

#all chains len < 4, board not full -> False
def is_game_over_connectfour_2_getargs() :  #TEST 3
    return [NEARLY_OVER]
def is_game_over_connectfour_2_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_2_getargs,
          testanswer = is_game_over_connectfour_2_testanswer,
          expected_val = "False",
          name = 'is_game_over_connectfour')

def is_game_over_connectfour_3_getargs() :  #TEST 4
    return [BOARD_PARTIAL]
def is_game_over_connectfour_3_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_3_getargs,
          testanswer = is_game_over_connectfour_3_testanswer,
          expected_val = "False",
          name = 'is_game_over_connectfour')

#empty board -> False
def is_game_over_connectfour_4_getargs() :  #TEST 5
    return [BOARD_EMPTY]
def is_game_over_connectfour_4_testanswer(val, original_val = None) :
    return val == False
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_4_getargs,
          testanswer = is_game_over_connectfour_4_testanswer,
          expected_val = "False",
          name = 'is_game_over_connectfour')

#chain of length 5 -> True
def is_game_over_connectfour_5_getargs() :  #TEST 6
    return [BOARD_FIVE_IN_A_ROW]
def is_game_over_connectfour_5_testanswer(val, original_val = None) :
    return val == True
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = is_game_over_connectfour_5_getargs,
          testanswer = is_game_over_connectfour_5_testanswer,
          expected_val = "True",
          name = 'is_game_over_connectfour')

## next_boards_connectfour

def compare_list_of_boards_by_array(list1, list2):
    # Note: This only checks whether board_arrays match, not other attributes.
    return (isinstance(list1, list) and isinstance(list2, list) and len(list1) == len(list2)
            and all([is_class_instance(board1, 'ConnectFourBoard')
                     and board1.same_board_array(board2)
                     for (board1, board2) in zip(list1, list2)]))

#empty board -> range(7)
next_boards_BOARD_EMPTY = [BOARD_EMPTY_move0, BOARD_EMPTY_move1,
                           BOARD_EMPTY_move2, BOARD_EMPTY_move3,
                           BOARD_EMPTY_move4, BOARD_EMPTY_move5,
                           BOARD_EMPTY_move6]
def next_boards_connectfour_0_getargs() :  #TEST 7
    return [BOARD_EMPTY]
def next_boards_connectfour_0_testanswer(val, original_val = None) :
    return compare_list_of_boards_by_array(val, next_boards_BOARD_EMPTY)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_0_getargs,
          testanswer = next_boards_connectfour_0_testanswer,
          expected_val = ("(list of 7 ConnectFourBoard objects resulting from "
                          +"adding a piece to boards.BOARD_EMPTY)"),
          name = 'next_boards_connectfour')

#board with some pieces, no columns full -> range(7)
next_boards_BOARD_PARTIAL = [BOARD_PARTIAL_move0, BOARD_PARTIAL_move1,
                             BOARD_PARTIAL_move2, BOARD_PARTIAL_move3,
                             BOARD_PARTIAL_move4, BOARD_PARTIAL_move5,
                             BOARD_PARTIAL_move6]
def next_boards_connectfour_1_getargs() :  #TEST 8
    return [BOARD_PARTIAL]
def next_boards_connectfour_1_testanswer(val, original_val = None) :
    return compare_list_of_boards_by_array(val, next_boards_BOARD_PARTIAL)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_1_getargs,
          testanswer = next_boards_connectfour_1_testanswer,
          expected_val = ("(list of 7 ConnectFourBoard objects resulting from "
                          +"adding a piece to boards.BOARD_PARTIAL)"),
          name = 'next_boards_connectfour')

#board with columns 1, 2, 3, 4, 6 full -> [0, 5]
next_boards_NEARLY_OVER = [NEARLY_OVER_move0, NEARLY_OVER_move5]
def next_boards_connectfour_2_getargs() :  #TEST 9
    return [NEARLY_OVER]
def next_boards_connectfour_2_testanswer(val, original_val = None) :
    return compare_list_of_boards_by_array(val, next_boards_NEARLY_OVER)
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_2_getargs,
          testanswer = next_boards_connectfour_2_testanswer,
          expected_val = ("(list of 2 ConnectFourBoard objects resulting from "
                          +"adding a piece to boards.NEARLY_OVER)"),
          name = 'next_boards_connectfour')

#board with all columns full -> []
def next_boards_connectfour_3_getargs() :  #TEST 10
    return [BOARD_FULL_TIED]
def next_boards_connectfour_3_testanswer(val, original_val = None) :
    return val == []
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_3_getargs,
          testanswer = next_boards_connectfour_3_testanswer,
          expected_val = "[]",
          name = 'next_boards_connectfour')

#board with some space, with chain len 4 -> []
def next_boards_connectfour_4_getargs() :  #TEST 11
    return [PLAYER_TWO2_WON]
def next_boards_connectfour_4_testanswer(val, original_val = None) :
    return val == []
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_4_getargs,
          testanswer = next_boards_connectfour_4_testanswer,
          expected_val = "[]",
          name = 'next_boards_connectfour')

#board with one space open in col 3 -> [3]
#This tests that other ConnectFourBoard attributes are correct, in addition to board_array
def next_boards_connectfour_5_getargs() :  #TEST 12
    return [BOARD_FULL_TIED_minus3]
def next_boards_connectfour_5_testanswer(val, original_val = None) :
    return val == [BOARD_FULL_TIED_minus3.add_piece(3)]
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = next_boards_connectfour_5_getargs,
          testanswer = next_boards_connectfour_5_testanswer,
          expected_val = "(list containing 1 full ConnectFourBoard with correct attributes)",
          name = 'next_boards_connectfour')


## endgame_score_connectfour

#MAX wins -> return 1000
def endgame_score_connectfour_MAX_getargs() :  #TEST 13
    return [PLAYER_2_ALICE_DOMINATED, False]
def endgame_score_connectfour_MAX_testanswer(val, original_val = None) :
    return val == 1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = endgame_score_connectfour_MAX_getargs,
          testanswer = endgame_score_connectfour_MAX_testanswer,
          expected_val = "1000",
          name = 'endgame_score_connectfour')

#MIN wins -> return -1000
def endgame_score_connectfour_MIN_getargs() :  #TEST 14
    return [PLAYER_ONE1_WON, True]
def endgame_score_connectfour_MIN_testanswer(val, original_val = None) :
    return val == -1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = endgame_score_connectfour_MIN_getargs,
          testanswer = endgame_score_connectfour_MIN_testanswer,
          expected_val = "-1000",
          name = 'endgame_score_connectfour')

#tie -> return 0
def endgame_score_connectfour_MIN_getargs() :  #TEST 15
    return [BOARD_FULL_TIED, True]
def endgame_score_connectfour_MIN_testanswer(val, original_val = None) :
    return val == 0
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = endgame_score_connectfour_MIN_getargs,
          testanswer = endgame_score_connectfour_MIN_testanswer,
          expected_val = "0",
          name = 'endgame_score_connectfour')


## endgame_score_connectfour_faster

#compare wins with fewer pieces on board (higher abs score) vs more pieces (lower abs score)
def endgame_score_connectfour_faster_MIN_getargs() :  #TEST 16
    return [[BOARD_ONEFISH_WON_FAST, True],  # stronger win for MIN (fewer total pieces on board)
            [BOARD_REDFISH_WON_LESS_FAST, True]]  # weaker win for MIN (more total pieces on board)
def endgame_score_connectfour_faster_MIN_testanswer(val, original_val = None) :
    val_stronger, val_weaker = val
    return val_stronger <= -1000 and val_weaker <= -1000 and val_stronger < val_weaker
make_test(type = 'MULTIFUNCTION',
          getargs = endgame_score_connectfour_faster_MIN_getargs,
          testanswer = endgame_score_connectfour_faster_MIN_testanswer,
          expected_val = ("(list of two endgame scores, the first less "
                          +"than the second, and each <= -1000)"),
          name = 'endgame_score_connectfour_faster')

def endgame_score_connectfour_faster_MAX_getargs() :  #TEST 17
    return [[PLAYER_TWO1_WON, False],  # stronger win for MAX (fewer total pieces on board)
            [PLAYER_2_ALICE_DOMINATED, False]]  # weaker win for MAX (more total pieces on board)
def endgame_score_connectfour_faster_MAX_testanswer(val, original_val = None) :
    val_stronger, val_weaker = val
    return val_stronger >= 1000 and val_weaker >= 1000 and val_stronger > val_weaker
make_test(type = 'MULTIFUNCTION',
          getargs = endgame_score_connectfour_faster_MAX_getargs,
          testanswer = endgame_score_connectfour_faster_MAX_testanswer,
          expected_val = ("(list of two endgame scores, the first greater "
                          +"than the second, and each >= 1000)"),
          name = 'endgame_score_connectfour_faster')


## heuristic_connectfour

# >0 if MAX's turn and MAX winning, val < 1000
def heuristic_connectfour_0_getargs() :  #TEST 18
    return [BOARD_1_WINNING_BARELY, True]
def heuristic_connectfour_0_testanswer(val, original_val = None) :
    return isinstance(val, (int, float)) and val > 0 and val < 1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = heuristic_connectfour_0_getargs,
          testanswer = heuristic_connectfour_0_testanswer,
          expected_val = "(heuristic score > 0 and < 1000)",
          name = 'heuristic_connectfour')

# >0 if MIN's turn and MAX winning, val < 1000
def heuristic_connectfour_1_getargs() :  #TEST 19
    return [BOARD_2_WINNING_DEFINITELY, False]
def heuristic_connectfour_1_testanswer(val, original_val = None) :
    return isinstance(val, (int, float)) and val > 0 and val < 1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = heuristic_connectfour_1_getargs,
          testanswer = heuristic_connectfour_1_testanswer,
          expected_val = "(heuristic score > 0 and < 1000)",
          name = 'heuristic_connectfour')

# <0 if MIN's turn and MIN winning, val > -1000
def heuristic_connectfour_2_getargs() :  #TEST 20
    return [BOARD_1_WINNING_BARELY, False]
def heuristic_connectfour_2_testanswer(val, original_val = None) :
    return isinstance(val, (int, float)) and val < 0 and val > -1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = heuristic_connectfour_2_getargs,
          testanswer = heuristic_connectfour_2_testanswer,
          expected_val = "(heuristic score < 0 and > -1000)",
          name = 'heuristic_connectfour')

# <0 if MAX's turn and MIN winning, val > -1000
def heuristic_connectfour_3_getargs() :  #TEST 21
    return [BOARD_2_WINNING_LESS_PIECES, True]
def heuristic_connectfour_3_testanswer(val, original_val = None) :
    return isinstance(val, (int, float)) and val < 0 and val > -1000
make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = heuristic_connectfour_3_getargs,
          testanswer = heuristic_connectfour_3_testanswer,
          expected_val = "(heuristic score < 0 and > -1000)",
          name = 'heuristic_connectfour')

# larger score if MAX is winning by more
def heuristic_connectfour_4_getargs() :  #TEST 22
    return [[BOARD_2_WINNING_DEFINITELY, True],  # MIN winning by a lot
            [BOARD_1_WINNING_BARELY, False],     # MIN winning, barely
            [BOARD_1_WINNING_BARELY, True],      # MAX winning, barely
            [BOARD_2_WINNING_DEFINITELY, False]] # MAX winning by a lot
def heuristic_connectfour_4_testanswer(val, original_val = None) :
    return (all(map(lambda v: v < 0, val[:2]))
            and all(map(lambda v: v > 0, val[2:]))
            and all(map(lambda v: abs(v) < 1000, val))
            and all(map(lambda i: val[i] < val[i+1], range(3))))
make_test(type = 'MULTIFUNCTION',
          getargs = heuristic_connectfour_4_getargs,
          testanswer = heuristic_connectfour_4_testanswer,
          expected_val = ("list of four heuristic scores in increasing order, "
                          + "representing a list of four boards wherein each "
                          + "board is clearly better than the previous for MAX"),
          name = 'heuristic_connectfour')


## dfs_maximizing

def dfs_0_getargs() :  #TEST 23
    return [GAME1]
def dfs_0_testanswer(val, original_val = None) :
    return  (is_dfs_return_type(val) and move_sequence(GAME1, [2,3]) == val[0]
             and (val[1], val[2]) == (16, 16))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = dfs_0_getargs,
          testanswer = dfs_0_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) corresponding to cooperatively playing as the maximizer.",
          name = 'dfs_maximizing')


# MINIMAX ENDGAME SEARCH
def minimax_endgame_0_getargs() :  #TEST 24
    return [GAME1, True]

def minimax_endgame_0_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val) and move_sequence(GAME1, [1,0]) == val[0]
            and (val[1], val[2]) == (4, 16))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_endgame_0_getargs,
          testanswer = minimax_endgame_0_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) corresponding to minimax score when the first player is the maximizer.",
          name = 'minimax_endgame_search')

def minimax_endgame_1_getargs() :  #TEST 25
    return [GAME1, False]

def minimax_endgame_1_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val) and move_sequence(GAME1, [0,1]) == val[0]
            and (val[1], val[2]) == (11, 16))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_endgame_1_getargs,
          testanswer = minimax_endgame_1_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) corresponding to minimax score when the first player is the minimizer.",
          name = 'minimax_endgame_search')

def minimax_endgame_2_getargs() :  #TEST 26
    GAME = AbstractGameState(NEARLY_OVER, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return [GAME, True]

def minimax_endgame_2_testanswer(val, original_val = None) :
    GAME = AbstractGameState(NEARLY_OVER, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return (is_dfs_return_type(val) and move_sequence(GAME, [1,0,0]) == val[0]
            and val[1] >= 1000 and val[2] == 6)

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_endgame_2_getargs,
          testanswer = minimax_endgame_2_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) " \
              + "corresponding to minimax score when the first player is the " \
              + "maximizer.  (Hint: make sure you're using the argument "\
              + "'maximize' with get_endgame_score.",
          name = 'minimax_endgame_search')


# LIMITED DEPTH SEARCH

# This test with depth_limit=INF is just to check use of the argument 'maximize'
def minimax_1_getargs() :  #TEST 27
    GAME = AbstractGameState(NEARLY_OVER, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return [GAME, always_zero, INF, True]

def minimax_1_testanswer(val, original_val = None) :
    GAME = AbstractGameState(NEARLY_OVER, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return (is_dfs_return_type(val) and move_sequence(GAME, [1,0,0]) == val[0]
            and val[1] >= 1000 and val[2] == 6)

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_1_getargs,
          testanswer = minimax_1_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) " \
              + "corresponding to minimax score when the first player is the " \
              + "maximizer.  (Hint: make sure you're using the argument "\
              + "'maximize' with get_endgame_score.",
          name = 'minimax_search')


def minimax_2_getargs() :  #TEST 28
    return [GAME_STATIC_ALL_LEVELS, always_zero, 2, True]

def minimax_2_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val) and move_sequence(GAME_STATIC_ALL_LEVELS, [2]) == val[0]
            and (val[1],val[2]) == (3,6))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_2_getargs,
          testanswer = minimax_2_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) corresponding to minimax score when the first player is the maximizer.",
          name = 'minimax_search')


def minimax_3_getargs() :  #TEST 29
    GAME = AbstractGameState(BOARD_UHOH, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    valuate = lambda board, player : len(sum(board.get_all_chains(player),[]))
    return [GAME, lambda board,maximize: [-1,1][maximize] * (valuate(board,True) - valuate(board, False)), 2, True]

def minimax_3_testanswer(val, original_val = None) :
    GAME = AbstractGameState(BOARD_UHOH, is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return (is_dfs_return_type(val) and move_sequence(GAME, [4,5]) == val[0]
            and (val[1],val[2]) == (-3,49))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_3_getargs,
          testanswer = minimax_3_testanswer,
          expected_val = ("List of (best_path, leaf_score, evaluation_count) "
                          +"corresponding to minimax score when the first player "
                          +"is the maximizer. (This is a Connect Four game, "
                          +"requiring methods you've written.)"),
          name = 'minimax_search')


def minimax_4_getargs() :  #TEST 30
    GAME = AbstractGameState(BOARD_EMPTY.add_piece(3).add_piece(3), is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    valuate = lambda board, player : len(sum(board.get_all_chains(player),[]))
    density = lambda board, player : sum([abs(index-3)
                                                 for row in board.board_array
                                                 for (piece, index) in zip(row, range(board.num_cols))
                                                 if piece and (piece == 1) == (board.count_pieces() + player) % 2])

    return [GAME, lambda board,maximize: [-1,1][maximize] * (density(board, False) - density(board, True) + 2*valuate(board,True) - 3*valuate(board, False)), 4, True]

def minimax_4_testanswer(val, original_val = None) :
    GAME = AbstractGameState(BOARD_EMPTY.add_piece(3).add_piece(3), is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    return (is_dfs_return_type(val) and move_sequence(GAME, [3,1,3,2]) == val[0]
            and (val[1],val[2]) == (-3,2401))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = minimax_4_getargs,
          testanswer = minimax_4_testanswer,
          expected_val = ("List of (best_path, leaf_score, evaluation_count) "
                          +"corresponding to minimax score when the first player "
                          +"is the maximizer. (This is a Connect Four game, "
                          +"requiring methods you've written.)"),
          name = 'minimax_search')


## minimax_search_alphabeta

#  A two-move game.
def alphabeta_0_getargs() :  #TEST 31
    return [GAME1, -INF, INF, lambda x,y:0, INF, True]

def alphabeta_0_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val) and move_sequence(GAME1, [1,0]) == val[0]
            and (val[1],val[2]) == (4,13))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_0_getargs,
          testanswer = alphabeta_0_testanswer,
          expected_val = "List of (best_path, leaf_score, evaluation_count) corresponding to minimax+alphabeta when the maximizer moves first.",
          name = 'minimax_search_alphabeta')


def alphabeta_1_getargs() :  #TEST 32
    return [GAME1, -INF, INF, lambda x,y:0, INF, False]

def alphabeta_1_testanswer(val, original_val = None) :
    return is_dfs_return_type(val) and (val[1],val[2]) == (11,11) and move_sequence(GAME1, [0,1]) == val[0]

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_1_getargs,
          testanswer = alphabeta_1_testanswer,
          expected_val = ("List of (best_path, leaf_score, evaluation_count) "
                          +"corresponding to minimax+alphabeta when the minimizer "
                          +"moves first."),
          name = 'minimax_search_alphabeta')




def alphabeta_2_getargs() :  #TEST 33
    return [GAME_EQUALITY_PRUNING, -INF, INF, lambda x,y:0, INF, True]

def alphabeta_2_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(GAME_EQUALITY_PRUNING, [0,0,0,0]) == val[0]
            and (val[1],val[2]) == (3,6))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_2_getargs,
          testanswer = alphabeta_2_testanswer,
          expected_val = ("List of (best_path, leaf_score, evaluation_count) "
                          +"corresponding to minimax+alphabeta when the maximizer "
                          +"moves first. (What should happen when alpha = beta?)"),
          name = 'minimax_search_alphabeta')


# A test for when the correct move is not just the first available move
def alphabeta_3_getargs() :  #TEST 34
    return [GAME_EQUALITY_PRUNING, -INF, INF, lambda x,y:0, INF, False]

def alphabeta_3_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(GAME_EQUALITY_PRUNING, [1,1,0,1]) == val[0]
            and (val[1],val[2]) == (14,11))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_3_getargs,
          testanswer = alphabeta_3_testanswer,
          expected_val = ("List of (best_path, leaf_score, evaluation_count) "
                          +"corresponding to minimax+alphabeta when the minimizer "
                          +"moves first."),
          name = 'minimax_search_alphabeta')


PRUNING_TREE = ToyTree()
PRUNING_TREE.sub('A',10).sub()
PRUNING_TREE.down().right().sub('B',20).sub()
PRUNING_TREE.down().right().down().right().sub('C',1).sub()
PRUNING_TREE.down().right().down().right().down().right().sub('D',4).sub('X',2)

PRUNING_GAME = AbstractGameState(PRUNING_TREE,
                          toytree_is_game_over,
                          toytree_generate_next_states,
                          toytree_endgame_score_fn)

def alphabeta_4_getargs() :  #TEST 35
    return [PRUNING_GAME, -INF, INF, toytree_heuristic_fn, INF, True]

def alphabeta_4_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(PRUNING_GAME, [0]) == val[0]
            and (val[1],val[2]) == (10,4))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_4_getargs,
          testanswer = alphabeta_4_testanswer,
          expected_val = ("((list of two AbstractGameState instances), 10, 4) "
                          +"(Hint: If you get 5 evaluations instead of 4, check "
                          +"your pruning condition, and check how your alpha "
                          +"and beta values get passed up and down the tree.)"),
          name = 'minimax_search_alphabeta')


PRUNING_TREE_NEG = ToyTree()
PRUNING_TREE_NEG.sub('A',-10).sub()
PRUNING_TREE_NEG.down().right().sub('B',-20).sub()
PRUNING_TREE_NEG.down().right().down().right().sub('C',-1).sub()
PRUNING_TREE_NEG.down().right().down().right().down().right().sub('D',-4).sub('X',-2)

PRUNING_GAME_NEG = AbstractGameState(PRUNING_TREE_NEG,
                          toytree_is_game_over,
                          toytree_generate_next_states,
                          toytree_endgame_score_fn)

def alphabeta_5_getargs() :  #TEST 36
    return [PRUNING_GAME_NEG, -INF, INF, toytree_heuristic_fn, INF, False]

def alphabeta_5_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(PRUNING_GAME_NEG, [0]) == val[0]
            and (val[1],val[2]) == (-10,4))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_5_getargs,
          testanswer = alphabeta_5_testanswer,
          expected_val = ("((list of two AbstractGameState instances), -10, 4) "
                          +"(Hint: If you get 5 evaluations instead of 4, check "
                          +"your pruning condition, and check how your alpha "
                          +"and beta values get passed up and down the tree.)"),
          name = 'minimax_search_alphabeta')


NEGATE_TREE = ToyTree()
NEGATE_TREE.sub('P',4).sub('Q',5)

NEGATE_GAME_endgame_score_fn = lambda tree, is_max: [-1,1][is_max] * tree.score
NEGATE_GAME = AbstractGameState(NEGATE_TREE,
                          toytree_is_game_over,
                          toytree_generate_next_states,
                          NEGATE_GAME_endgame_score_fn)

def alphabeta_6_getargs() :  #TEST 37
    return [NEGATE_GAME, -INF, INF, toytree_heuristic_fn, INF, True]

def alphabeta_6_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(NEGATE_GAME, [0]) == val[0]
            and (val[1],val[2]) == (-4,2))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_6_getargs,
          testanswer = alphabeta_6_testanswer,
          expected_val = ("((list of two AbstractGameState instances), -4, 2) "
                          +"(Hint: If you get a score of 5 instead of -4, check "
                          +"that you're calling state.get_endgame_score with "
                          +"the 'maximize' argument.)"),
          name = 'minimax_search_alphabeta')


# This checks that the heuristic function is actually used, rather than being
# reset to always_zero.
NONZERO_TREE = ToyTree()
NONZERO_TREE.sub().sub()
NONZERO_TREE.down().sub('C',1).right().sub('E',2)

NONZERO_GAME = AbstractGameState(NONZERO_TREE,
                          toytree_is_game_over,
                          toytree_generate_next_states,
                          toytree_endgame_score_fn)

def alphabeta_7_getargs() :  #TEST 38
    return [NONZERO_GAME, -INF, INF,
            lambda x,y: x.children[0].score if x.children else x.score, 1, True]

def alphabeta_7_testanswer(val, original_val = None) :
    return (is_dfs_return_type(val)
            and move_sequence(NONZERO_GAME, [1]) == val[0]
            and (val[1],val[2]) == (2,2))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = alphabeta_7_getargs,
          testanswer = alphabeta_7_testanswer,
          expected_val = ("((list of two AbstractGameState instances), 2, 2) "
                          +"(Hint: check how you use heuristic_fn and depth_limit)"),
          name = 'minimax_search_alphabeta')


## progressive_deepening

def progressive_0_getargs() :  #TEST 39
    return [GAME_STATIC_ALL_LEVELS, toytree_heuristic_fn, 3, True]

def progressive_0_testanswer(val, original_val = None) :
    if not is_class_instance(val, 'AnytimeValue'):
        return False
    h = val.history
    return (all(map(is_dfs_return_type, h))
            and [11,10,10] == map(lambda x: x[1], h) and [4,5,6] == map(lambda x: x[2], h))

make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = progressive_0_getargs,
          testanswer = progressive_0_testanswer,
          expected_val = ("An AnytimeValue object storing the results of " +
                          "progressive deepening. (You can use .pretty_print " +
                          "to see the properties of your AnytimeValue object.)"),
          name = 'progressive_deepening')



def progressive_1_getargs() :  #TEST 40

    GAME = AbstractGameState(BOARD_EMPTY.add_piece(3).add_piece(3), is_game_over_connectfour, next_boards_connectfour, endgame_score_connectfour)
    valuate = lambda board, player : len(sum(board.get_all_chains(player),[]))
    density = lambda board, player : sum([abs(index-3)
                                                 for row in board.board_array
                                                 for (piece, index) in zip(row, range(board.num_cols))
                                                 if piece and (piece == 1) == (board.count_pieces() + player) % 2])

    return [GAME, lambda board,maximize: [-1,1][maximize] * (density(board, False) - density(board, True) + 2*valuate(board,True) - 3*valuate(board, False)), 5, True]

def progressive_1_testanswer(val, original_val = None) :
    if not is_class_instance(val, 'AnytimeValue'):
        return False
    h = val.history
    return (all(map(is_dfs_return_type, h))
            and [4, -2, 5, -3, 20] == map(lambda x: x[1], h) and [7,34,176, 695, 2259] == map(lambda x: x[2], h))


make_test(type = 'FUNCTION_ENCODED_ARGS',
          getargs = progressive_1_getargs,
          testanswer = progressive_1_testanswer,
          expected_val = ("An AnytimeValue object storing the results of " +
                          "progressive deepening. (You can use .pretty_print " +
                          "to see the properties of your AnytimeValue object. " +
                          "This is a Connect Four game, requiring methods you've written.)"),
          name = 'progressive_deepening')


#### PART 3: Multiple Choice ##################################

ANSWER_1_getargs = "ANSWER_1"
def ANSWER_1_testanswer(val, original_val = None):  #TEST 41
    """Minimax without the alpha-beta optimization never prunes any nodes.
    All nodes must be examined."""
    if val == '':
        raise NotImplementedError
    return str(val) == '4'
make_test(type = 'VALUE',
          getargs = ANSWER_1_getargs,
          testanswer = ANSWER_1_testanswer,
          expected_val = "correct value of ANSWER_1 ('1', '2', '3', '4', or '5')",
          name = ANSWER_1_getargs)

ANSWER_2_getargs = "ANSWER_2"
def ANSWER_2_testanswer(val, original_val = None):  #TEST 42
    """With monotonically decreasing leaves, running minimax with
    alpha-beta will eventually prune the last two leaves of the 
    tree (the two leaves belonging to the right-most branch).
    Note that in this situation, only two leaves may be pruned,
    whereas the best case game tree of this shape allows 
    three leaves to be pruned."""
    if val == '':
        raise NotImplementedError
    return str(val) == '1'
make_test(type = 'VALUE',
          getargs = ANSWER_2_getargs,
          testanswer = ANSWER_2_testanswer,
          expected_val = "correct value of ANSWER_2 ('1', '2', '3', '4', or '5')",
          name = ANSWER_2_getargs)

ANSWER_3_getargs = "ANSWER_3"
def ANSWER_3_testanswer(val, original_val = None):  #TEST 43
    """
    (1) If no leaves were pruneable in the tree, swapping two children could
    definitely help. For example, what would happen if it's MAX's turn and the
    tree initially had monotonically increasing leaves, but then you swapped the
    two top-level children?
    (2) Similarly, that idea can be applied at any level of the tree. Especially
    in a tree with distinct, monotonically increasing/decreasing leaves,
    swapping any two children is likely to change whether any nodes will get
    pruned in that subtree.
    (3) Because depth_limit=INF, the heuristic_fn is never even used.
    Hence, changing the heuristic_fn will have no effect.

    Thus, the final answer is (4).
    """
    if val == '':
        raise NotImplementedError
    return str(val) == '4'
make_test(type = 'VALUE',
          getargs = ANSWER_3_getargs,
          testanswer = ANSWER_3_testanswer,
          expected_val = "correct value of ANSWER_3 ('1', '2', '3', '4', or '5')",
          name = ANSWER_3_getargs)

ANSWER_4_getargs = "ANSWER_4"
def ANSWER_4_testanswer(val, original_val = None):  #TEST 44
    """
    (1) This idea won't improve anything, and in fact will actually just make
    your algorithm run n times slower. You're running the same *deterministic*
    algorithm n times on the *same tree*, so no matter how Eve rearranged the
    nodes, you're running the same exact steps n times.

    (2) If depth_limit is finite and less than the depth of the tree (a common
    situation), then the always_zero function is a terrible heuristic, because
    it prevents you from getting any information about non-leaf nodes.
    Your algorithm will likely suffer as a result.

    (3) Similar to above, but even worse. This time, you are possibly returning
    larger and smaller numbers, which would arbitrarily label nodes as being
    better options for MAX (large numbers) or MIN (small numbers).

    (4) This is the least disastrous of the 'wrong' options. At best, it won't
    do much. If your heuristic is decent, a small depth_limit could result in
    fast, well-informed decisions about which branch to take. However, if you're
    only looking one or two levels down in the tree, there won't be much
    opportunity for pruning, and you may get a misleading result if your
    heuristic isn't fantastic.

    (5) This is the best answer. Adding this stochastic step thwarts Eve's
    efforts, because her reordering is no match against a random branch picker.
    Sometimes your algorithm will do great; other times, it will do poorly.
    But on average, it will fare moderately well against Eve's meddling.
    """
    if val == '':
        raise NotImplementedError
    return str(val) == '5'
make_test(type = 'VALUE',
          getargs = ANSWER_4_getargs,
          testanswer = ANSWER_4_testanswer,
          expected_val = "correct value of ANSWER_4 ('1', '2', '3', '4', or '5')",
          name = ANSWER_4_getargs)
