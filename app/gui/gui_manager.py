import pygame
from app.settings import *


class GUIManager:
    """
    Manages all GUI elements and overlays using pygame.

    Uses OpenGL context for 3D previews and pygame surface for 2D UI.
    """

    def __init__(self, app):
        self.app = app
        self.widgets = {}  # Dictionary of UI widgets

        # GUI state
        self.show_block_preview = True  # Toggle for 3D block preview

    def add_widget(self, name, widget):
        """Register a widget with the GUI system."""
        self.widgets[name] = widget

    def toggle_block_preview(self):
        """Toggle the 3D block preview window."""
        self.show_block_preview = not self.show_block_preview
        print(f"Block preview: {'ON' if self.show_block_preview else 'OFF'}")

    def update(self):
        """Update all active widgets."""
        for widget in self.widgets.values():
            if hasattr(widget, 'update'):
                widget.update()

    def render(self):
        """Render all visible widgets."""
        import moderngl

        # Render 3D widgets (like block preview) in OpenGL space
        if self.show_block_preview and 'block_preview' in self.widgets:
            # Disable depth test for UI overlay
            self.app.ctx.disable(moderngl.DEPTH_TEST)
            self.widgets['block_preview'].render()
            self.app.ctx.enable(moderngl.DEPTH_TEST)

    def handle_event(self, event):
        """Handle GUI-related events."""
        if event.type == pygame.KEYDOWN:
            # Toggle block preview with 'B' key
            if event.key == pygame.K_b:
                self.toggle_block_preview()
