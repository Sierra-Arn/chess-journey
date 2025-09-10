# src/chess_game/gui/components/button.py
from typing import Callable
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from pygame_gui.core import UIContainer
from .base import BaseComponent, RectType
from ..event_manager import event_manager

class Button(BaseComponent):
    """
    Button component for UI interactions.
    
    Wraps pygame_gui's UIButton with automatic event registration
    and callback handling. 
    The button calls the provided callback function when clicked.

    Attributes:
        text: Button label text.
        on_click: Callback function called when button is clicked.
    """
    
    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        text: str,
        on_click: Callable[[], None] = lambda: None
    ):
        self.text = text
        self.on_click = on_click
        super().__init__(rect, manager, container)
        
    def create_element(self) -> None:
        """
        Create the pygame_gui button element.
        """
        self.element = UIButton(
            relative_rect=self.rect,
            text=self.text,
            manager=self.manager,
            container=self.container
        )

    def _register_events(self) -> None:
        """
        Register button click event with event manager.
        """
        event_manager.register_callback(
            ui_element=self.element, 
            event_type=pygame_gui.UI_BUTTON_PRESSED, 
            callback=self._handle_button_pressed
        )
            
    def _handle_button_pressed(self, event) -> None:
        """
        Handle button press events by calling the callback.
        
        Note: event parameter is required by CallbackType signature
        even though it's not used in this handler.
        """
        self.on_click()