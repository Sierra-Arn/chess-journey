# src/chess_game/custom_types.py
from enum import Enum

class PlayerType(Enum):
    HUMAN = "Human"
    AI = "AI"

class ModeType(Enum):
    STANDARD = "Standard"
    CHESS960 = "Chess960"

class OrientationType(Enum):
    WHITE = "White"
    BLACK = "Black"