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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Os = 0
    Xs = 0
    for row in board:
        Os += row.count(O)
        Xs += row.count(X)

    if Os == Xs:
        return X
    else:
        return O
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    brd = range(len(board))
    for i in brd:
        for j in brd:
            if board[i][j] is EMPTY:
                actions.add((i, j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    player_turn = player(board)
    valid_actions = actions(board)
    if action in valid_actions:
        new_board[action[0]][action[1]] = player_turn
    else:
        raise NameError('invalid action')
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None

    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            winner = board[i][0]
            break
        elif board[0][i] == board[1][i] == board[2][i]:
            winner = board[0][i]
            break

    if winner == None:
        if board[0][0] == board[1][1] == board[2][2]:
            winner = board[0][0]
        elif board[0][2] == board[1][1] == board[2][0]:
            winner = board[0][2]

    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    emp = 0
    for row in board:
        emp += row.count(EMPTY)
    if emp == 0 or winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    if the_winner == X:
        return 1
    elif the_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
        
    player_turn = player(board)

    if player_turn == X:
        max_val = max_value(board)
        for action in actions(board):
            if min_value(result(board, action)) == max_val:
                return action
                
    elif player_turn == O:
        min_val = min_value(board)
        for action in actions(board):
            if max_value(result(board, action)) == min_val:
                return action


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v