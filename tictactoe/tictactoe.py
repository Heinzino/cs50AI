"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board:list):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return EMPTY
    
    numX = 0 
    numO = 0
    for row in board:
        for cell in row:
            if cell == X:
                numX += 1
            if cell == O:
                numO += 1

    if(numX == numO):
        return X
    elif(numX-1 == numO):
        return O
    else:
        return EMPTY


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_all_possible_actions = set()

    if terminal(board):
        return None

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_all_possible_actions.add(((i,j)))

    return set_of_all_possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    #Degenerate cases
    if not isinstance(action,tuple):
        raise ValueError
    if terminal(board):
        raise ValueError
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError

    player_to_move = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = player_to_move
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one. Else returns None.
    Assumes no two winners at the same time as that's an invalid board
    """

    win_by_diag = ( (board[0][0] == board[1][1] and board[1][1] == board[2][2]) 
                      or (board[0][2] == board[1][1] and board[1][1] == board[2][0]) )
    if(win_by_diag):
         return board[1][1]

    for row in board:
        if(row[0] == row[1] and row[1] == row[2]):
            return row[1]
    
    for i in range(3):
        if(board[0][i] == board[1][i] and board[1][i] == board[2][i]):
            return board[0][i]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assume terminal board is given
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board) -> tuple:
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    tryingToMaximize = True    

    if currentPlayer == O:
        tryingToMaximize = False
    elif currentPlayer == X:
        tryingToMaximize = True
    else:
        return None
    

    def max_value(board) -> tuple:
    
        if terminal(board):
            return utility(board),None
        
        highest_value = -math.inf
        optimalAction = None

        for action in actions(board):
            val,act = min_value(result(board,action))
            if(val > highest_value):
                highest_value = val
                optimalAction = action

                if highest_value == 1: #if this action makes me win TAKE IT! optimization
                    return highest_value,optimalAction
                
        return highest_value,optimalAction

    def min_value(board) -> tuple:

        if terminal(board):
            return utility(board),None

        lowest_value = math.inf
        optimalAction = None

        for action in actions(board):
            val,act  = max_value(result(board,action))
            if(val < lowest_value):
                lowest_value = val
                optimalAction = action

                if lowest_value == -1:
                    return lowest_value,optimalAction
                
        return lowest_value,optimalAction

    
    if tryingToMaximize:
        val,optimalAction = max_value(board)
    else:
        val,optimalAction = min_value(board)

    return optimalAction

    
