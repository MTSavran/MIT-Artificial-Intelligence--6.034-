# MIT 6.034 Lab 3: Games

from copy import deepcopy

def always_zero(state, maximize=True):
    return 0

class AbstractGameState :

    def __init__(self,
                 snapshot,
                 is_game_over_fn,
                 generate_next_states_fn,
                 endgame_score_fn) :

        self.snapshot = snapshot
        self.starting_state = snapshot
        self.is_game_over_fn = is_game_over_fn
        self.generate_next_states_fn = generate_next_states_fn
        self.endgame_score_fn = endgame_score_fn

    def __str__(self) :
        return "\n<AbstractGameState representing:\n" + self.snapshot.__str__() + "\n>"

    def __eq__(self, other):
        return (is_class_instance(other, 'AbstractGameState')
                and self.snapshot.__eq__(other.snapshot))

    def wrap(self, snapshot) :
        return AbstractGameState(snapshot, self.is_game_over_fn,
                                 self.generate_next_states_fn, self.endgame_score_fn)

    def get_snapshot(self):
        return self.snapshot

    def is_game_over(self) :
        return len(self.generate_next_states()) == 0 or self.is_game_over_fn(self.snapshot)

    def generate_next_states(self) :
        return map(self.wrap, self.generate_next_states_fn(self.snapshot))

    def describe_previous_move(self) :
        return self.snapshot.describe_previous_move()

    def get_endgame_score(self, is_current_player_maximizer=True) :
        # only for leaf nodes
        if not self.is_game_over() :
            raise ValueError("Only endgame states have endgame score defined.")
        return self.endgame_score_fn(self.snapshot, is_current_player_maximizer)

    def restart(self) :
        self.snapshot = self.starting_state
        return self

    def copy(self):
        return deepcopy(self)


