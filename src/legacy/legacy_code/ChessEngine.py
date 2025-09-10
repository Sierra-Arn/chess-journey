class Game_state():
    def __init__(self):
        # board is an 8x8 list, each element of the list has 2 characters
        # The first character represents the color of the piece< 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'
        # "--" - represents an empty space with no piece
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.move_functions = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.WhiteToMove = True
        self.move_log = []

        self.white_King_location = (7, 4)
        self.black_King_location = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False

        self.en_passant_possible = ()  # coordinates for the square where en-passant is possible
        self.en_passant_possible_log = [self.en_passant_possible]

        self.current_castle_rights = Castle_rights(True, True, True, True)
        self.castle_rights_log = [Castle_rights(self.current_castle_rights.white_king_side,
                                                self.current_castle_rights.white_queen_side,
                                                self.current_castle_rights.black_king_side,
                                                self.current_castle_rights.black_queen_side)]

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.WhiteToMove = not self.WhiteToMove
        if move.piece_moved == "wK":
            self.white_King_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_King_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
        # en passant
        if move.is_en_passant_move:
            self.board[move.start_row][move.end_col] = '--'  # en-passant move itself

        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advances
            self.en_passant_possible = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.en_passant_possible = ()

        self.en_passant_possible_log.append(self.en_passant_possible)

        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = '--'

        self.update_castle_rights(move)
        self.castle_rights_log.append(Castle_rights(self.current_castle_rights.white_king_side,
                                                self.current_castle_rights.white_queen_side,
                                                self.current_castle_rights.black_king_side,
                                                self.current_castle_rights.black_queen_side))

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()  # reverse function
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.WhiteToMove = not self.WhiteToMove  # swap
            if move.piece_moved == "wK":
                self.white_King_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_King_location = (move.start_row, move.start_col)

            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.en_passant_possible_log.pop()
            self.en_passant_possible = self.en_passant_possible_log[-1]

            self.castle_rights_log.pop()
            new_rights = self.castle_rights_log[-1]
            self.current_castle_rights = Castle_rights(new_rights.white_king_side, new_rights.white_queen_side, new_rights.black_king_side, new_rights.black_queen_side)

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.CheckForPinsAndChecks()
        if self.WhiteToMove:
            king_row = self.white_King_location[0]
            king_col = self.white_King_location[1]
        else:
            king_row = self.black_King_location[0]
            king_col = self.black_King_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check
                moves = self.get_all_possible_moves()  # to move king or block check
                check = self.checks[0]  # check information below
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]  # enemy piece causing the check
                valid_squares = []
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block of capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:  # double check
                self.get_king_moves(king_row, king_col, moves)
        else:  # there's no check
            moves = self.get_all_possible_moves()
        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
                print('Checkmate')
            else:
                self.stalemate = True
                print('Stalemate')

        return moves

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)  # calls the appropriate function based on the piece

        return moves

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.WhiteToMove:
            move_pawn = -1
            start_row = 6
            enemy_color = 'b'
            king_row, king_col = self.white_King_location
        else:
            move_pawn = 1
            start_row = 1
            enemy_color = 'w'
            king_row, king_col = self.black_King_location

        if self.board[r + move_pawn][c] == '--':
            if not piece_pinned or pin_direction == (move_pawn, 0):
                moves.append(Move((r, c), (r + move_pawn, c), self.board))
                if r == start_row and self.board[r + 2 * move_pawn][c] == '--':
                    moves.append(Move((r, c), (r + 2 * move_pawn, c), self.board))

        if c - 1 >= 0:
            if not piece_pinned or pin_direction == (move_pawn, -1):
                if self.board[r + move_pawn][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_pawn, c - 1), self.board))
                if (r + move_pawn, c - 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c:
                            inside_range = range(king_col + 1, c - 1)  # positive direction, just 1, so we don't write it
                            outside_range = range(c+1, 8)
                        else:
                            inside_range = range(king_col - 1, c, - 1)  # -1 -- negative direction
                            outside_range = range(c-2, -1, -1)  # -1 -- negative direction
                        for i in inside_range:
                            if self.board[r][i] != '--':  # some other pieces beside en passant pawn
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_pawn, c - 1), self.board, en_passant_move=True))

        if c + 1 <= 7:  # captures to the right
            if not piece_pinned or pin_direction == (move_pawn, 1):
                if self.board[r + move_pawn][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_pawn, c + 1), self.board))
            if (r + move_pawn, c + 1) == self.en_passant_possible:
                attacking_piece = blocking_piece = False
                if king_row == r:
                    if king_col < c:
                        inside_range = range(king_col + 1, c)  # positive direction, just 1, so we don't write it
                        outside_range = range(c + 2, 8)
                    else:
                        inside_range = range(king_col - 1, c+1, - 1)  # -1 -- negative direction
                        outside_range = range(c - 1, -1, -1)  # -1 -- negative direction
                    for i in inside_range:
                        if self.board[r][i] != '--':  # some other pieces beside en passant pawn
                            blocking_piece = True
                    for i in outside_range:
                        square = self.board[r][i]
                        if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                            attacking_piece = True
                        elif square != '--':
                            blocking_piece = True
                if not attacking_piece or blocking_piece:
                    moves.append(Move((r, c), (r + move_pawn, c + 1), self.board, en_passant_move=True))

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":  # Queen exception
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.WhiteToMove:
            enemy_color = "b"
        else:
            enemy_color = "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == (-d[0], -d[1]) or pin_direction == d:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c,), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if self.WhiteToMove:
            ally_color = "w"
        else:
            ally_color = "b"
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.WhiteToMove:
            ally_color = "w"
        else:
            ally_color = "b"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == (-d[0], -d[1]) or pin_direction == d:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == ally_color:
                            break
                        else:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                    else:
                        break

    def get_queen_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.WhiteToMove:
            enemy_color = "b"
        else:
            enemy_color = "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == (-d[0], -d[1]) or pin_direction == d:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c,), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        if self.WhiteToMove:
            ally_color = "w"
        else:
            ally_color = "b"
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == "w":
                        self.white_King_location = (end_row, end_col)
                    elif ally_color == "b":
                        self.black_King_location = (end_row, end_col)
                    in_check, pins, checks = self.CheckForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == "w":
                        self.white_King_location = (r, c)
                    else:
                        self.black_King_location = (r, c)

        self.get_castle_moves(r, c, moves, ally_color)

    def CheckForPinsAndChecks(self):
        pins = []  # figures protecting king
        checks = []  # direction of check
        in_check = False
        if self.WhiteToMove:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_King_location[0]
            start_col = self.white_King_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_King_location[0]
            start_col = self.black_King_location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():  # list of allied piece could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:  # there's second allied piece so no pin or check are possible
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        # rook orthogonally
                        # bishop diagonally
                        # pawn 1 square diagonally
                        # queen any direction
                        # king any direction 1 square away
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or (i == 1 and type == "K") or \
                                (i == 1 and type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or
                                                             (enemy_color == "b" and 4 <= j <= 5))) or (type == "Q"):
                            if possible_pin == ():  # no piece's blocking so check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:  # piece's blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:  # off board
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

    def square_under_attack(self, r, c, ally_color):
        if ally_color == 'b':
            enemy_color = 'w'
        else:
            enemy_color = 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color:
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        # rook orthogonally
                        # bishop diagonally
                        # pawn 1 square diagonally
                        # queen any direction
                        # king any direction 1 square away
                        if (0 <= j < 3 and type == "R") or (4 <= j < 7 and type == "B") or (i == 1 and type == "K") or \
                                (i == 1 and type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or
                                                             (enemy_color == "b" and 4 <= j <= 5))) or (type == "Q"):
                            return True
                        else:
                            break
                else:  # off board
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":
                    return True
        return False

    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castle_rights.white_king_side = False
            self.current_castle_rights.white_queen_side = False
        elif move.piece_moved == 'bK':
            self.current_castle_rights.black_king_side = False
            self.current_castle_rights.black_queen_side = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castle_rights.white_queen_side = False
                elif move.start_col == 7:
                    self.current_castle_rights.white_king_side = False
        elif move.piece_moved == 'bR':
            if move.start_col == 0:
                self.current_castle_rights.black_queen_side = False
            elif move.start_col == 7:
                self.current_castle_rights.black_king_side = False

        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castle_rights.white_queen_side = False
                elif move.end_col == 7:
                    self.current_castle_rights.white_king_side = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castle_rights.black_queen_side = False
                elif move.end_col == 7:
                    self.current_castle_rights.black_king_side = False

    def get_castle_moves(self, r, c, moves, ally_color):
        if self.square_under_attack(r, c, ally_color):
            return
        if (self.WhiteToMove and self.current_castle_rights.white_king_side) or (not self.WhiteToMove and self.current_castle_rights.black_king_side):
            self.get_king_side_castle_moves(r, c, moves, ally_color)
        if (self.WhiteToMove and self.current_castle_rights.white_queen_side) or (not self.WhiteToMove and self.current_castle_rights.black_queen_side):
            self.get_queen_side_castle_moves(r, c, moves, ally_color)

    def get_king_side_castle_moves(self, r, c, moves, ally_color):
        if self.board[r][c+1] == self.board[r][c+2] == '--':
            if not self.square_under_attack(r, c + 1, ally_color) and not self.square_under_attack(r, c + 2, ally_color):
                moves.append(Move((r, c), (r, c + 2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, r, c, moves, ally_color):
        if self.board[r][c - 1] == self.board[r][c - 2] == self.board[r][c - 3] == '--':
            if not self.square_under_attack(r, c - 1, ally_color) and not self.square_under_attack(r, c - 2, ally_color):
                moves.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))

