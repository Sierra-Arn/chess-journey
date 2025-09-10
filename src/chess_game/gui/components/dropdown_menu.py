# src/chess_game/gui/components/dropdown_menu.py
from typing import Callable, List
from pygame_gui import UIManager
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.core import UIContainer
import pygame_gui
from .base import BaseComponent, RectType
from ..event_manager import event_manager

class DropdownMenu(BaseComponent):
    """
    Dropdown menu component for selecting options.
    
    Wraps pygame_gui's UIDropDownMenu with automatic event registration
    and callback handling. 
    Calls the provided callback function when a selection is made.

    Attributes:
        options_list: List of available options.
        starting_option: Initial selected option (first from options_list).
        current_value: Currently selected option.
        on_selection_changed: Callback function called when selection changes.
    """
    
    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        options_list: List[str],
        on_selection_changed: Callable[[str], None] = lambda x: None
    ):
        self.options_list = options_list
        self.starting_option = options_list[0]
        self.current_value = self.starting_option
        self.on_selection_changed = on_selection_changed
        super().__init__(rect, manager, container)
        
    def create_element(self) -> None:
        """
        Create the pygame_gui dropdown element.
        """
        self.element = UIDropDownMenu(
            options_list=self.options_list,
            starting_option=self.starting_option,
            relative_rect=self.rect,
            manager=self.manager,
            container=self.container
        )
        
    def _register_events(self) -> None:
        """
        Register dropdown change event with event manager.
        """
        event_manager.register_callback(
            ui_element=self.element, 
            event_type=pygame_gui.UI_DROP_DOWN_MENU_CHANGED, 
            callback=self._handle_dropdown_changed
        )

    def _handle_dropdown_changed(self, event) -> None:
        """
        Handle dropdown change events by calling the callback.
        """
        self.current_value = event.text # event.text is dynamically added by pygame_gui and not visible to type checkers
        self.on_selection_changed(self.current_value)