class ConnectFourBoard :
    num_rows = 6  # board height
    num_cols = 7  # board width

    def __init__(self, board_array=None, players=['Player One','Player Two'],
                 whose_turn=None) :
        """A board array is a list of rows. The pieces are either 0 (no player), 1, or 2."""
        if (not isinstance(players, (list, tuple))) or len(players) != 2:
            raise TypeError("Expected list of two players, got "+str(players))
        if not board_array :
            board_array = [[0 for c in range(ConnectFourBoard.num_cols)] for r in range(ConnectFourBoard.num_rows)]
        self.board_array = [ [x if x is not 0 else None for x in row] for row in board_array]
        self.prev_move_string = 'none'
        self.players = players[:]
        self.whose_turn = whose_turn if whose_turn in players else players[0]
        if self.whose_turn != self.players[0] :
            self.players.reverse()

    def get_current_player_name(self) :
        """Return the current player. By default, 'Player One' or 'Player Two'."""
        return self.whose_turn

    def set_current_player_name(self, player) :
        """Set the current player. By default, 'Player One' or 'Player Two'."""
        assert player in self.players
        self.whose_turn = player
        self.players = [player] + filter(lambda x : x != player, self.players)

    def get_other_player_name(self) :
        """Return the other player (the one whose turn it is NOT). By default,
        'Player One' or 'Player Two'."""
        return self.players[1]

    def get_player_name(self, player_number):
        """Given a player number (1 or 2), returns name of corresponding player
        (ie 'Player One' or 'Player Two')"""
        p, q = self.players
        return p if self.__piece_type__(p) == player_number else q

    def get_piece(self, col, row) :
        return self.board_array[row][col]

    def count_pieces(self, current_player=None) :
        """Return the total number of pieces on the board. If player is
        supplied, returns only the number of those belonging to that player."""
        if current_player not in [True, False, None]:
            raise TypeError("Expected boolean value for current_player, got "
                            + str(current_player))
        piece_type = self.__piece_type__(self.get_current_player_name() if current_player else self.get_other_player_name())
        player_test = (lambda x: x) if current_player is None else (lambda piece: piece == piece_type)
        return len(filter(player_test, sum(self.board_array,[])))

    def get_column_height(self, col_number) :
        """Return the number of pieces in the column; e.g., 0 if the column is empty."""
        height = 0
        for row in reversed(self.board_array) :
            if row[col_number] :
                height += 1
            else :
                break
        return height

    def is_column_full(self, col_number) :
        "Return True if column is full, False otherwise"
        return self.get_column_height(col_number) == ConnectFourBoard.num_rows

    def add_piece(self, col_number, player=None) :
        """Adds a piece belonging to the player to the given column.
        Returns new board without modifying original."""

        if self.is_column_full(col_number) :
            raise IndexError("Can't add piece to full column "+str(col_number)+".")

        player = player or self.whose_turn
        piece_type = self.__piece_type__(player)
        new_board = self.copy()
        height = 1 + new_board.get_column_height(col_number)
        new_board.board_array[-height][col_number] = piece_type
        new_board.prev_move_string = ("Put " + str(player)
                                      + "'s piece in col " + str(col_number))
        # adding a piece causes the current player to swap
        new_board.set_current_player_name(new_board.players[1])
        return new_board

    def describe_previous_move(self) :
        "Returns a string describing the most recent move leading to current state"
        return self.prev_move_string

    def copy(self) :
        return deepcopy(self)

    def __get_line__(self, col, row, dx, dy) :
        """Return the list of pieces you get starting at (col, row) and
        incrementing by dx,dy until you run out of board."""

        indexes = [(col + i*dx, row + i*dy)
                   for i in range((ConnectFourBoard.num_rows +
                                      ConnectFourBoard.num_cols -1))]
        # to determine if you've run out of board, see whether either col, row exceeds the max value
        # or if the (col, row) changes from non-negative/negative or vice-versa.

        pieces_line = []
        for c,r in indexes :
            if (c >= ConnectFourBoard.num_cols
                or r >= ConnectFourBoard.num_rows
                or c < -ConnectFourBoard.num_cols
                or r < -ConnectFourBoard.num_rows) :
                break
            else :
                pieces_line.append(self.get_piece(c, r))
        return pieces_line

    def get_all_chains(self, current_player=None):
        """Get all maximal contiguous chains of pieces. If player is provided,
        returns only chains belonging to that player."""
        if current_player not in [True, False, None]:
            raise TypeError("Expected boolean value for current_player, got "
                            + str(current_player))
        piece_type = self.__piece_type__(self.get_current_player_name() if current_player else self.get_other_player_name())
        player_test = (lambda chain: True) if current_player is None else (lambda chain : chain[0] == piece_type)

        ret = []
        ret += self.get_singleton_chains()
        ret += self.get_horizontal_chains(False)
        ret += self.get_vertical_chains(False)
        ret += self.get_northeast_chains(False)
        ret += self.get_northwest_chains(False)

        ret = filter(player_test, ret)

        # Uncomment these lines to print chains as lists of player names instead of lists of 1's and 2's:
        #whose = self.__whose_piece__()
        #return map(lambda x: map(lambda y: whose.get(y),x) , ret)

        return ret

    def get_singleton_chains(self):
        def has_twin_in_neighbors(col, row):
            "returns True if piece has a neighbor of same type, else False"
            piece_type = self.get_piece(col, row)
            for x in [col-1, col, col+1]:
                for y in [row-1, row, row+1]:
                    if ((x, y) == (col, row) or x < 0 or y < 0
                        or x >= self.num_cols or y >= self.num_rows):
                        continue
                    if self.get_piece(x, y) == piece_type:
                        return True
            return False

        singleton_chains = []
        for row_index in range(self.num_rows):
            for col_index in range(self.num_cols):
                piece_type = self.get_piece(col_index, row_index)
                if piece_type is None or has_twin_in_neighbors(col_index, row_index):
                    continue
                singleton_chains.append([piece_type])
        return singleton_chains

    def get_horizontal_chains(self, includeSingletons=False):
        return self.__get_non_diagonal_chains__(1, 0, includeSingletons) # horizontal rightward

    def get_vertical_chains(self, includeSingletons=False):
        return self.__get_non_diagonal_chains__(0, 1, includeSingletons) #vertical downward

    def __get_non_diagonal_chains__(self, dx, dy, includeSingletons=False):
        "Get all chains in a particular direction, horizontal or vertical."
        ret = []
        if dx > 0 :
            # Iterate over all rows
            for r in range(ConnectFourBoard.num_rows):
                ret += self.__break_apart_line__(self.__get_line__(0, r, dx, dy))
        if dx <= 0 :
            # Iterate over all cols
            for c in range(ConnectFourBoard.num_cols):
                ret += self.__break_apart_line__(self.__get_line__(c, 0, dx, dy))
        return filter(lambda x: includeSingletons or len(x) > 1, ret)

    def __break_apart_line__(self, line) :
        """Given a line of pieces as returned by __get_line__, return a list of
        the maximal contiguous subsequences.  For example:
        [None, 1, None, 1, 1, 2, 2, 2] returns [[1],[1,1],[2,2,2]]."""
        ret = []
        current_chain = []

        while line :
            x = line.pop(0)
            if x is None or (current_chain and current_chain[0] != x) :
                if current_chain :
                    ret.append(current_chain)
                current_chain = []
            if x is not None and (not current_chain or current_chain[0] == x) :
                current_chain.append(x)
        else :
            if current_chain :
                ret.append(current_chain)
        return ret

    def get_northeast_chains(self, includeSingletons=False):
        return self.__get_diagonal_chains__(+1, -1, includeSingletons)

    def get_northwest_chains(self, includeSingletons=False):
        return self.__get_diagonal_chains__(-1, -1, includeSingletons)

    def __get_diagonal_chains__(self, dx, dy=-1, includeSingletons=False):
        indexes = self.__get_diagonal_indexes__(dx, dy, includeSingletons)
        chains =  map( lambda chain :
                       map(lambda (col, row) : self.get_piece(col, row), chain),
                       filter(lambda x : x,
                              indexes))
        chains = reduce(lambda a,b: a+b, map(self.__break_apart_line__, chains))
        chains = filter(lambda chain : includeSingletons or len(chain) > 1, chains)
        return chains

    def __get_diagonal_indexes__(self, dx, dy=-1, includeSingletons=False):
        indexes = []

        # north half of board
        col_start = 0 if dx>0 else self.num_cols - 1
        for row_start in range(self.num_rows - 1): # -1 to avoid double counting longest diagonal
            indexes.append(self.__make_index_list__(col_start, row_start, dx, dy))

        # south half of board
        row_start = self.num_rows - 1
        for col_start in range(self.num_cols): # including longest diagonal
            indexes.append(self.__make_index_list__(col_start, row_start, dx, dy))

        return indexes

    def __make_index_list__(self, col_start, row_start, dx, dy):
        ilist = []
        x, y = col_start, row_start
        while x >= 0 and y >= 0 and x < self.num_cols and y < self.num_rows:
            ilist.append((x, y))
            x += dx
            y += dy
        return ilist

    def __piece_type__(self, player=None) :
        player = player or self.whose_turn
        num_pieces = len(filter(lambda x: bool(x),
                                reduce(lambda a,b:a+b, self.board_array)))
        return [1,2][((player != self.whose_turn) + num_pieces) % 2]

    def __whose_piece__(self) :
        """Return a dictionary sending piece symbol to player name."""
        return dict([(self.__piece_type__(x), x) for x in self.players])

    def same_board_array(self, other):
        """Given two ConnectFourBoard objects, returns True if they have pieces in
        the same places (that is, same .board_array attribute), otherwise False."""
        return (is_class_instance(other, 'ConnectFourBoard')
                and (self.board_array == other.board_array))

    def __eq__(self, other):
        return (is_class_instance(other, 'ConnectFourBoard')
                and (self.board_array == other.board_array)
                and (self.prev_move_string == other.prev_move_string)
                and (self.players == other.players)
                and (self.whose_turn == other.whose_turn))

    def __str__(self) :
        ret = ""
        for row in self.board_array :
            ret += "".join(map( lambda x : {1 : "1 ", 2: "2 "}.get(x,"_ "), row))
            ret += "\n"
        return ret

