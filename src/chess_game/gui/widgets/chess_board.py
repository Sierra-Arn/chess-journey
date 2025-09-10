# src/chess_game/gui/widgets/chess_board.py
from typing import Optional, Tuple, Callable, List
import random
from pygame import Rect, Surface, Color
import pygame
import chess
from ..components import RectType
from ..config import gui_config
from ...assets import image_loader

class ChessBoardWidget:
    """
    Chess board widget for displaying and interacting with a chess game.

    Handles drawing and input processing internally without pygame_gui dependency.
    Uses ImageLoader to render real piece PNGs.
    Supports Chess960, board flipping, move highlighting and callbacks.

    Attributes:
        rect: Widget position and dimensions (x, y, width, height).
        on_move_made: Callback function when a legal move is made.
        flip_board: Flag indicating whether to display board from black's perspective.
        chess960: Flag indicating whether to use random Chess90 starting position.
        board: chess.Board instance representing current game state.
        selected_square: Currently selected chess square (None if no selection).
        possible_moves: List of legal moves from the selected square.
        light_square_color: Color for light squares from config.
        dark_square_color: Color for dark squares from config.
        selected_square_color: Highlight color for selected square.
        possible_move_color: Highlight color for possible move indicators.
        border_width: Width of board border from config.
        board_border_color: Color of board border from config.
    """

    def __init__(
        self,
        rect: RectType,
        on_move_made: Optional[Callable[[chess.Move], None]] = None,
        flip_board: bool = False,
        chess960: bool = False
    ):
        self.rect = Rect(rect)

        # Callbacks
        self.on_move_made = on_move_made
        self.flip_board = flip_board
        self.chess960 = chess960

        # Game state
        self.board = self._create_board()

        self.selected_square: Optional[chess.Square] = None
        self.possible_moves: List[chess.Move] = []

        # Visuals from config
        self.light_square_color = Color(*gui_config.square_light_color)
        self.dark_square_color = Color(*gui_config.square_dark_color)
        self.selected_square_color = Color(*gui_config.square_selected_color)
        self.possible_move_color = Color(*gui_config.square_possible_move_color)
        self.border_width = gui_config.board_border_width
        self.board_border_color = Color(*gui_config.board_border_color)

        # Load images if not loaded
        image_loader.load_all_images()

    def _create_board(self) -> chess.Board:
        """
        Create a chess.Board: normal start or random Chess960 position.
        
        Returns:
            Initialized chess.Board instance with appropriate starting position.
        """
        if self.chess960:
            random_pos = random.randint(0, 959)
            board = chess.Board.from_chess960_pos(random_pos)
            return board
        else:
            return chess.Board()

    def draw(self, surface: Surface) -> None:
        """
        Draw the chess board, pieces and move indicators using unified coordinate mapping.
        
        Renders all squares with appropriate colors, pieces using ImageLoader,
        selection highlights, possible move indicators, and board border.
        
        Args:
            surface: pygame Surface to draw on.
        """
        board_x, board_y, board_size, square_size = self._get_board_geometry()

        # Draw all squares and pieces
        self._draw_squares_and_pieces(surface, board_x, board_y, square_size)

        # Draw possible move indicators
        self._draw_move_indicators(surface, board_x, board_y, square_size)

        # Draw border
        self._draw_board_border(surface, board_x, board_y, board_size)

    def _draw_squares_and_pieces(self, surface: Surface, board_x: int, board_y: int, square_size: int) -> None:
        """
        Draw all squares with appropriate colors and pieces.
        
        Renders the chess board grid and places pieces on their respective squares.
        
        Args:
            surface: pygame Surface to draw on.
            board_x: X coordinate of board origin.
            board_y: Y coordinate of board origin.
            square_size: Size of each square in pixels.
        """
        for square in chess.SQUARES:
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # a1 (file=0, rank=0) should be dark -> parity 0 -> dark.
            # So light squares are when (file + rank) % 2 == 1
            is_light = (file + rank) % 2 == 1
            color = self.light_square_color if is_light else self.dark_square_color

            rect = self._square_to_draw_rect(square, board_x, board_y, square_size)

            if square == self.selected_square:
                color = self.selected_square_color

            pygame.draw.rect(surface, color, rect)

            piece = self.board.piece_at(square)
            if piece:
                self._draw_piece(surface, piece, rect, square_size)

    def _draw_move_indicators(self, surface: Surface, board_x: int, board_y: int, square_size: int) -> None:
        """
        Draw possible move indicators for selected square.
        
        Renders visual indicators showing legal moves from the currently selected square.
        
        Args:
            surface: pygame Surface to draw on.
            board_x: X coordinate of board origin.
            board_y: Y coordinate of board origin.
            square_size: Size of each square in pixels.
        """
        if self.selected_square is not None:
            for move in self.possible_moves:
                if move.from_square != self.selected_square:
                    continue
                to_rect = self._square_to_draw_rect(move.to_square, board_x, board_y, square_size)
                radius = max(4, square_size // 6)
                indicator = Surface((square_size, square_size), pygame.SRCALPHA)
                pygame.draw.circle(indicator, self.possible_move_color, (square_size // 2, square_size // 2), radius)
                surface.blit(indicator, (to_rect.x, to_rect.y))

    def _draw_board_border(self, surface: Surface, board_x: int, board_y: int, board_size: int) -> None:
        """
        Draw the board border around the chess grid.
        
        Renders the outer border of the chess board with configured width and color.
        
        Args:
            surface: pygame Surface to draw on.
            board_x: X coordinate of board origin.
            board_y: Y coordinate of board origin.
            board_size: Total size of the board in pixels.
        """
        board_rect = Rect(board_x, board_y, board_size, board_size)
        pygame.draw.rect(surface, self.board_border_color, board_rect, self.border_width)

    def _get_board_geometry(self) -> Tuple[int, int, int, int]:
        """
        Return board geometry: (board_x, board_y, board_size, square_size).
        
        Centralises the geometry calculation so both drawing and input can reuse it.
        Ensures the board is centered within the widget rectangle.
        
        Returns:
            Tuple of (board_x, board_y, board_size, square_size) coordinates.
        """
        board_size = min(self.rect.width, self.rect.height)
        square_size = board_size // 8
        board_x = self.rect.x + (self.rect.width - board_size) // 2
        board_y = self.rect.y + (self.rect.height - board_size) // 2
        return board_x, board_y, board_size, square_size

    def _square_to_draw_rect(self, square: chess.Square, board_x: int, board_y: int, square_size: int) -> Rect:
        """
        Convert a chess.Square (0..63) to the Rect on the screen, taking flip_board into account.
        
        Maps chess square coordinates to screen pixel coordinates, handling board orientation.
        
        Args:
            square: chess.Square (0-63) to convert.
            board_x: X coordinate of board origin.
            board_y: Y coordinate of board origin.
            square_size: Size of each square in pixels.
            
        Returns:
            pygame.Rect representing the screen area for the square.
        """
        file = chess.square_file(square)   # 0..7 (a..h)
        rank = chess.square_rank(square)   # 0..7 (1..8)

        if self.flip_board:
            draw_file = 7 - file
            draw_rank = rank
        else:
            draw_file = file
            draw_rank = 7 - rank

        draw_x = board_x + draw_file * square_size
        draw_y = board_y + draw_rank * square_size
        return Rect(draw_x, draw_y, square_size, square_size)

    def _piece_key(self, piece: chess.Piece) -> str:
        """
        Generate key for ImageLoader (e.g. 'white_king').
        
        Maps chess piece type and color to corresponding image key string.
        
        Args:
            piece: chess.Piece instance to generate key for.
            
        Returns:
            String key for ImageLoader lookup.
        """
        piece_keys = {
            (chess.WHITE, chess.PAWN): 'white_pawn',
            (chess.WHITE, chess.KNIGHT): 'white_knight',
            (chess.WHITE, chess.BISHOP): 'white_bishop',
            (chess.WHITE, chess.ROOK): 'white_rook',
            (chess.WHITE, chess.QUEEN): 'white_queen',
            (chess.WHITE, chess.KING): 'white_king',
            (chess.BLACK, chess.PAWN): 'black_pawn',
            (chess.BLACK, chess.KNIGHT): 'black_knight',
            (chess.BLACK, chess.BISHOP): 'black_bishop',
            (chess.BLACK, chess.ROOK): 'black_rook',
            (chess.BLACK, chess.QUEEN): 'black_queen',
            (chess.BLACK, chess.KING): 'black_king',
        }
        
        return piece_keys.get((piece.color, piece.piece_type))

    def _draw_piece(
        self, 
        surface: Surface, 
        piece: chess.Piece, 
        square_rect: Rect, 
        square_size: int
    ) -> None:
        """
        Draw piece image centered in square_rect, robust to missing images.
        
        Scales piece image to fit within square with padding and centers it.
        Handles image loading and scaling errors gracefully.
        
        Args:
            surface: pygame Surface to draw on.
            piece: chess.Piece to draw.
            square_rect: Rectangle defining square boundaries.
            square_size: Size of the square in pixels.
        """
        key = self._piece_key(piece)
        base_img = image_loader.get_image(key)

        # Scale image to fit square with a little padding
        padding = max(2, square_size // 12)
        target_size = max(1, square_size - 2 * padding)
        try:
            if target_size > 0:
                scaled_img = pygame.transform.smoothscale(base_img, (target_size, target_size))
            else:
                scaled_img = base_img
        except Exception:
            try:
                scaled_img = pygame.transform.scale(base_img, (target_size, target_size))
            except Exception:
                return

        img_x = square_rect.x + (square_size - target_size) // 2
        img_y = square_rect.y + (square_size - target_size) // 2

        try:
            surface.blit(scaled_img, (img_x, img_y))
        except Exception:
            pass

    def _pos_to_square(self, pos: Tuple[int, int]) -> Optional[chess.Square]:
        """
        Convert a screen position (x,y) to a chess.Square (0..63).
        
        Maps screen coordinates to chess board coordinates, handling board orientation
        and boundary checking.
        
        Args:
            pos: Screen position tuple (x, y).
            
        Returns:
            chess.Square (0-63) if position is valid, None otherwise.
        """
        board_x, board_y, board_size, square_size = self._get_board_geometry()

        # outside board?
        if not (board_x <= pos[0] < board_x + board_size and board_y <= pos[1] < board_y + board_size):
            return None

        rel_x = pos[0] - board_x
        rel_y = pos[1] - board_y
        col = int(rel_x // square_size)   # screen column from left 0..7
        row = int(rel_y // square_size)   # screen row from top 0..7

        # Convert screen col,row to chess file,rank considering flip_board
        if self.flip_board:
            file = 7 - col
            rank = row
        else:
            file = col
            rank = 7 - row

        file = max(0, min(7, file))
        rank = max(0, min(7, rank))
        return chess.square(file, rank)

    def handle_board_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse click on board; map screen position to chess square and delegate selection/move logic.
        
        Main entry point for mouse interaction with the chess board.
        
        Args:
            pos: Screen position tuple (x, y) of mouse click.
        """
        square = self._pos_to_square(pos)
        if square is None:
            return
        self._handle_square_selection(square)

    def _handle_square_selection(self, square: chess.Square) -> None:
        """
        Handle selection logic: select piece, show legal moves, make move if destination clicked.
        
        Implements chess selection rules:
        - Select own piece to show legal moves
        - Click destination to make move
        - Click another own piece to reselect
        - Click same piece again to deselect
        - Automatic queen promotion for convenience
        
        Args:
            square: chess.Square that was selected.
        """
        piece = self.board.piece_at(square)

        # Helper function to select a piece and show legal moves
        def _select_piece():
            self.selected_square = square
            self.possible_moves = [move for move in self.board.legal_moves if move.from_square == square]

        # Helper function to attempt making a move
        def _attempt_move(promotion=None):
            move = chess.Move(self.selected_square, square, promotion=promotion)
            if move in self.board.legal_moves:
                self._make_move(move)
                return True
            return False

        # If clicking on own piece
        if piece and piece.color == self.board.turn:
            # If same piece clicked again, deselect it
            if self.selected_square == square:
                self._deselect()
            else:
                # Select new piece (or reselect different piece)
                _select_piece()
            return

        # If a square is already selected, try to make a move
        if self.selected_square is not None:
            # Try regular move
            if _attempt_move():
                return

            # Try promotion to queen
            if _attempt_move(promotion=chess.QUEEN):
                return

        # Otherwise deselect
        self._deselect()

    def _make_move(self, move: chess.Move) -> None:
        """
        Push a legal move onto the board and call callback.
        
        Updates game state with the move and notifies listeners.
        
        Args:
            move: Legal chess.Move to execute.
        """
        self.board.push(move)
        self._deselect()
        if self.on_move_made:
            self.on_move_made(move)

    def _deselect(self) -> None:
        """
        Clear selection and possible moves.
        
        Resets the selection state after move completion or cancellation.
        """
        self.selected_square = None
        self.possible_moves = []