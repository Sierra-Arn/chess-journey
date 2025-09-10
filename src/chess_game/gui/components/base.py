# src/chess_game/gui/components/base.py
from abc import ABC, abstractmethod
from typing import Tuple, TypeAlias, Optional
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIContainer, UIElement
from ..event_manager import event_manager

RectType: TypeAlias = Tuple[int, int, int, int]  # Direct pixel coordinates (x, y, width, height)

class BaseComponent(ABC):
    """
    Base class for UI components in the chess game interface.
    
    This abstract class provides a foundation for all GUI components,
    handling common functionality.
    
    Note: The show and hide methods, as well as the visible field
    (as well as the enabled field which is required only for visability),
    are not implemented in this abstract class because components 
    either exist and are displayed on the screen, or they don't exist at all.

    Attributes:
        rect: Component position and dimensions (x, y, width, height).
        manager: pygame_gui UIManager instance for this component.
        container: pygame_gui UIContainer instance for this component.
        element: The actual pygame_gui UIElement (will be created by create_element()).
    """
    
    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer
    ):
        self.rect = Rect(rect)
        self.manager = manager
        self.container = container
        self.element: Optional[UIElement] = None 
        self.create_element()
        self._register_events()
            
    @abstractmethod
    def create_element(self) -> None:
        """
        Creates the pygame_gui element for this component.
        
        Must be implemented by subclasses to instantiate their specific UI element.
        The created element should be stored in self.element.
        """
        pass

    @abstractmethod
    def _register_events(self) -> None:
        """
        Register event callbacks with the event manager.
        
        Override in subclasses to register specific events for this component.
        Called automatically after element creation.
        """
        pass

    def _unregister_events(self) -> None:
        """
        Unregister event callbacks with the event manager.
        
        Called automatically during the element's kill process.
        """
        event_manager.unregister_all_callbacks(self.element)

    def kill(self) -> None:
        """
        Cleanly destroy the UI element and unregister events.
        Subclasses that have extra children should override and call super().
        """
        try:
            self._unregister_events()
        except Exception:
            pass

        # Even if the pygame_gui element was killed, the component instance
        # itself may still remain in memory as long as there are references to it.
        # That's why we explicitly check if self.element is not None before acting.
        if self.element is not None:
            try:
                self.element.kill()
            except Exception:
                pass
            finally:
                self.element = None

    def enable(self) -> None:
        """
        Enable the component.
        """
        if self.element is not None:
            self.element.enable()
    
    def disable(self) -> None:
        """
        Disable the component.
        """
        if self.element is not None:
            self.element.disable()