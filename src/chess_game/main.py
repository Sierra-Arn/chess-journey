# src/chess_game/main.py
from typing import Dict
import sys
import pygame
from pygame_gui import UIManager
from .gui.screens import BaseScreen, SetupScreen, GameScreen
from .gui import event_manager

class ChessGameApp:
    """
    Main application class for the chess game.
    
    Manages the complete chess game application lifecycle including pygame
    initialization, screen management, event handling, and resource cleanup.
    Coordinates transitions between setup and game screens while maintaining
    stable frame rate and proper error handling. Implements proper screen
    lifecycle management through BaseScreen inheritance.
    
    Attributes:
        SCREEN_WIDTH: Application window width in pixels.
        SCREEN_HEIGHT: Application window height in pixels.
        FPS: Target frame rate for smooth gameplay.
        screen: Main pygame display surface.
        manager: pygame_gui UIManager for component management.
        clock: pygame Clock for frame rate control.
        running: Flag controlling main game loop execution.
        screens: Dictionary storing screen instances by name.
        current_screen_name: Name of currently active screen.
        current_screen: Reference to currently active screen instance.
        game_config: Configuration dictionary passed between screens.
    """
    
    def __init__(self):
        """
        Initialize chess game application with pygame and UI systems.
        
        Sets up pygame display, GUI manager, timing system, and initializes
        the first screen (setup screen). Configures application constants
        and prepares for main game loop execution.
        """
        # Initialize pygame
        pygame.init()
        
        # Application constants
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Create the main window
        self.screen_rect = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")
        
        # Create pygame_gui manager
        self.manager = UIManager(
            window_resolution=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )

        # Create clock for timing
        self.clock = pygame.time.Clock()
        
        # Application state
        self.running = True
        
        # Screen management
        self.screens: Dict[str, BaseScreen] = {}
        self.current_screen_name = None
        self.current_screen = None
        
        # Game configuration
        self.game_config = None
        
        # Initialize screens
        self._init_screens()
        
    def _init_screens(self) -> None:
        """
        Initialize all game screens.
        
        Creates setup screen as initial interface and prepares game screen
        creation mechanism. Uses proper screen rectangle positioning and
        establishes callback for game start transition.
        """
        # Create setup screen (shown first)
        self.screens['setup'] = SetupScreen(
            rect=self.screen_rect,
            manager=self.manager,
            on_start_game=self._on_start_game
        )
        
        # Game screen will be created when needed (with config)
        self.screens['game'] = None
        
        # Show setup screen initially
        self._show_screen('setup')
        
    def _show_screen(self, screen_name: str) -> None:
        """
        Show a specific screen and hide others.
        
        Manages screen transitions by properly destroying current screen
        and activating new screen. Maintains screen state consistency
        and prevents resource leaks during transitions.
        
        Args:
            screen_name: Name of screen to activate ('setup' or 'game').
        """
        # Hide current screen if exists
        if self.current_screen:
            self.current_screen.kill()
                
        # Show new screen
        if screen_name in self.screens:
            self.current_screen_name = screen_name
            self.current_screen = self.screens[screen_name]
            
    def _on_start_game(self) -> None:
        """
        Callback when user clicks 'Start Game' in setup screen.
        
        Retrieves game configuration from setup screen, creates or recreates
        game screen with configuration parameters, and transitions to game
        screen. Ensures proper cleanup of previous game instances.
        """
        # Get configuration from setup screen
        self.game_config = self.screens['setup'].get_game_config()
        print(f"Starting game with config: {self.game_config}")
        
        # Create or recreate game screen with the configuration
        if self.screens['game']:
            self.screens['game'].kill()
                
        # Pass configuration to new game screen
        self.screens['game'] = GameScreen(
            rect=self.screen_rect,
            manager=self.manager,
            game_config=self.game_config
        )
        
        # Show game screen
        self._show_screen('game')
        
    def run(self) -> None:
        """
        Run the main game loop.
        
        Executes primary application loop with event handling, state updates,
        and rendering. Maintains consistent frame rate and ensures proper
        cleanup on application exit or exception.
        """
        print("Starting Chess Game Application...")
        
        try:
            while self.running:
                time_delta = self.clock.tick(self.FPS) / 1000.0
                self._handle_events()
                self._update(time_delta)
                self._draw()
        finally:
            self._cleanup()
        
    def _handle_events(self) -> None:
        """
        Handle all pygame events.
        
        Processes system events (quit, etc.), GUI events through manager,
        custom events through event manager, and screen-specific events.
        Maintains proper event flow and prevents event processing during
        application shutdown.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            self.manager.process_events(event)
            event_manager.dispatch(event)
            
            if self.current_screen and hasattr(self.current_screen, 'handle_event'):
                self.current_screen.handle_event(event)
                
    def _update(self, time_delta: float) -> None:
        """
        Update application state.
        
        Updates current screen state and GUI manager. Handles time-based
        updates like animations, timers, and screen transitions.
        
        Args:
            time_delta: Time elapsed since last update in seconds.
        """
        if self.current_screen and hasattr(self.current_screen, 'update'):
            self.current_screen.update(time_delta)
        self.manager.update(time_delta)
                
    def _draw(self) -> None:
        """
        Draw all elements to the screen.
        
        Renders application background, current screen content, and GUI
        elements. Uses double buffering for smooth visual updates and
        maintains consistent visual hierarchy.
        """
        self.screen.fill((50, 50, 50))  # Dark gray background
        
        if self.current_screen and hasattr(self.current_screen, 'draw'):
            self.current_screen.draw(self.screen)
            
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        
    def _cleanup(self) -> None:
        """
        Clean up resources before exiting.
        
        Performs proper cleanup sequence by destroying all screen instances
        and shutting down pygame systems. Ensures no resources are leaked
        and all background processes are terminated gracefully.
        """
        # Kill all screens
        for screen in self.screens.values():
            if screen:
                screen.kill()
            
        pygame.quit()

def main() -> None:
    """
    Main entry point function.
    
    Creates and runs chess game application with proper error handling.
    Ensures clean application exit even in case of unhandled exceptions.
    """
    try:
        app = ChessGameApp()
        app.run()
    except Exception:
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()