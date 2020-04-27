"""
Tic Tac Toe Player
"""

import math, copy

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
    c=0
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                c+=1
    if c%2==0:
        return X
    else:
        return O
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                s.add((i,j))
    return s
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0]>=3 or action[1]>=3 or action[0]<0 or action[1]<0 or board[action[0]][action[1]]!=EMPTY:
        raise IndexError
    nb=copy.deepcopy(board)
    nb[action[0]][ action[1]]=player(board)
    return nb
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0]==board[i][1] and board[i][1]==board[i][2]:
            return board[i][2]
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[2][i]
    if board[0][0]==board[1][1] and board[1][1]==board[2][2]:
            return board[2][2]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
    return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                return False

    return True
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    if player(board)==X:
        v=-math.inf
        best_action=None
        for action in actions(board):
            new_v=min_value(result(board,action),-100,100)
            if new_v>v:
                v=new_v
                #print(v)
                best_action=action
        return best_action
    elif player(board) == O:
        v = math.inf
        best_action = None
        for action in actions(board):
            new_v = max_value(result(board, action),-100,100)
            if new_v < v:
                v = new_v
                #print(v)
                best_action = action
        return best_action
    return None
    #raise NotImplementedError
    

def max_value(board,alpha,beta):
    
    if terminal(board):
        return utility(board)
    v=-math.inf
    for action in actions(board):
        new_v=min_value(result(board,action),alpha,beta)
        v=max(v,new_v)
        alpha=max(alpha,new_v)
        if beta <= alpha:
            break
    return v 

def min_value(board,alpha,beta):
    
    if terminal(board):
        return utility(board)
    v=math.inf
    for action in actions(board):
        new_v = max_value(result(board, action),alpha,beta)
        v=min(v,new_v)
        beta=min(beta,new_v)
        if alpha >= beta:
            break
    return v 




