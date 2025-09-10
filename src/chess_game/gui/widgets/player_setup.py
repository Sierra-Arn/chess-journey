# src/chess_game/gui/widgets/player_setup.py
from pygame import Rect
from pygame_gui import UIManager
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIPanel
from .import BaseWidget 
from ..components import RectType, Label, DropdownMenu, TextInput, Slider
from ...custom_types import PlayerType

class PlayerSetupWidget(BaseWidget):
    """
    Minimal player configuration block for setup screen.
    
    Contains labels, dropdown for player type, text input for player name,
    difficulty slider for AI player, and time control slider.

    Attributes:
        default_title: Default title text for the player section.
        default_name: Default name for the player.
        title_label: Label displaying the player section title.
        type_dropdown: Dropdown for selecting player type (PlayerType.HUMAN.value, PlayerType.AI.value).
        name_input: Text input for player name.
        difficulty_label: Label for AI difficulty setting.
        difficulty_slider: Slider for AI difficulty level (1-20).
        time_label: Label for time control setting.
        time_slider: Slider for player time control in minutes (1-60).
        element: UIPanel container for all child components.
    """

    def __init__(
        self,
        rect: RectType,
        manager: UIManager,
        container: UIContainer,
        default_title: str,
        default_name: str
    ):
        self.default_title = default_title
        self.default_name = default_name

        super().__init__(rect, manager, container)
        
        # Wrap the type change callback to handle difficulty slider enable/disable
        self.type_dropdown.on_selection_changed = self._handle_type_change

    def create_element(self) -> None:
        """
        Create panel container and child components for player setup.
        
        Instantiates the UIPanel container and initializes all child components
        in a vertical layout with consistent padding.
        """
        self.element = UIPanel(
            relative_rect=self.rect,
            manager=self.manager,
            container=self.container
        )
        self._initialize_components()

    def _initialize_components(self) -> None:
        """
        Create and position all child components inside panel with vertical layout and padding.
        
        Calculates layout parameters and creates all UI components in sequence.
        """
        self._calculate_layout_params()
        self._create_title_label()
        self._create_type_dropdown()
        self._create_name_input()
        self._create_difficulty_label()
        self._create_difficulty_slider()
        self._create_time_label()
        self._create_time_slider()
        self._update_ui_state()

    def _calculate_layout_params(self) -> None:
        """
        Calculate common layout dimensions and padding values.
        
        Computes component heights and padding based on panel dimensions to ensure
        consistent vertical spacing across all child components.
        """
        self._panel_width = self.rect.width
        self._panel_height = self.rect.height
        self._padding = 10
        self._horizontal_padding = self._padding
        self._vertical_padding = self._padding // 2
        self._total_vertical_padding = 8 * self._vertical_padding
        self._available_height = self._panel_height - self._total_vertical_padding
        self._component_height = self._available_height // 7

    def _create_title_label(self) -> None:
        """
        Create and position the title label component.
        
        Displays the player section title at the top of the panel.
        """
        title_rect = Rect(
            self._horizontal_padding, 
            self._vertical_padding, 
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.title_label = Label(
            rect=title_rect, 
            manager=self.manager, 
            container=self.element, 
            text=self.default_title
        )
        self.add_child(self.title_label)

    def _create_type_dropdown(self) -> None:
        """
        Create and position the player type dropdown menu.
        
        Allows selection between human and AI player types.
        """
        dropdown_rect = Rect(
            self._horizontal_padding, 
            self._component_height + 2 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.type_dropdown = DropdownMenu(
            rect=dropdown_rect,
            manager=self.manager,
            container=self.element,
            options_list=[PlayerType.HUMAN.value, PlayerType.AI.value], 
        )
        self.add_child(self.type_dropdown)

    def _create_name_input(self) -> None:
        """
        Create and position the player name text input field.
        
        Text input for human player names with placeholder guidance.
        """
        name_rect = Rect(
            self._horizontal_padding,
            2 * self._component_height + 3 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.name_input = TextInput(
            rect=name_rect,
            manager=self.manager,
            container=self.element,
            initial_text=self.default_name,
            placeholder_text=f"{self.default_name} Name (if applicable)"
        )
        self.add_child(self.name_input)

    def _create_difficulty_label(self) -> None:
        """
        Create and position the AI difficulty level label.
        
        Descriptive label for the AI difficulty slider control.
        """
        difficulty_label_rect = Rect(
            self._horizontal_padding,
            3 * self._component_height + 4 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.difficulty_label = Label(
            rect=difficulty_label_rect,
            manager=self.manager,
            container=self.element,
            text="AI Difficulty Level (if applicable)"
        )
        self.add_child(self.difficulty_label)

    def _create_difficulty_slider(self) -> None:
        """
        Create and position the AI difficulty level slider.
        
        Slider control for setting AI skill level from 1 (weakest) to 20 (strongest).
        """
        difficulty_slider_rect = Rect(
            self._horizontal_padding,
            4 * self._component_height + 5 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.difficulty_slider = Slider(
            rect=difficulty_slider_rect,
            manager=self.manager,
            container=self.element,
            start_value=10,
            value_range=(1, 20)
        )
        self.add_child(self.difficulty_slider)

    def _create_time_label(self) -> None:
        """
        Create and position the time control label.
        
        Descriptive label for the player time control slider.
        """
        time_label_rect = Rect(
            self._horizontal_padding,
            5 * self._component_height + 6 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.time_label = Label(
            rect=time_label_rect,
            manager=self.manager,
            container=self.element,
            text="Player Time Control (minutes)"
        )
        self.add_child(self.time_label)

    def _create_time_slider(self) -> None:
        """
        Create and position the time control slider.
        
        Slider control for setting player time from 1 to 60 minutes.
        """
        time_slider_rect = Rect(
            self._horizontal_padding,
            6 * self._component_height + 7 * self._vertical_padding,
            self._panel_width - 2 * self._horizontal_padding, 
            self._component_height
        )
        self.time_slider = Slider(
            rect=time_slider_rect,
            manager=self.manager,
            container=self.element,
            start_value=600,
            value_range=(60, 3600)
        )
        self.add_child(self.time_slider)

    def _handle_type_change(self, value: str) -> None:
        """
        Handle player type change and update UI elements' state.
        
        Args:
            value: Selected player type (PlayerType.HUMAN.value or PlayerType.AI.value).
        """
        
        # Update UI state
        self._update_ui_state()

    def _update_ui_state(self) -> None:
        """
        Enable/disable UI elements based on player type.
        
        Controls the interactive state of name input and difficulty controls:
        - If AI: disable name input, enable difficulty slider and label
        - If Human: enable name input, disable difficulty slider and label
        - Time control is always enabled for both player types
        """
        is_ai = self.type_dropdown.current_value == PlayerType.AI.value
        
        if is_ai:
            self.name_input.disable()
            self.difficulty_label.enable()
            self.difficulty_slider.enable()
        else:
            self.name_input.enable()
            self.difficulty_label.disable()
            self.difficulty_slider.disable()

    def get_config(self) -> dict:
        """
        Return current player configuration.
        
        Provides a dictionary with player settings based on current UI state:
        - For AI: return type, name='Stockfish', difficulty level, and time control
        - For Human: return type, entered name, difficulty=None, and time control
        
        Returns:
            Dictionary containing player type, name, difficulty, and time settings.
        """
        player_type = PlayerType(self.type_dropdown.current_value)
        
        if player_type == PlayerType.AI:
            return {
                "type": PlayerType.AI.value,
                "name": "Stockfish",
                "difficulty": self.difficulty_slider.current_value,
                "time": self.time_slider.current_value
            }
        else:
            return {
                "type": PlayerType.HUMAN.value,
                "name": self.name_input.current_text,
                "difficulty": None,
                "time": self.time_slider.current_value
            }