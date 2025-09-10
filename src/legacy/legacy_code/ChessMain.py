import pygame as p
import ChessEngine, ChessAI

BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8
MOVE_LOG_PANEL_WIDTH = 256
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
SQ_SIZE = BOARD_HEIGHT // DIMENSION
IMAGES = {}

def load_images():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'bQ', 'wQ', 'wK', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess_images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying 'IMAGES['wp']'

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    p.display.set_caption("Chess")  # name of the program
    img = p.image.load("chess_images/bK.png")  # icon of the program
    p.display.set_icon(img)
    screen.fill(p.Color('white'))
    move_log_font = p.font.SysFont("Helvitca", 20, False, False)  # Arial
    gs = ChessEngine.Game_state()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    sq_selected = ()  # col and row
    player_clicks = []  # keep track of player clicks
    game_over = False
    running = True
    player_one = True  # human plays on white side if true
    player_two = True  # AI plays on black side if false
    while running:
        human_turn = (gs.WhiteToMove and player_one) or (not gs.WhiteToMove and player_two)
        for e in p.event.get():  # stable function
            if e.type == p.QUIT:
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8:  # unable to move figure on the same spot
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                sq_selected = ()  # reset
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:  # undo move once
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
                    game_over = False
                if e.key == p.K_c:  # undo moves twice
                    gs.undo_move()
                    gs.undo_move()
                    move_made = True
                    game_over = False
                if e.key == p.K_r:  # reset
                    gs = ChessEngine.Game_state()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False

        if not game_over and not human_turn:  # AI PLAYS
            AI_move = ChessAI.find_best_move_negamax_alphabeta(gs, valid_moves)
            if AI_move is None:
                AI_move = ChessAI.random_move_algorithm(valid_moves)
            gs.make_move(AI_move)
            move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font)

        if gs.checkmate or gs.stalemate:
            game_over = True
            draw_endgame_text(screen, 'STALEMATE!' if gs.stalemate else 'Black wins by checkmate!'
                                                if gs.WhiteToMove else 'White wins by checkmate!')

        p.display.flip()

def draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)

def draw_board(screen):
    colors = [p.Color('gray'), p.Color('brown')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_move_log(screen, gs, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("brown"), move_log_rect)
    move_log = gs.move_log
    move_texts = []

    for i in range(0, len(move_log), 2):
        move_string = str(i//2 + 1) + ". " + str(move_log[i]) + "  "
        if i + 1 < len(move_log):
            move_string += str(move_log[i+1]) + "  "
        move_texts.append(move_string)
        if (i // 2 ) == 50:
            gs.stalemate = True

    moves_per_row = 2
    padding = 5
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_object = font.render(text, True, p.Color('Gray'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height()  # + line_spacing if you want to

def draw_endgame_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, True, p.Color('Black'))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH // 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT // 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    # text_object = font.render(text, True, p.Color('Gray'))
    # screen.blit(text_object, text_location.move(2, 2))

def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))  # selected square
            s.set_alpha(100)  # transparency value (0 transparent; 255 oraque)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('purple'))  # from that square
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

if __name__ == " __main__ ":
    main()

main()