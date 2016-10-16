# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    l = board.get_all_chains()
    for chain in l:
        if len(chain) >= 4:
            return True
    if board.count_pieces() == 42:
        return True
    return False

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    answer = []
    if is_game_over_connectfour(board):
        return []
    for i in range(board.num_cols):
        if board.is_column_full(i): #Column is full, can't add to next states!
            continue
        else: 
            newboard = board.add_piece(i)
            answer.append(newboard)
    return answer

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    
    score1 = 0 
    score2 = 0
    l = board.get_all_chains(True)
    for chain in l:
        uzunluk = len(chain)
        if uzunluk == 4:
            score1 += 1000
        elif uzunluk ==3: 
            score1 += 100
        elif uzunluk ==2:
            score1 += 5

    l2 = board.get_all_chains(False)
    for chain in l2:
        uzunluk = len(chain)
        if uzunluk == 4:
            score2 += 1000
        elif uzunluk ==3: 
            score2 += 100
        elif uzunluk ==2:
            score2 += 5

    skor = score1 - score2 
    if is_current_player_maximizer:
        return skor
    else: 
        return -1*skor


def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    # if is_current_player_maximizer:
    #     return -1000
    # return 1000
    for chain in board.get_all_chains(is_current_player_maximizer):
        if len(chain) >= 4:
            return 1000
    for chain in board.get_all_chains(not is_current_player_maximizer):
        if len(chain) >= 4:
            return -1000
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if is_current_player_maximizer:
        return -35000/board.count_pieces()
    return 35000/board.count_pieces()


# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    global glob
    glob = 0 

    li = []

    def dfsrecurse(state, path = []):
        global glob
        path = path + [state]
        if state.is_game_over():
            # print state
            # print state.get_endgame_score(False)
            glob+=1
            li.append((state.get_endgame_score(),glob,path))
            return path

        # beststatescore = 0 
        # dic = {}
        for child in state.generate_next_states():
            if child not in path:
                dfsrecurse(child,path)
        return path

    dfsrecurse(state)
    li = sorted(li,key = lambda sth: sth[1],reverse=True)
    li = sorted(li,reverse=True)
    # for i in li:
    #     print i
    highest = li[0]
    return (highest[2],highest[0],glob)
# pretty_print_dfs_type(dfs_maximizing(state_NEARLY_OVER))


def minimax_endgame_search(state, maximize=True):
    results = []
    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize),1)
    moves = state.generate_next_states()
    for child in moves:
        results.append(minimax_endgame_search(child,not maximize))
    su = 0 
    for i in results:
        su += i[2]
    if maximize:
        results = max(results,key = lambda sth: sth[1])
    if not maximize:
        results = min(results,key = lambda sth: sth[1])
    
    # results = sorted(results, key = lambda sth: sth[1], reverse = True)
    best_path = [state] + results[0] 
    return (best_path, results[1], su)
#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    results = []
    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize),1)
    if depth_limit == 0:
        return ([state], heuristic_fn(state.get_snapshot(),maximize), 1)
    moves = state.generate_next_states()
    for child in moves:
        results.append(minimax_search(child, heuristic_fn, depth_limit - 1, not maximize))
    su = 0 
    for i in results:
        su += i[2]
    if maximize:
        results = max(results,key = lambda sth: sth[1])
    if not maximize:
        results = min(results,key = lambda sth: sth[1])
    
    # results = sorted(results, key = lambda sth: sth[1], reverse = True)
    best_path = [state] + results[0] 
    return (best_path, results[1], su)

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True):
    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize),1)
    if depth_limit == 0:
        return ([state], heuristic_fn(state.get_snapshot(),maximize), 1)
    if maximize:
        bestalpha = alpha
        bestresult = None
        results = []
        moves = state.generate_next_states()
        for child in moves:
            result=minimax_search_alphabeta(child, bestalpha, beta, heuristic_fn, depth_limit - 1, not maximize)
            results.append(result)
            oldalpha = bestalpha
            bestalpha = max(bestalpha,result[1])
            if bestalpha != oldalpha:
                bestresult = result
            if bestalpha >= beta:
                break
        su = 0 
        for i in results:
            su += i[2]
        bestresult = max(results,key = lambda sth: sth[1])
        return ([state] + bestresult[0], bestresult[1], su)
    if not maximize:
        results = []
        bestresult = None
        bestbeta = beta
        moves = state.generate_next_states()
        for child in moves:
            result=minimax_search_alphabeta(child, alpha, bestbeta, heuristic_fn, depth_limit - 1, not maximize)
            results.append(result)
            oldbeta = bestbeta
            bestbeta = min(bestbeta,result[1])
            if bestbeta != oldbeta:
                bestresult = result
            if bestbeta <= alpha:
                break
        su = 0 
        for i in results:
            su += i[2]
        bestresult = min(results,key = lambda sth: sth[1])
        return ([state] + bestresult[0], bestresult[1], su)
 


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()
    d=0   # TA Note: Use this to store values.
    while d < depth_limit:
        anytime_value.set_value(minimax_search_alphabeta(state, -INF, INF, heuristic_fn,
                             d+1, maximize=True))
        d+=1
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = "Mehmet Tugrul Savran"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = "6"
WHAT_I_FOUND_INTERESTING = "Nothing"
WHAT_I_FOUND_BORING = "Nothing"
SUGGESTIONS = "Nothing"







#####MUSVEDDE

# def min_play(state, maximize=False):
#   if state.is_game_over():
#     return state.get_endgame_score()
#   moves = state.generate_next_states()
#   best_score = float('inf')
#   for move in moves:
#     score = max_play(move)
#     if score < best_score:
#       best_move = move
#       best_score = score
#   return best_score

# def max_play(state, maximize = True):
#   if game_state.is_game_over():
#     return state.get_endgame_score()
#   moves = state.get_available_moves()
#   best_score = float('-inf')
#   for move in moves:
#     min_play(move)
#     if score > best_score:
#       best_move = move
#       best_score = score
#   return best_score


# def minimax_endgame_search(state,maximize=True):
#     path = []
#     moves = state.generate_next_states()
#     best_move = moves[0]
#     best_score = float('-inf')
#     for move in moves:
#         score = min_play(move, False)
#         if score > best_score:
#             best_move = move 
#             best_score = score 
#     return best_move
# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:
