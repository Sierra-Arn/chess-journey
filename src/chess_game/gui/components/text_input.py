# src/chess_game/gui/components/text_input.py
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine
from pygame_gui.core import UIContainer
from .base import BaseComponent, RectType
from ..event_manager import event_manager

class TextInput(BaseComponent):
    """
    Single-line text input component for user text entry.
    
    Wraps pygame_gui's UITextEntryLine with automatic event registration
    and callback handling. 

    Attributes:
        initial_text: Initial text value.
        placeholder_text: Gray placeholder text shown when empty.
        current_text: Currently entered text.

    Note:
        initial_text - this is the actual content of the field at creation time.
        It is set as the element's text and will be returned by get_text().
        When the field is focused or text is entered, this text remains as normal editable content.
        
        placeholder_text - this is a hint/placeholder that is only drawn when the field is empty
        and not in focus. This is not the "real" content of the field: as soon as the user clicks
        in the field (the field gains focus) or you write real text to it, the placeholder disappears.
        Placeholders are usually styled differently (to make it clear that this is a hint) 
        rather than as user input.
    """
    
    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        initial_text: str,
        placeholder_text: str,
    ):
        self.initial_text = initial_text
        self.placeholder_text = placeholder_text
        self.current_text = initial_text
        super().__init__(rect, manager, container)
        
    def create_element(self) -> None:
        """
        Create the pygame_gui text input element.
        """
        self.element = UITextEntryLine(
            relative_rect=self.rect,
            manager=self.manager,
            container=self.container,
            initial_text=self.initial_text,
            placeholder_text=self.placeholder_text
        )
        
    def _register_events(self) -> None:
        """
        Register text input events with event manager.
        """
        event_manager.register_callback(
            ui_element=self.element, 
            event_type=pygame_gui.UI_TEXT_ENTRY_CHANGED, 
            callback=self._handle_text_changed
        )
        event_manager.register_callback(
            ui_element=self.element, 
            event_type=pygame_gui.UI_TEXT_ENTRY_FINISHED, 
            callback=self._handle_text_finished
        )

    def _handle_text_changed(self, event) -> None:
        """
        Handle text change events by calling the callback.
        """
        self.current_text = event.text # event.text is dynamically added by pygame_gui and not visible to type checkers
            
    def _handle_text_finished(self, event) -> None:
        """
        Handle text finish events by calling the callback.
        """
        self.current_text = event.text # event.text is dynamically added by pygame_gui and not visible to type checkers