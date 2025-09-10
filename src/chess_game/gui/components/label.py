# src/chess_game/gui/components/label.py
from typing import Union
from pygame_gui import UIManager
from pygame_gui.elements import UILabel
from pygame_gui.core import UIContainer
from .base import BaseComponent, RectType

class Label(BaseComponent):
    """
    Label component for displaying information.
    
    Wraps pygame_gui's UILabel for static text display.
    Text can be updated dynamically using set_text().

    Attributes:
        text: Initial text to display.
    """

    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        text: str
    ):
        self.text = text
        super().__init__(rect, manager, container)
        
    def create_element(self) -> None:
        """
        Create the pygame_gui label element.
        """
        self.element = UILabel(
            relative_rect=self.rect,
            text=self.text,
            manager=self.manager,
            container=self.container
        )

    def _register_events(self) -> None:
        """
        Label class does not handle mouse signals but simply displays information.
        """
        pass

    def set_text(self, text: Union[str, int, float]) -> None:
        """
        Update the label text.
        
        Args:
            text: New text to display

        Example:
            This method is used to refresh labels that change frequently,
            such as a player timer.
        """
        new_text = str(text)
        if new_text == self.text:
            return  # skip if nothing changed
        
        self.text = new_text
        self.element.set_text(new_text)  # element.set_text is dynamically added by pygame_gui and not visible to type checkers