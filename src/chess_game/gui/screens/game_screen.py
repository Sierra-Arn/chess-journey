# src/chess_game/gui/screens/game_screen.py
from typing import List, Optional, Dict, Any
from pygame import Surface, Rect, Event
import pygame
from pygame_gui import UIManager
import chess
from ..components import BaseComponent, Label
from ..widgets import ChessBoardWidget, PlayerTimerWidget
from ...ai import AIManager, AI_MOVE_EVENT
from ...custom_types import PlayerType, ModeType, OrientationType
from .base import BaseScreen

class GameScreen(BaseScreen):
    """
    Main game screen with chess board, timers and controls.
    Supports separate AIManager for each side (WHITE / BLACK).
    
    Manages complete game flow including player input handling, AI move
    processing, timer management, and game state tracking. Coordinates
    between UI widgets and game logic components. Handles both human
    and AI players with proper turn scheduling and event processing.
    
    Attributes:
        game_config: Configuration dictionary containing game settings.
        board: Main chess.Board instance tracking game state.
        game_active: Boolean indicating if game is currently in progress.
        widgets: List of all active UI components for cleanup.
        chess_board: Chess board widget for visual representation.
        white_timer: Timer widget for white player.
        black_timer: Timer widget for black player.
        end_game_label: Label displaying game result when finished.
        ai_managers: Dictionary mapping player colors to AI managers.
    """

    def __init__(
        self,
        rect: Rect,
        manager: UIManager,
        game_config: Dict[str, Any]
    ):
        """
        Initialize game screen with configuration and UI manager.
        
        Sets up complete game environment including board, timers, and
        AI managers based on provided configuration. Automatically
        starts game timers and schedules initial AI move if applicable.
        
        Args:
            rect: Rectangle defining screen position and dimensions.
            manager: Pygame GUI manager for widget creation.
            game_config: Dictionary containing player types, times, etc.
        """
        self.game_config = game_config

        # Game state
        self.board = chess.Board()
        self.game_active = False

        # UI Elements
        self.widgets: List[BaseComponent] = []
        self.chess_board: Optional[ChessBoardWidget] = None
        self.white_timer: Optional[PlayerTimerWidget] = None
        self.black_timer: Optional[PlayerTimerWidget] = None
        self.end_game_label: Optional[Label] = None

        # AI managers per side
        self.ai_managers: Dict[int, AIManager] = {}

        # Initialize base screen (calls _create_ui)
        super().__init__(rect, manager)

        # Initialize game after UI creation
        self._start_timers()
        self._setup_ai_managers()
        self._sync_board_state()
        self._schedule_initial_ai_move()

    def _create_ui(self) -> None:
        """
        Create all UI elements (board, timers).
        
        Creates chess board widget with proper positioning and configuration
        based on game mode (standard/Chess960) and board orientation.
        Sets up player timer widgets with names and initial times.
        Calculates layout dimensions to center game elements properly.
        """
        padding = 20
        board_size = 512
        timer_height = 60

        total_width = board_size
        total_height = timer_height + padding + board_size

        game_area_x = (self.container.rect.width - total_width) // 2
        game_area_y = (self.container.rect.height - total_height) // 2

        board_x = game_area_x
        board_y = game_area_y + timer_height + padding

        chess960 = self.game_config.get('game_mode') == ModeType.CHESS960.value
        flip_board = self.game_config.get('board_orientation') == OrientationType.BLACK.value
        white_name = self.game_config.get('players').get('white').get('name')
        black_name = self.game_config.get('players').get('black').get('name')
        white_time = self.game_config.get('players').get('white').get('time')
        black_time = self.game_config.get('players').get('black').get('time')

        board_rect = (board_x, board_y, board_size, board_size)
        self.chess_board = ChessBoardWidget(
            rect=board_rect,
            on_move_made=self._on_move_made,
            flip_board=flip_board,
            chess960=chess960
            # Container not needed because ChessBoardWidget is drawn directly via pygame
            # rather than using pygame_gui system, so it manages its own rendering
        )
        self.widgets.append(self.chess_board)

        white_timer_rect = (board_x, game_area_y, board_size // 2, timer_height)
        black_timer_rect = (board_x + board_size // 2, game_area_y, board_size // 2, timer_height)

        self.white_timer = PlayerTimerWidget(
            rect=white_timer_rect,
            manager=self.manager,
            container=self.container,
            player_name=white_name,
            initial_time=white_time
        )
        self.widgets.append(self.white_timer)

        self.black_timer = PlayerTimerWidget(
            rect=black_timer_rect,
            manager=self.manager,
            container=self.container,
            player_name=black_name,
            initial_time=black_time
        )
        self.widgets.append(self.black_timer)

    def _setup_ai_managers(self) -> None:
        """
        Create AI managers for AI players based on game configuration.
        
        Initializes Stockfish engine instances for each AI player with
        configured difficulty levels. Only creates managers for players
        marked as AI type in game configuration.
        """
        white_cfg = self.game_config.get('players').get('white')
        black_cfg = self.game_config.get('players').get('black')

        if white_cfg.get("type") == PlayerType.AI.value:
            white_skill = white_cfg.get("difficulty")
            self.ai_managers[chess.WHITE] = AIManager(skill_level=white_skill)

        if black_cfg.get("type") == PlayerType.AI.value:
            black_skill = black_cfg.get("difficulty")
            self.ai_managers[chess.BLACK] = AIManager(skill_level=black_skill)

    def _sync_board_state(self) -> None:
        """
        Sync GameScreen.board with widget's board (important for Chess960).
        
        Ensures internal board state matches visual board widget state,
        particularly important for Chess960 random starting positions.
        Handles potential synchronization errors gracefully.
        """
        if self.chess_board:
            try:
                self.board = chess.Board(self.chess_board.board.fen())
            except Exception:
                self.board = chess.Board()

    def _schedule_initial_ai_move(self) -> None:
        """
        Schedule initial AI move if first player is AI.
        
        Checks if game is active and current player has an AI manager,
        then schedules move calculation. Prevents duplicate scheduling
        by checking game_active flag and existing AI tasks.
        """
        if self.game_active and self.board.turn in self.ai_managers:
            self.ai_managers[self.board.turn].schedule(self.board)

    def handle_event(self, event: Event) -> bool:
        """
        Handle pygame events, including AI_MOVE_EVENT and player input.
        
        Processes both custom AI move events and user interface events.
        Returns True if event was handled, False otherwise for event
        propagation to other handlers.
        
        Args:
            event: Pygame event to process.
            
        Returns:
            True if event was consumed, False otherwise.
        """
        if event.type == AI_MOVE_EVENT:
            return self._handle_ai_move_event(event)

        if (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.chess_board and
                self.game_active):
            return self._handle_mouse_click(event)

        return False

    def _handle_ai_move_event(self, event: Event) -> bool:
        """
        Process AI move event and apply the move to the game.
        
        Validates received move against legal moves and applies it
        to either board widget or internal board state. Triggers
        post-move processing including timer switching and game end
        condition checking. Schedules next AI move if applicable.
        
        Args:
            event: AI_MOVE_EVENT containing move UCI string.
            
        Returns:
            True if move was successfully processed, False otherwise.
        """
        move_uci = getattr(event, "move_uci", None)
        if not move_uci:
            return False

        move = chess.Move.from_uci(move_uci)
        if move not in self.board.legal_moves:
            return False

        if self.chess_board:
            self.chess_board._make_move(move)
        else:
            self.board.push(move)
            self._switch_active_timer()
            self._check_game_end()

        return True

    def _handle_mouse_click(self, event: Event) -> bool:
        """
        Handle player mouse input, blocking if AI is thinking.
        
        Processes player clicks on chess board while preventing
        input during AI calculation to avoid race conditions.
        Only processes clicks within board boundaries.
        
        Args:
            event: MOUSEBUTTONDOWN event with click position.
            
        Returns:
            True if click was processed, False otherwise.
        """
        current_side = self.board.turn
        manager = self.ai_managers.get(current_side)
        if manager and manager.is_thinking:
            return False

        if self.chess_board.rect.collidepoint(event.pos):
            self.chess_board.handle_board_click(event.pos)
            return True
            
        return False

    def update(self, time_delta: float) -> None:
        """
        Update screen state (timers etc).
        
        Called each frame to update time-sensitive UI elements.
        Updates active player timers and processes time-based
        game end conditions like timeout detection.
        
        Args:
            time_delta: Time elapsed since last update in seconds.
        """
        if self.game_active:
            if self.white_timer:
                self.white_timer.draw()
            if self.black_timer:
                self.black_timer.draw()

    def draw(self, surface: Surface) -> None:
        """
        Draw custom elements and optional AI thinking indicators.
        
        Renders all custom-drawn UI components to the provided surface.
        Excludes timer widgets which are managed by pygame_gui system.
        
        Args:
            surface: Pygame surface to draw elements on.
        """
        for widget in self.widgets:
            if hasattr(widget, 'draw') and widget not in [self.white_timer, self.black_timer]:
                widget.draw(surface)

        if hasattr(self, 'end_game_label_bg') and self.end_game_label_bg:
            bg_rect = Rect(self.end_game_label_bg['rect'])
            bg_surface = Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill(self.end_game_label_bg['color'])
            surface.blit(bg_surface, (bg_rect.x, bg_rect.y))

    def _on_move_made(self, move: chess.Move) -> None:
        """
        Called when any move is made via widget or other source.
        
        Central callback for move processing that updates game state,
        switches active timers, checks for game end conditions, and
        schedules next AI move if required. Maintains game flow logic.
        
        Args:
            move: Chess move that was just executed.
        """
        self.board.push(move)
        self._switch_active_timer()
        self._check_game_end()

        if self.game_active and self.board.turn in self.ai_managers:
            self.ai_managers[self.board.turn].schedule(self.board)

    def _start_timers(self) -> None:
        """
        Initialize and start player timers.
        
        Resets both player timers to their initial values and activates
        white player's timer to begin the game. Sets game_active flag
        to enable timer updates and game processing.
        """
        if self.white_timer and self.black_timer:
            self.white_timer.reset()
            self.black_timer.reset()
            self.white_timer.set_active(True)
            self.black_timer.set_active(False)

        self.game_active = True

    def _switch_active_timer(self) -> None:
        """
        Switch active timer between players.
        
        Toggles timer activation state to reflect current player turn.
        Ensures only one timer is active at a time for accurate timing.
        """
        if not (self.white_timer and self.black_timer):
            return

        is_white_active = self.white_timer.is_active
        self.white_timer.set_active(not is_white_active)
        self.black_timer.set_active(is_white_active)

    def _check_game_end(self) -> None:
        """
        Check various game end conditions and display result.
        
        Evaluates standard chess end conditions including checkmate,
        stalemate, insufficient material, and timeout scenarios.
        Displays appropriate end game message when conditions met.
        """
        if not self.game_active:
            return

        end_text = self._get_game_end_text()
        if end_text:
            self.game_active = False
            self._show_game_end_message(end_text)

    def _get_game_end_text(self) -> Optional[str]:
        """
        Determine game end condition and return appropriate message.
        
        Checks all possible game termination conditions in order of
        precedence and returns descriptive message for display.
        Includes both standard chess rules and timer-based endings.
        
        Returns:
            End game message string or None if game continues.
        """
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.WHITE else "Black"
            return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate! Game is a draw."
        elif self.board.is_insufficient_material():
            return "Draw due to insufficient material!"
        elif self.board.is_seventyfive_moves():
            return "Draw due to 75-move rule!"
        elif self.board.is_fivefold_repetition():
            return "Draw due to fivefold repetition!"

        # Check timers
        if (self.white_timer and self.white_timer.is_active and self.white_timer.remaining_time <= 0):
            return "White's time is up! Black wins!"
        elif (self.black_timer and self.black_timer.is_active and self.black_timer.remaining_time <= 0):
            return "Black's time is up! White wins!"
            
        return None

    def _show_game_end_message(self, text: str) -> None:
        """
        Display game end message on the board.
        
        Creates centered label overlay on chess board displaying
        the game result. Positioned to be clearly visible without
        obstructing board view unnecessarily.
        
        Args:
            text: Game result message to display.
        """
        if self.chess_board:
            board_rect = self.chess_board.rect
            label_width = int(board_rect.width // 1.5)
            label_height = 60
            label_x = board_rect.x + (board_rect.width - label_width) // 2
            label_y = board_rect.y + (board_rect.height - label_height) // 2

            self.end_game_label = Label(
                rect=(label_x, label_y, label_width, label_height),
                manager=self.manager,
                container=self.container,
                text=text
            )
            self.widgets.append(self.end_game_label)

            self.end_game_label_bg = {
                    'rect': (label_x, label_y, label_width, label_height),
                    'color': (0, 0, 0, 200)
                }

    def kill(self) -> None:
        """
        Cleanly destroy all widgets and AI managers.
        
        Performs proper cleanup sequence by first shutting down all
        AI engines to prevent background processes from attempting
        UI updates after destruction. Then destroys all UI widgets
        and clears internal references to prevent memory leaks.
        """
        # shutdown all AI managers first
        for mgr in self.ai_managers.values():
            if mgr:
                mgr.shutdown()
        self.ai_managers.clear()
        
        # then kill widgets
        if self.end_game_label:
            self.end_game_label.kill()

        for widget in self.widgets:
            widget.kill()
        self.widgets.clear()
        
        # Call parent kill to cleanup container and components
        super().kill()