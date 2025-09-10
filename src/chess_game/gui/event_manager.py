# src/chess_game/gui/event_manager.py
from typing import Dict, TypeAlias, Callable
from pygame.event import Event
from pygame_gui.core import UIElement

# TypeAlias tells type checkers "this name is a type alias",
# so the assignment should be interpreted as a type definition (PEP 613).

# A callable object (function, lambda, or class with __call__) 
# that takes one argument of type Event and returns None.
CallbackType = Callable[[Event], None]
CallbackMap: TypeAlias = Dict[int, CallbackType]
UIElementCallbackMap: TypeAlias = Dict[UIElement, CallbackMap]


class EventManager:
    """
    Manages registration and dispatching of pygame_gui events to component callbacks.
    
    Purpose
    -------
    Instead of each component checking all events, this manager receives events
    and directly calls the appropriate callback based on the pygame_gui UI element and event type.

    Internal structure
    ------------------
    _callbacks is a two-level dictionary:
     - the first key is a UIElement (button, text box, etc.)
     - the value is another dict, where:
          * the key is an event type (int, e.g. UI_BUTTON_PRESSED)
          * the value is the function (callback) to run when that event happens
    
    Example structure:
    {
        some_button: {
            UI_BUTTON_PRESSED:   on_button_click,
            UI_BUTTON_UNPRESSED: on_button_release
        },
        text_input: {
            UI_TEXT_CHANGED: on_text_change
        }
    }

    Note
    ----
    In pygame (and pygame_gui), events are internally represented as integers.
    Readable constants like pygame.QUIT or UI_BUTTON_PRESSED are just named ints
    that map to specific numeric event type codes.

    That's why in CallbackMap we use int and not some special pygame event type.
    """

    def __init__(self):
        self._callbacks: UIElementCallbackMap = {}

    def register_callback(
        self, 
        ui_element: UIElement, 
        event_type: int, 
        callback: CallbackType
    ) -> None:
        """
        Register a callback for a specific UI element and event type.
        """
        if ui_element not in self._callbacks:
            self._callbacks[ui_element] = {}
        self._callbacks[ui_element][event_type] = callback

    def unregister_all_callbacks(self, ui_element: UIElement) -> None:
        """
        Remove all callbacks for a specific UI element.
        """
        self._callbacks.pop(ui_element, None)

    def dispatch(self, event: Event) -> bool:
        """
        Dispatch an event to the appropriate callback.
        Returns True if the event was handled by a registered callback.
        """

        # This is a built-in Python function that checks whether the object `event` has
        # an attribute named "ui_element".
        if hasattr(event, "ui_element"):

            # In pygame_gui, developers extend pygame.event.Event by dynamically attaching
            # extra attributes (e.g. `ui_element`). 
            # Since pygame_gui does not provide type annotations for these dynamic fields, 
            # static type checkers cannot see them and report them as missing.
            ui_element: UIElement = event.ui_element
            callbacks: CallbackMap | None = self._callbacks.get(ui_element)
            if callbacks:
                callback: CallbackType | None = callbacks.get(event.type)
                if callback:
                    callback(event)
                    return True
        return False

    def has_callbacks(self, ui_element: UIElement) -> bool:
        """
        Check if a UI element has any registered callbacks.
        """
        return ui_element in self._callbacks


event_manager = EventManager()