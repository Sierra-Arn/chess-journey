# src/chess_game/ai/ai_manager.py
import concurrent.futures
import pygame
import chess
from .stockfish_engine import SimpleStockfishEngine

AI_MOVE_EVENT = pygame.USEREVENT + 1 # Custom pygame event type for AI move notifications

class AIManager:
    """
    Manager for handling AI (Stockfish) operations in a separate thread.
    
    Orchestrates asynchronous chess engine operations by running move calculations
    in background threads to prevent UI blocking. Manages engine lifecycle,
    task scheduling, and inter-thread communication via pygame events.
    Provides thread-safe operation cancellation and graceful shutdown.
    
    Attributes:
        skill_level: Engine strength level (0-20) passed to Stockfish engine.
        is_thinking: Boolean property indicating if AI is currently calculating.
    """

    def __init__(self, skill_level: int):
        """
        Initialize AI manager with specified engine strength.
        
        Creates Stockfish engine instance and thread pool executor for
        asynchronous move calculation. Engine runs in separate process
        while calculations execute in thread pool.
        
        Args:
            skill_level: Engine strength from 0 (weakest) to 20 (strongest).
        """
        self.skill_level = skill_level
        self.engine = SimpleStockfishEngine(skill_level=skill_level)
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._future = None
        self._shutdown = False

    @property
    def is_thinking(self) -> bool:
        """
        Check if AI is currently calculating a move.
        
        Thread-safe property that returns True when there is an active
        move calculation task that hasn't completed yet.
        
        Returns:
            True if AI is actively thinking, False otherwise.
        """
        return self._future is not None and not self._future.done()

    def schedule(self, board: chess.Board) -> None:
        """
        Schedule AI move calculation for given board position.
        
        Submits move calculation task to thread pool executor. When complete,
        posts AI_MOVE_EVENT to pygame event queue with move UCI string.
        Prevents scheduling new tasks when already thinking or shutting down.
        
        Args:
            board: Current chess.Board position for AI analysis.
        """
        if self._shutdown or self.is_thinking:
            return

        def _worker(fen_str: str):
            """
            Worker function executed in thread pool.
            
            Creates board from FEN string and queries engine for best move.
            Returns move in UCI format for cross-thread communication.
            
            Args:
                fen_str: FEN representation of board position.
                
            Returns:
                UCI string representation of best move.
            """
            position = chess.Board(fen_str)
            return self.engine.get_best_move(position).uci()

        def _on_done(fut: concurrent.futures.Future):
            """
            Callback executed when move calculation completes.
            
            Posts pygame event with move result or handles shutdown conditions.
            Silently ignores errors during shutdown or pygame cleanup.
            
            Args:
                fut: Completed future containing move calculation result.
            """
            if self._shutdown:
                return
            
            # Prevents issues during game shutdown - ensures clean termination 
            # and prevents engine from attempting to send moves 
            # after pygame has already closed
            try:
                move_uci = fut.result()
                pygame.event.post(pygame.event.Event(AI_MOVE_EVENT, {"move_uci": move_uci}))
            except pygame.error:
                # pygame already shut down, ignore
                pass
            except Exception:
                # other errors, ignore silently
                pass

        self._future = self._executor.submit(_worker, board.fen())
        self._future.add_done_callback(_on_done)

    def cancel(self) -> None:
        """
        Cancel ongoing AI move calculation if active.
        
        Attempts to cancel current move calculation task. Safe to call
        even when no task is running - will have no effect in that case.
        """
        if self._future and not self._future.done():
            self._future.cancel()

    def shutdown(self) -> None:
        """
        Gracefully shutdown AI manager and cleanup resources.
        
        Sets shutdown flag, terminates thread pool executor, and closes
        Stockfish engine connection. Clears all internal references
        to prevent resource leaks during application exit.
        """
        self._shutdown = True
        self._executor.shutdown(wait=False)
        self.engine.close()
        self.engine = None
        self._executor = None
        self._future = None