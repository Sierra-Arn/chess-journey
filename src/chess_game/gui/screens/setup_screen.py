# src/chess_game/gui/screens/setup_screen.py
from typing import Callable, Dict
from pygame_gui import UIManager
from ..components import BaseComponent, RectType, Label, DropdownMenu, Button
from ..widgets import PlayerSetupWidget
from ...custom_types import ModeType, OrientationType
from .base import BaseScreen

class SetupScreen(BaseScreen):
    """
    Setup screen for configuring chess game parameters.
    
    Manages the game configuration interface allowing users to set player types,
    names, difficulty levels, time controls, game mode, and board orientation.
    Provides a structured layout for all game setup options before starting play.

    Attributes:
        on_start_game: Callback function to start the game with current config.
        white_player: PlayerSetupWidget for white player configuration.
        black_player: PlayerSetupWidget for black player configuration.
        mode_label: Label for game mode selection.
        mode_dropdown: DropdownMenu for choosing Standard or Chess960.
        orientation_label: Label for board orientation selection.
        orientation_dropdown: DropdownMenu for choosing board bottom color.
        start_button: Button to begin game with current settings.
    """

    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        on_start_game: Callable[[], None]
    ):
        """
        Initialize setup screen with UI manager and start callback.
        
        Creates complete game configuration interface with player setup sections,
        game mode options, and start button. Uses BaseScreen container system
        for automatic cleanup and positioning.
        
        Args:
            rect: Rectangle defining screen position and dimensions.
            manager: Pygame GUI manager for component creation and lifecycle.
            on_start_game: Callback function invoked when start button clicked.
        """
        self.on_start_game = on_start_game

        # Store component references
        self.components: Dict[str, BaseComponent] = {}

        # Initialize base screen (calls _create_ui)
        super().__init__(rect, manager)

    def _create_ui(self) -> None:
        """
        Create all UI elements for the setup screen.

        Arranges player configuration sections, game options, and start button
        in a structured layout with consistent spacing and alignment. Calculates
        layout parameters and creates all interactive components in proper order.
        """
        self._calculate_layout_params()
        self._create_player_sections()
        self._create_game_options()
        self._create_start_button()
        self._store_component_references()

    def _calculate_layout_params(self) -> None:
        """
        Calculate common layout dimensions and positioning values.
        
        Computes screen dimensions, margins, and component sizes for consistent layout.
        Pre-calculates positioning values to ensure proper alignment of all elements.
        """
        self._screen_x = int(self.container.rect.x)
        self._screen_y = int(self.container.rect.y)
        self._screen_w = int(self.container.rect.width)
        self._screen_h = int(self.container.rect.height)
        self._margin = 20
        self._section_height = 240
        self._control_height = 40
        self._button_height = 50
        self._player_section_width = (self._screen_w - 3 * self._margin) // 2

    def _create_player_sections(self) -> None:
        """
        Create player configuration sections for both players.
        
        Initializes PlayerSetupWidget instances for white and black player settings.
        Positions sections side-by-side with appropriate spacing and dimensions.
        """
        white_rect = (
            self._screen_x + self._margin,
            self._screen_y + self._margin,
            self._player_section_width,
            self._section_height
        )
        self.white_player = PlayerSetupWidget(
            rect=white_rect,
            manager=self.manager,
            container=self.container,
            default_title="White Player Settings",
            default_name="White Player"
        )

        black_rect = (
            self._screen_x + self._margin * 2 + self._player_section_width,
            self._screen_y + self._margin,
            self._player_section_width,
            self._section_height
        )
        self.black_player = PlayerSetupWidget(
            rect=black_rect,
            manager=self.manager,
            container=self.container,
            default_title="Black Player Settings",
            default_name="Black Player"
        )

    def _create_game_options(self) -> None:
        """
        Create game mode and board orientation selection controls.
        
        Sets up dropdown menus and labels for game configuration options.
        Positions controls in vertical stack below player configuration sections.
        """
        # Game mode controls
        mode_label_rect = (
            self._screen_x + self._margin,
            self._screen_y + self._margin * 2 + self._section_height,
            150,
            self._control_height
        )
        self.mode_label = Label(
            rect=mode_label_rect,
            manager=self.manager,
            container=self.container,
            text="Game Mode:"
        )

        mode_dropdown_rect = (
            self._screen_x + self._margin + 160,
            self._screen_y + self._margin * 2 + self._section_height,
            200,
            self._control_height
        )
        self.mode_dropdown = DropdownMenu(
            rect=mode_dropdown_rect,
            manager=self.manager,
            container=self.container,
            options_list=[ModeType.STANDARD.value, ModeType.CHESS960.value]
        )

        # Board orientation controls
        orientation_label_rect = (
            self._screen_x + self._margin,
            self._screen_y + self._margin * 3 + self._section_height + self._control_height,
            150,
            self._control_height
        )
        self.orientation_label = Label(
            rect=orientation_label_rect,
            manager=self.manager,
            container=self.container,
            text="Board Bottom:"
        )

        orientation_dropdown_rect = (
            self._screen_x + self._margin + 160,
            self._screen_y + self._margin * 3 + self._section_height + self._control_height,
            200,
            self._control_height
        )
        self.orientation_dropdown = DropdownMenu(
            rect=orientation_dropdown_rect,
            manager=self.manager,
            container=self.container,
            options_list=[OrientationType.WHITE.value, OrientationType.BLACK.value]
        )

    def _create_start_button(self) -> None:
        """
        Create the start game button centered at the bottom of the screen.
        
        Initializes the main action button that triggers game start.
        Positioned at bottom of screen with appropriate margin and sizing.
        """
        button_width = 200
        start_button_rect = (
            self._screen_x + (self._screen_w - button_width) // 2,
            self._screen_y + self._screen_h - self._margin - self._button_height,
            button_width,
            self._button_height
        )
        self.start_button = Button(
            rect=start_button_rect,
            manager=self.manager,
            container=self.container,
            text="Start Game",
            on_click=self._on_start_clicked
        )

    def _store_component_references(self) -> None:
        """
        Store references to all created UI components in a dictionary.
        
        Maintains a collection of all components for easy management and cleanup.
        Enables centralized component access and proper destruction handling.
        """
        self.components = {
            'white_player': self.white_player,
            'black_player': self.black_player,
            'mode_label': self.mode_label,
            'mode_dropdown': self.mode_dropdown,
            'orientation_label': self.orientation_label,
            'orientation_dropdown': self.orientation_dropdown,
            'start_button': self.start_button
        }

    def _on_start_clicked(self) -> None:
        """
        Handle start button click.

        Invokes the on_start_game callback to transition to game screen.
        Provides clean separation between UI interaction and game logic.
        """
        self.on_start_game()

    def get_game_config(self) -> dict:
        """
        Return complete game configuration.

        Provides a dictionary containing all game setup parameters including
        player configurations, game mode, and board orientation settings.
        Formats configuration data for consumption by game screen.
        
        Returns:
            Dictionary containing complete game configuration parameters.
        """
        return {
            'players': {
                'white': self.white_player.get_config(),
                'black': self.black_player.get_config()
            },
            'game_mode': getattr(self.mode_dropdown, 'current_value', None),
            'board_orientation': getattr(self.orientation_dropdown, 'current_value', None)
        }

    def kill(self) -> None:
        """
        Remove all UI elements from the screen.

        Cleans up all components and delegates container destruction to
        parent BaseScreen class. Ensures proper UI state management when
        switching screens and prevents memory leaks.
        """
        for component in self.components.values():
            try:
                component.kill()
            except Exception:
                pass

        # Call parent kill to cleanup container
        super().kill()