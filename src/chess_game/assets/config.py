# src/chess_game/assets/config.py
from typing import Tuple, Dict, Annotated, TypeAlias
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

PieceSizeInt = Annotated[int, Field(ge=0)]
PieceSizeTuple: TypeAlias = Tuple[PieceSizeInt, PieceSizeInt]

class AssetConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="ASSETS_"
    )

    images_path: str = Field(..., description="Absolute path relative to project root to images directory")
    stockfish_path: str = Field(..., description="Absolute path relative to project root to Stockfish executable")

    piece_size: PieceSizeTuple = Field(..., description="Size of chess pieces in pixels as [width, height]")

    white_pawn: str = Field(..., description="Filename for white pawn image")
    white_rook: str = Field(..., description="Filename for white rook image")
    white_knight: str = Field(..., description="Filename for white knight image")
    white_bishop: str = Field(..., description="Filename for white bishop image")
    white_queen: str = Field(..., description="Filename for white queen image")
    white_king: str = Field(..., description="Filename for white king image")

    black_pawn: str = Field(..., description="Filename for black pawn image")
    black_rook: str = Field(..., description="Filename for black rook image")
    black_knight: str = Field(..., description="Filename for black knight image")
    black_bishop: str = Field(..., description="Filename for black bishop image")
    black_queen: str = Field(..., description="Filename for black queen image")
    black_king: str = Field(..., description="Filename for black king image")

    @property
    def piece_files(self) -> Dict[str, str]:
        """
        Dictionary mapping piece names to filenames.
        """
        return {
            'white_pawn': self.white_pawn,
            'white_rook': self.white_rook,
            'white_knight': self.white_knight,
            'white_bishop': self.white_bishop,
            'white_queen': self.white_queen,
            'white_king': self.white_king,
            'black_pawn': self.black_pawn,
            'black_rook': self.black_rook,
            'black_knight': self.black_knight,
            'black_bishop': self.black_bishop,
            'black_queen': self.black_queen,
            'black_king': self.black_king
        }

asset_config = AssetConfig()