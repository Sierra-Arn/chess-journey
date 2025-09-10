# src/chess_game/gui/widgets/base.py
from abc import ABC
from typing import List
from ..components import BaseComponent

class BaseWidget(BaseComponent, ABC):
    """
    Base class for composite UI widgets.
    
    Extends BaseComponent to provide automatic management of children components.
    Children components are automatically killed when the widget is destroyed.
    The disable() and enable() methods are automatically applied to all children components.
    """
    
    def __init__(self, *args, **kwargs):
        self._children: List[BaseComponent] = []
        super().__init__(*args, **kwargs)
    
    def add_child(self, child: BaseComponent) -> None:
        """
        Add a child component to be managed by this widget.
        
        Args:
            child: The child component to manage
        """
        self._children.append(child)
    
    def remove_child(self, child: BaseComponent) -> None:
        """
        Remove a child component from management.
        
        Args:
            child: The child component to remove
        """
        if child in self._children:
            self._children.remove(child)
    
    def kill(self) -> None:
        """
        Cleanly destroy the widget and all its child components.
        
        This method ensures proper cleanup by:
        1. Creating a copy of the children list to avoid modification during iteration,
        since child.kill() may modify the original _children list during cleanup
        2. Iteratively killing each child component to ensure proper resource cleanup
        3. Clearing the internal children tracking list to prevent memory leaks
        4. Finally killing the widget's own UI element through the parent class
        """

        for child in self._children[:]:  # Copy list to avoid modification during iteration
            try:
                child.kill()
            except Exception:
                pass
        
        self._children.clear()
        
        super().kill()

    def _register_events(self) -> None:
        """
        No events needed for widgets as all interactions are handled by children components.
        """
        pass