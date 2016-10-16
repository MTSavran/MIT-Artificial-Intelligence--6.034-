# MIT 6.034 Lab 3: Games

from game_api import ConnectFourBoard
from toytree import *

# ------- PART I: CONNECTFOUR BOARDS
# Note: The tester uses some of these boards, so if you change them, tests may
# break.  However, feel free to copy these to make new boards of your own.

BOARD_UHOH = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,2,0,0,0 ),
                                    ( 0,0,2,1,0,1,1 ),
                                    ),
                                  players = ['Callie', 'English'],
                                  whose_turn = 'Callie')

# NO-WIN GAME COMPLETELY FULL
BOARD_FULL_TIED = ConnectFourBoard(board_array =
                                  ( ( 2,2,1,2,1,1,1 ),
                                    ( 1,2,1,1,2,2,2 ),
                                    ( 2,1,2,1,2,1,1 ),
                                    ( 2,1,1,1,2,2,2 ),
                                    ( 1,2,1,2,1,2,2 ),
                                    ( 1,1,2,1,2,1,2 ),
                                    ),
                                  players = ['Weiss', 'Schwarz'],
                                  whose_turn = 'Schwarz')

# one move before BOARD_FULL_TIED
BOARD_FULL_TIED_minus3 = ConnectFourBoard(board_array =
                                  ( ( 2,2,1,0,1,1,1 ),
                                    ( 1,2,1,1,2,2,2 ),
                                    ( 2,1,2,1,2,1,1 ),
                                    ( 2,1,1,1,2,2,2 ),
                                    ( 1,2,1,2,1,2,2 ),
                                    ( 1,1,2,1,2,1,2 ),
                                    ),
                                  players = ['Alethea', 'Apate'],
                                  whose_turn = 'Alethea')

# PLAYER ONE WON IN NW DIAGONAL PATTERN
PLAYER_ONE1_WON = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,1,0,0,0,0,0 ),
                                    ( 0,2,1,1,1,0,0 ),
                                    ( 0,2,1,1,2,0,0 ),
                                    ( 0,2,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                    ),
                                  whose_turn = 'Player Two')

PLAYER_TWO1_WON = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,1,0,0,0,0,0 ),
                                    ( 0,2,1,1,1,0,0 ),
                                    ( 0,2,1,1,2,0,0 ),
                                    ( 0,2,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                    ),
                                  whose_turn = 'Player One') #2 = Player One

# PLAYER TWO WON HORIZONTALLY
PLAYER_TWO2_WON = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,1,0,0,0 ),
                                    ( 0,2,2,2,2,0,0 ),
                                    ( 0,1,1,2,1,0,0 ),
                                    ( 0,1,2,2,1,0,0 ),
                                    ( 2,1,1,1,2,0,0 ),
                                    ),
                                  whose_turn = 'Player One')

PLAYER_2_PATRICK_WON = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,1,0,0,0 ),
                                    ( 0,2,2,2,2,0,0 ),
                                    ( 0,1,1,2,1,0,0 ),
                                    ( 0,1,2,2,1,0,0 ),
                                    ( 2,1,1,1,2,0,0 ),
                                    ),
                                  players = ['Siri', 'Patrick'],
                                  whose_turn = 'Siri') # 2=Patrick

# PLAYER TWO WON IN TWO WAYS (HORIZONTAL AND NW)
PLAYER_2_ALICE_DOMINATED = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,2,2,2,2,0,0 ),
                                    ( 0,1,2,1,2,1,0 ),
                                    ( 0,2,1,1,1,2,0 ),
                                    ( 0,1,1,2,2,1,2 ),
                                    ( 0,1,2,1,1,1,2 ),
                                    ),
                                  players = ['Alice', 'Bob'],
                                  whose_turn = 'Bob')



# PLAYER ONE SHOULD CHOOSE NOT TO MOVE IN THE FIRST COLUMN.
# PLAYER ONE WINS IN THREE MOVES IN OPTIMAL PLAY.
NEARLY_OVER = ConnectFourBoard(board_array =
                                 ( ( 0,2,1,2,1,0,1 ),
                                   ( 0,2,1,1,2,2,2 ),
                                   ( 0,1,2,1,2,1,1 ),
                                   ( 0,1,1,1,2,2,2 ),
                                   ( 0,2,1,2,1,2,2 ),
                                   ( 1,1,2,2,1,1,2 ),
                                   ),
                                 players = ['Harry', 'Ron'],
                                 whose_turn = 'Harry')



BOARD_PARTIAL = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                    ),
                                  players = ['Crowley', 'Aziraphael'],
                                  whose_turn = 'Aziraphael')



BOARD_EMPTY = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ),
                                  players = ['Luke', 'Leia'],
                                  whose_turn = 'Luke')

