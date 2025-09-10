# src/chess_game/assets/image_loader.py
from pathlib import Path
from typing import Dict
import pygame
from pygame import Surface
from .config import asset_config

class ImageLoader:
    """Class for loading and managing chess piece images."""
    
    def __init__(self):
        """
        Initialize image loader with configuration.
        """
        self.images_path = Path(asset_config.images_path)
        self.piece_size = asset_config.piece_size
        self.images: Dict[str, Surface] = {}
    
    def load_all_images(self) -> bool:
        """
        Load all chess piece images from configuration.
        
        Returns:
            True if all images loaded successfully
            
        Raises:
            FileNotFoundError: If any required image file is missing
            pygame.error: If image loading fails
        """
        missing_files = []
        
        for piece_name, filename in asset_config.piece_files.items():
            image_path = self.images_path / filename
            
            if not image_path.exists():
                missing_files.append(str(image_path))
                continue
                
            try:
                image = pygame.image.load(str(image_path))
                self.images[piece_name] = image
            except pygame.error as e:
                raise pygame.error(f"Failed to load image {image_path}: {e}")
        
        if missing_files:
            raise FileNotFoundError(f"Required chess piece images not found: {missing_files}")

        return True
    
    def get_image(self, piece_name: str) -> Surface:
        """
        Get piece image by name.
        
        Args:
            piece_name: Piece name (e.g., 'white_pawn', 'black_king')
            
        Returns:
            Piece image surface
            
        Raises:
            KeyError: If image was not loaded or not found
        """
        if piece_name not in self.images:
            raise KeyError(
                f"Chess piece image not loaded: {piece_name}. "
                f"Available images: {list(self.images.keys())}"
            )
        return self.images[piece_name]
    
image_loader = ImageLoader()