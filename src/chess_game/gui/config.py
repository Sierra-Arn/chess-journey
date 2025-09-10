# src/chess_game/gui/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Tuple, Annotated, TypeAlias

# Constrain an integer to be a valid color component (0-255)
ColorComp = Annotated[int, Field(ge=0, le=255)]
ColorRGBA: TypeAlias = Tuple[ColorComp, ColorComp, ColorComp, ColorComp] 

class GUIConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="GUI_",
    )

    # --- Chess Board ---
    square_light_color: ColorRGBA = Field(..., description="Color of the light squares on the chessboard (RGBA)")
    square_dark_color: ColorRGBA = Field(..., description="Color of the dark squares on the chessboard (RGBA)")
    square_selected_color: ColorRGBA = Field(..., description="Color of the selected square highlight (RGBA)")
    square_possible_move_color: ColorRGBA = Field(..., description="Color for possible move indicators (RGBA)")

    board_border_color: ColorRGBA = Field(..., description="Border color around chess board")
    board_border_width: int = Field(..., description="Width of chess board border in pixels")

gui_config = GUIConfig()