BOARD_FIVE_IN_A_ROW = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,2,0,0,0,2,0 ),
                                    ( 2,1,1,1,1,1,2 ),
                                    ),
                                  players = ['Rey', 'Finn'],
                                  whose_turn = 'Finn')

BOARD_ONEFISH_WON_FAST = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,2,2,0,0,0 ),
                                    ( 1,1,1,1,2,0,0 ),
                                    ),
                                  players = ['One Fish', 'Two Fish'],
                                  whose_turn = 'Two Fish')

BOARD_REDFISH_WON_LESS_FAST = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,2,2,2,0,0 ),
                                    ( 1,1,1,1,2,1,0 ),
                                    ),
                                  players = ['Red Fish', 'Blue Fish'],
                                  whose_turn = 'Blue Fish')

BOARD_1_WINNING_BARELY = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,2,0,0 ),
                                    ( 0,2,0,2,1,0,0 ),
                                    ( 0,1,2,1,2,0,0 ),
                                    ( 0,1,2,1,2,1,0 ),
                                    ( 2,1,1,1,2,1,2 ),
                                    ) ) # current player winning; 10 pieces/player

BOARD_2_WINNING_DEFINITELY = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 1,0,0,0,0,0,1 ),
                                    ( 1,0,1,0,0,0,1 ),
                                    ( 2,0,2,1,2,0,2 ),
                                    ( 1,0,2,2,2,0,1 ),
                                    ( 1,0,2,2,2,0,1 ),
                                    ) ) # current player losing; 10 pieces/player

BOARD_2_WINNING_LESS_PIECES = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,0,0,0,0 ),
                                    ( 1,2,2,2,0,0,1 ),
                                    ) ) # current player losing; 3 pieces/player


## Boards that can result from making one move in one of the boards above

NEARLY_OVER_move0 = ConnectFourBoard(board_array =
                                 ( ( 0,2,1,2,1,0,1 ),
                                   ( 0,2,1,1,2,2,2 ),
                                   ( 0,1,2,1,2,1,1 ),
                                   ( 0,1,1,1,2,2,2 ),
                                   ( 1,2,1,2,1,2,2 ),
                                   ( 1,1,2,2,1,1,2 ),
                                 ) )

NEARLY_OVER_move5 = ConnectFourBoard(board_array =
                                 ( ( 0,2,1,2,1,1,1 ),
                                   ( 0,2,1,1,2,2,2 ),
                                   ( 0,1,2,1,2,1,1 ),
                                   ( 0,1,1,1,2,2,2 ),
                                   ( 0,2,1,2,1,2,2 ),
                                   ( 1,1,2,2,1,1,2 ),
                                 ) )

NEARLY_OVER_move5_0 = ConnectFourBoard(board_array =
                                 ( ( 0,2,1,2,1,1,1 ),
                                   ( 0,2,1,1,2,2,2 ),
                                   ( 0,1,2,1,2,1,1 ),
                                   ( 0,1,1,1,2,2,2 ),
                                   ( 2,2,1,2,1,2,2 ),
                                   ( 1,1,2,2,1,1,2 ),
                                 ) )

NEARLY_OVER_move5_0_0 = ConnectFourBoard(board_array = #game over
                                 ( ( 0,2,1,2,1,1,1 ),
                                   ( 0,2,1,1,2,2,2 ),
                                   ( 0,1,2,1,2,1,1 ),
                                   ( 1,1,1,1,2,2,2 ),
                                   ( 2,2,1,2,1,2,2 ),
                                   ( 1,1,2,2,1,1,2 ),
                                 ) )


BOARD_PARTIAL_move0 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 2,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move1 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,2,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move2 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,2,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move3 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,2,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move4 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,2,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move5 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,2,0 ),
                                    ( 0,1,2,2,1,2,0 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )

BOARD_PARTIAL_move6 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,1,0,0,0 ),
                                    ( 0,0,2,1,2,0,0 ),
                                    ( 0,1,2,2,1,2,2 ),
                                    ( 2,1,1,1,2,2,1 ),
                                 ) )


BOARD_EMPTY_move0 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 1,0,0,0,0,0,0 ),
                                 ) )

BOARD_EMPTY_move1 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,1,0,0,0,0,0 ),
                                 ) )

BOARD_EMPTY_move2 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,1,0,0,0,0 ),
                                 ) )

BOARD_EMPTY_move3 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,1,0,0,0 ),
                                 ) )

BOARD_EMPTY_move4 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,1,0,0 ),
                                 ) )

BOARD_EMPTY_move5 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,1,0 ),
                                 ) )

BOARD_EMPTY_move6 = ConnectFourBoard(board_array =
                                  ( ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,0 ),
                                    ( 0,0,0,0,0,0,1 ),
                                 ) )
