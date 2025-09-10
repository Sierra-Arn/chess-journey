import random

piece_score = {'K': 1000, 'Q': 30, 'R': 18, 'B': 15, 'N': 15, 'p': 5}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

pawn_scores = [[5, 5, 5, 5, 5, 5, 5, 5],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [3, 3, 3, 3, 3, 3, 3, 3],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [3, 3, 3, 3, 3, 3, 3, 3],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [5, 5, 5, 5, 5, 5, 5, 5]]

rook_scores = [[18, 5, 5, 18, 5, 18, 5, 18],
               [18, 5, 5, 5, 5, 5, 5, 18],
               [18, 10, 4, 4, 4, 4, 10, 18],
               [18, 5, 4, 1, 1, 4, 5, 18],
               [18, 5, 4, 1, 1, 4, 5, 18],
               [18, 10, 4, 4, 4, 4, 10, 18],
               [18, 5, 5, 5, 5, 5, 5, 18],
               [18, 5, 5, 18, 5, 18, 5, 18]]

knight_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 8, 2, 2, 8, 2, 1],
                 [1, 2, 15, 15, 15, 15, 2, 1],
                 [1, 2, 15, 2, 2, 15, 2, 1],
                 [1, 2, 15, 2, 2, 15, 2, 1],
                 [1, 2, 15, 15, 15, 15, 2, 1],
                 [1, 2, 8, 2, 2, 8, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_scores = [[15, 1, 1, 1, 1, 1, 1, 15],
                 [1, 15, 2, 1, 1, 2, 15, 1],
                 [1, 2, 15, 9, 9, 15, 2, 1],
                 [1, 1, 9, 15, 15, 9, 1, 1],
                 [1, 1, 9, 15, 15, 9, 1, 1],
                 [1, 2, 15, 9, 9, 15, 2, 1],
                 [1, 15, 2, 1, 1, 2, 15, 1],
                 [15, 1, 1, 1, 1, 1, 1, 15]]

queen_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 20, 20, 20, 20, 20, 20, 1],
                [1, 20, 30, 30, 30, 30, 20, 1],
                [1, 20, 30, 20, 20, 30, 20, 1],
                [1, 20, 30, 20, 20, 30, 20, 1],
                [1, 20, 30, 30, 30, 30, 20, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

king_scores = [[1, 1, 100, 1, 1, 1, 100, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 100, 1, 1, 1, 100, 1]]

piece_positions_scores = {"N": knight_scores, 'Q': queen_scores, 'B': bishop_scores, 'p': pawn_scores, 'R': rook_scores, 'K': king_scores}

def random_move_algorithm(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

#----------------------------------------

def greed_algorithm(gs, valid_moves):
    turn_multiplier = 1 if gs.WhiteToMove else -1
    max_score = CHECKMATE
    best_move = None
    for player_move in valid_moves:
        gs.make_move(player_move)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turn_multiplier * score_material(gs.board)
        if score > max_score:
            max_score = score
            best_move = player_move
        gs.undo_move()
    return best_move


def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score

#-----------------------------------------------

def prototype_MinMax(gs, valid_moves):
    turn_multiplier = 1 if gs.WhiteToMove else -1
    opponent_minmax_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        if gs.stalemate:
            opponent_max_score = STALEMATE
        elif gs.checkmate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                #gs.get_valid_moves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(gs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_minmax_score:
            opponent_minmax_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move

#-----------------------------------------------

def find_best_move_minmax(gs, valid_moves):
    global next_move
    next_move = None
    find_move_minmax(gs, valid_moves, DEPTH, gs.WhiteToMove)
    return next_move


def score_board_point01(gs):
    if gs.checkmate:
        if gs.WhiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score


def find_move_minmax(gs, valid_moves, depth, WhiteToMove):
    global next_move
    if depth == 0:
        return score_material(gs.board)

    if WhiteToMove:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_minmax(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score

    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_minmax(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

#---------------------------------------------------------------

def find_move_negamax(gs, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board_point01(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = - find_move_negamax(gs, next_moves, depth-1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score


def find_best_move_negamax(gs, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_move_negamax(gs, valid_moves, DEPTH, 1 if gs.WhiteToMove else -1)
    return next_move

#-----------------------------------------------------------------------------------

def find_move_negamax_alphabeta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board_point02(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = - find_move_negamax_alphabeta(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move, score)
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def find_best_move_negamax_alphabeta(gs, valid_moves):
    global next_move, counter
    next_move = None
    random.shuffle(valid_moves)
    counter = 0
    find_move_negamax_alphabeta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.WhiteToMove else -1)
    print(counter)
    return next_move


def score_board_point02(gs):
    if gs.checkmate:
        if gs.WhiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):  # for row in gs.board
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piece_positions_score = piece_positions_scores[square[1]][row][col]
        # for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]] + piece_positions_score * .1
            elif square[0] == 'b':
                score -= (piece_score[square[1]] + piece_positions_score * .1)

    return score