class Castle_rights():
    def __init__(self, white_king_side, black_king_side, white_queen_side, black_queen_side):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side


class Move():

    # key : value
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    # reverse key and values
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, en_passant_move=False, is_castle_move=False, checkmate=False, stalemate=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # en-passant
        self.is_en_passant_move = en_passant_move
        if self.is_en_passant_move:
            if self.piece_moved == 'wp':
                self.piece_captured = 'bp'
            else:
                self.piece_captured = 'wp'

        self.is_pawn_promotion = False
        if self.piece_moved[1] == "p" and ((self.end_row == 0) or (self.end_row == 7)):
            self.is_pawn_promotion = True

        self.is_castle_move = is_castle_move
        self.checkmate = checkmate
        self.stalemate = stalemate
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
    '''
    Overriding the equals
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    def __str__(self):

        start_square = self.get_rank_file(self.start_row, self.start_col)
        end_square = self.get_rank_file(self.end_row, self.end_col)

        if self.is_castle_move:
            return '0-0' if self.end_col == 6 else '0-0-0'

        elif self.piece_moved[1] == 'p':
            if self.is_en_passant_move:
                return 'e.p.' + start_square + end_square
            if self.is_pawn_promotion:
                return end_square + ' Q'
            else:
                return start_square + end_square

        elif self.checkmate:
            return self.piece_moved[1] + start_square + end_square + '#'

        elif self.stalemate:
            return self.piece_moved[1] + start_square + end_square + '='

        else:
            return self.piece_moved[1] + start_square + end_square
