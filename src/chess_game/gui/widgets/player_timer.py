# src/chess_game/gui/widgets/player_timer.py
from typing import Optional
import time
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIPanel
from ..components import RectType, Label
from ..widgets import BaseWidget

class PlayerTimerWidget(BaseWidget):
    """
    Player timer widget with real-time countdown display.

    Wraps pygame_gui's UIPanel to create a visually distinct timer container.
    Displays player name and remaining time in a vertical layout.
    Automatically updates time display based on real-world elapsed time.

    Attributes:
        player_name: Name of the player associated with this timer.
        initial_time: Starting time value in seconds.
        remaining_time: Current remaining time in seconds.
        is_active: Flag indicating whether timer is currently counting down.
        last_update_time: Timestamp of the last update; used to compute elapsed time so 
                          the timer counts down based on real time, not frame rate.
        element: UIPanel container for the timer widget.
        name_label: Label displaying the player's name.
        time_label: Label displaying the formatted remaining time.
    """

    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        player_name: str,
        initial_time: int
    ):
        self.player_name = player_name
        self.initial_time = initial_time
        self.remaining_time = initial_time
        self.is_active = False
        self.last_update_time: Optional[float] = None

        super().__init__(rect, manager, container)

    def create_element(self) -> None:
        """
        Create panel container and child components for timer.

        Instantiates the UIPanel container and initializes the name and time labels
        as child components within the panel.
        """
        self.element = UIPanel(
            relative_rect=self.rect,
            manager=self.manager,
            container=self.container
        )
        self._initialize_labels()

    def _initialize_labels(self) -> None:
        """
        Create and position name and time labels.

        Divides the panel vertically into two equal parts:
        - Top half: player name label
        - Bottom half: remaining time label
        """
        label_height = self.rect.height // 2
        name_rect = Rect(0, 0, self.rect.width, label_height)
        time_rect = Rect(0, label_height, self.rect.width, label_height)
        
        self.name_label = Label(
            rect=name_rect,
            manager=self.manager,
            container=self.element,
            text=self.player_name
        )
        
        self.time_label = Label(
            rect=time_rect,
            manager=self.manager,
            container=self.element,
            text=self._format_time(self.initial_time)
        )
        
        self.add_child(self.name_label)
        self.add_child(self.time_label)

    def draw(self) -> None:
        """
        Update time label text (only if changed).

        Computes the new time display and updates the label only when
        the text content actually changes to avoid unnecessary redraws.
        """
        self._update_time()
        new_text = self._format_time(self.remaining_time)
        if self.time_label.element is not None:
            if new_text != self.time_label.element.text:
                self.time_label.set_text(new_text)

    def _update_time(self) -> None:
        """
        Update countdown if active.

        Calculates elapsed time since last update using real-world timestamps
        and decrements the remaining time accordingly. Ensures time never goes below zero.

        Note: This method should be called frequently (e.g., every frame) to maintain
        accurate timing, but the actual time calculation is based on wall-clock time,
        not frame rate.
        """
        if not self.is_active or self.remaining_time <= 0:
            return

        current_time = time.time()
        if self.last_update_time is not None:
            elapsed = current_time - self.last_update_time
            self.remaining_time = max(0.0, self.remaining_time - elapsed)
        self.last_update_time = current_time

    def _format_time(self, seconds: float) -> str:
        """
        Format time as MM:SS.

        Converts a time value in seconds to a human-readable string format.

        Args:
            seconds: Time value in seconds to format.

        Returns:
            Formatted time string in MM:SS format.
        """
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02d}:{secs:02d}"

    def set_active(self, active: bool) -> None:
        """
        Activate or pause timer.

        Controls the timer's active state and manages the timestamp tracking
        for accurate elapsed time calculation.

        Args:
            active: True to start/resume timer, False to pause it.
        """
        if self.is_active and not active:
            self._update_time()
            self.last_update_time = None
        elif not self.is_active and active:
            self.last_update_time = time.time()
        
        self.is_active = active
        
        if active:
            self.element.enable()
        else:
            self.element.disable()

    def reset(self) -> None:
        """
        Reset timer to initial state and update label immediately.

        Restores the timer to its original configuration:
        - Resets remaining time to initial value
        - Stops the timer
        - Clears the last update timestamp
        - Updates display labels to show initial values
        - Disables the UI element
        """
        self.remaining_time = self.initial_time
        self.is_active = False
        self.last_update_time = None
        
        if self.time_label.element is not None:
            self.time_label.set_text(self._format_time(self.initial_time))
        if self.name_label.element is not None:
            self.name_label.set_text(self.player_name)

        self.element.disable()