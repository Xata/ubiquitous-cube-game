"""
Game mode definitions and management.

Defines the different game modes available in the game.
"""

from enum import Enum


class GameMode(Enum):
    """
    Available game modes.

    DEBUG: Creative mode with flight, no health, instant block breaking
    GAME: Survival mode with inventory, health, hunger, enemies
    """
    DEBUG = "debug"
    GAME = "game"


class GameModeManager:
    """
    Manages the current game mode and mode switching.

    Attributes:
        current_mode: The currently active game mode
    """

    def __init__(self, starting_mode=GameMode.DEBUG):
        """
        Initialize the game mode manager.

        Args:
            starting_mode: The mode to start in (default: DEBUG)
        """
        self.current_mode = starting_mode
        print(f"Game mode: {self.current_mode.value.upper()}")

    def switch_mode(self, new_mode):
        """
        Switch to a different game mode.

        Args:
            new_mode: The GameMode to switch to
        """
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            print(f"Switched to {self.current_mode.value.upper()} mode")
            return True
        return False

    def toggle_mode(self):
        """
        Toggle between DEBUG and GAME modes.
        """
        if self.current_mode == GameMode.DEBUG:
            self.switch_mode(GameMode.GAME)
        else:
            self.switch_mode(GameMode.DEBUG)

    def is_debug(self):
        """Check if currently in DEBUG mode."""
        return self.current_mode == GameMode.DEBUG

    def is_game(self):
        """Check if currently in GAME mode."""
        return self.current_mode == GameMode.GAME
