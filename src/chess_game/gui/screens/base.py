# src/chess_game/gui/screens/base.py
from typing import Dict
from abc import ABC, abstractmethod
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIContainer
from ..components import BaseComponent, RectType

class BaseScreen(ABC):
    """
    Base class for all game screens.
    
    Provides common functionality for screen management including UIContainer,
    component lifecycle management, and basic screen operations. Implements
    abstract base class pattern to enforce UI creation contract for subclasses.
    Manages hierarchical UI organization through container system and ensures
    proper resource cleanup during screen transitions.
    
    Attributes:
        rect: Screen bounding rectangle defining position and dimensions.
        manager: Pygame GUI manager for UI element lifecycle management.
        container: UIContainer grouping all screen elements for easy management.
        components: Dictionary mapping component names to BaseComponent instances.
    """

    def __init__(
        self, 
        rect: RectType, 
        manager: UIManager
    ):
        """
        Initialize base screen with positioning and UI manager.
        
        Creates UI container that serves as parent for all screen elements,
        enabling coordinated positioning and cleanup. Initializes component
        registry for tracking and managing child UI elements.
        
        Args:
            rect: Rectangle defining screen position and dimensions.
            manager: Pygame GUI manager for element creation and lifecycle.
        """
        self.rect = Rect(rect)
        self.manager = manager
        
        # Create container for all screen elements
        self.container = UIContainer(
            relative_rect=self.rect,
            manager=self.manager
        )
        
        # Store component references for cleanup
        self.components: Dict[str, BaseComponent] = {}
        
        # Create screen-specific UI
        self._create_ui()

    @abstractmethod
    def _create_ui(self) -> None:
        """
        Create all UI elements for the screen.
        
        Abstract method that must be implemented by subclasses to
        initialize screen-specific UI components. Called during
        initialization to populate the screen with interactive elements.
        Components should be registered via add_component() method.
        """
        pass

    def add_component(self, name: str, component: BaseComponent) -> None:
        """
        Add a component to the components dictionary.
        
        Registers UI component for automatic cleanup and potential
        future retrieval by name. Maintains reference to enable
        coordinated destruction during screen transition.
        
        Args:
            name: Unique identifier for the component.
            component: BaseComponent instance to register.
        """
        self.components[name] = component

    def kill(self) -> None:
        """
        Remove all UI elements from the screen.
        
        Performs coordinated cleanup by destroying all registered
        components and the parent container. Ensures no UI elements
        remain in pygame_gui system to prevent memory leaks or
        ghost elements persisting after screen transition.
        """
        for component in self.components.values():
            component.kill()
        self.container.kill()