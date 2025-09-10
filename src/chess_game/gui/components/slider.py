# src/chess_game/gui/components/slider.py
from typing import Tuple
from pygame_gui import UIManager
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.core import UIContainer
import pygame_gui
from .base import BaseComponent, RectType
from ..event_manager import event_manager

class Slider(BaseComponent):
    """
    Horizontal slider component for selecting numeric values.
    
    Wraps pygame_gui's UIHorizontalSlider with automatic event registration
    and callback handling.

    Attributes:
        start_value: Initial slider value.
        value_range: Tuple of (min, max) values (inclusive).
        current_value: Currently selected value.
    """
    
    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        start_value: int,
        value_range: Tuple[int, int]
    ):
        self.start_value = start_value
        self.value_range = value_range
        self.current_value = start_value
        super().__init__(rect, manager, container)
        
    def create_element(self) -> None:
        """
        Create the pygame_gui slider element.
        """
        self.element = UIHorizontalSlider(
            relative_rect=self.rect,
            start_value=self.start_value,
            value_range=self.value_range,
            manager=self.manager,
            container=self.container
        )
        
    def _register_events(self) -> None:
        """
        Register slider move event with event manager.
        """
        event_manager.register_callback(
            ui_element=self.element, 
            event_type=pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, 
            callback=self._handle_slider_moved
        )

    def _handle_slider_moved(self, event) -> None:
        """
        Handle slider move events by calling the callback.
        """
        self.current_value = event.value # element.value is dynamically added by pygame_gui and not visible to type checkers