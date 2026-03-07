import math
from game import WIN_COMBINATIONS

def evaluate(state):
    winner = state.check_global_win()
    if winner == 'O': return 1000
    if winner == 'X': return -1000

    score = 0
    for s in state.smallBoardStatus:
        if s == 'O': score += 10
        elif s == 'X': score -= 10

    if state.smallBoardStatus[4] == 'O': score += 5
    if state.smallBoardStatus[4] == 'X': score -= 5

    return score

def minimax(state, depth, alpha, beta, maximizing):
    if depth == 0 or state.check_global_win():
        return evaluate(state)

    boards = range(9) if state.nextBoard == -1 else [state.nextBoard]

    if maximizing:
        best = -math.inf
        for b in boards:
            if state.smallBoardStatus[b] is not None: continue
            for c in range(9):
                if state.board[b][c] is None:
                    old_nb = state.nextBoard
                    old_sb = state.smallBoardStatus[b]

                    state.board[b][c] = 'O'
                    state.update_small_board(b)
                    state.nextBoard = c if state.smallBoardStatus[c] is None else -1

                    val = minimax(state, depth-1, alpha, beta, False)

                    state.board[b][c] = None
                    state.smallBoardStatus[b] = old_sb
                    state.nextBoard = old_nb

                    best = max(best, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = math.inf
        for b in boards:
            if state.smallBoardStatus[b] is not None: continue
            for c in range(9):
                if state.board[b][c] is None:
                    old_nb = state.nextBoard
                    old_sb = state.smallBoardStatus[b]

                    state.board[b][c] = 'X'
                    state.update_small_board(b)
                    state.nextBoard = c if state.smallBoardStatus[c] is None else -1

                    val = minimax(state, depth-1, alpha, beta, True)

                    state.board[b][c] = None
                    state.smallBoardStatus[b] = old_sb
                    state.nextBoard = old_nb

                    best = min(best, val)
                    beta = min(beta, val)
                    if beta <= alpha:
                        return best
        return best

def find_best_move(state, depth=3):
    best_score = -math.inf
    move = None

    boards = range(9) if state.nextBoard == -1 else [state.nextBoard]

    for b in boards:
        if state.smallBoardStatus[b] is not None: continue
        for c in range(9):
            if state.board[b][c] is None:
                old_nb = state.nextBoard
                old_sb = state.smallBoardStatus[b]

                state.board[b][c] = 'O'
                state.update_small_board(b)
                state.nextBoard = c if state.smallBoardStatus[c] is None else -1

                score = minimax(state, depth-1, -math.inf, math.inf, False)

                state.board[b][c] = None
                state.smallBoardStatus[b] = old_sb
                state.nextBoard = old_nb

                if score > best_score:
                    best_score = score
                    move = (b, c)

    return move