class AnytimeValue :
    def __init__(self, val=None) :
        self.value = val
        self.history = []
        self.total_evaluations = 0
        if val is not None:
            self.set_value(val)
    def set_value(self, val):
        if not is_dfs_return_type(val):
            raise TypeError('AnytimeValue.set_value expected tuple (path, '
                            +'score, number of evaluations)')
        self.value = val
        self.history.append(val)
        self.total_evaluations += val[2]
    def get_value(self) :
        return self.value
    def pretty_print(self):
        print '*** Begin printing AnytimeValue history ***\n'
        for val in self.history:
            print '\nProgressive deepening to depth ' + str(len(val[0])-1) + ':'
            pretty_print_dfs_type(val)
        print '*** Done printing AnytimeValue history ***\n'
        print 'Total number of static evaluations:', self.total_evaluations, '\n'
    def __str__(self):
        return ("<AnytimeValue object representing %i levels of progressive deepening>"
                % len(self.history))
    __repr__ = __str__
    def copy(self):
        return deepcopy(self)

def is_class_instance(obj, class_name):
    return hasattr(obj, '__class__') and obj.__class__.__name__ == class_name

def is_AbstractGameState_instance(obj):
    return is_class_instance(obj, 'AbstractGameState')

def is_dfs_return_type(val):
    return (isinstance(val, (tuple, list))
            and len(val) == 3
            and isinstance(val[0], (tuple, list))
            and all(map(is_AbstractGameState_instance, val[0])))

def pretty_print_dfs_type(dfs_result):
    print pretty_format_dfs_type(dfs_result)

def pretty_format_dfs_type(dfs_result):
    if not is_dfs_return_type(dfs_result):
        raise TypeError('expected tuple (path, score, number of evaluations)')
    s = '\nPath:'
    for state in dfs_result[0]:
        s += '\n' + str(state.snapshot.__class__) + '\n' + str(state.snapshot)
    s += '\nScore: ' + str(dfs_result[1])
    s += '\nEvaluations: ' + str(dfs_result[2]) + '\n'
    return s

def move_sequence(state, move_indexes=[]) :
    """Produces a sequence of states, starting with the input state.
    For Connect Four, note that a move index may be different from a column
    number; for example, if the first open column is column 2, it will have
    a move index of 0."""
    return reduce(lambda states, index : states + [states[-1].generate_next_states()[index]],
                  move_indexes, [state])
