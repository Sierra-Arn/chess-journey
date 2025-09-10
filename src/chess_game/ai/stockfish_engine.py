# src/chess_game/stockfish_engine.py
from typing import Optional
import chess.engine
from ..assets import asset_config

class SimpleStockfishEngine:
    """
    Wrapper class for Stockfish chess engine.
    
    Provides a simplified interface for interacting with the Stockfish UCI engine,
    handling initialization, skill level configuration, and move calculations.
    Manages engine lifecycle and provides move analysis for AI opponents.
    
    Attributes:
        skill_level: Engine strength from 0 (weakest) to 20 (strongest).
    """
    
    def __init__(
        self,
        skill_level: int
    ):
        self.engine = chess.engine.SimpleEngine.popen_uci(asset_config.stockfish_path)

        # Configure engine skill level - this setting exists in Stockfish internally
        # Can be verified by running: ./stockfish, then 'uci' command
        self.engine.configure({"Skill Level": skill_level})

    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Get best move from the engine.
        
        Requests the engine to analyze the current position and return its
        recommend.
        
        Args:
            board: Current chess.Board position to analyze.
            
        Returns:
            Best move found by engine, or None if no legal moves available.
        """
        result = self.engine.play(board=board, limit=chess.engine.Limit(time=1))
        return result.move
    
    def close(self) -> None:
        """
        Close engine connection and cleanup resources.
        """
        self.engine.quit()