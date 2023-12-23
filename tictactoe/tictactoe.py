"""
Tic Tac Toe Player
"""

import math

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

    """
    TODO: terminal() implementation
    if terminal(board):
        return None
    """

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_all_possible_actions.add(((i,j)))

    return set_of_all_possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


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
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
