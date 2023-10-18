from abc import ABC, abstractmethod
import pygame as pg
from pygame.locals import *

class GUIElement(ABC):
    """
    Abstract base class for GUI elements.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str = '', text: str = '',
                 active_color: [int, int, int] = (255, 255, 255),
                 passive_color: [int, int, int] = (50, 50, 50)) -> None:
        """Initialize a GUI element."""
        self.input_rect = pg.Rect(x, y, width, height)
        self.font = pg.font.Font(None, 16) if not font else pg.font.Font(font, 16)
        self.text = text
        self.active_color = active_color
        self.passive_color = passive_color
        self.pressed = False
        self.hover = False
        self.user_text = ''

    @abstractmethod
    def handle_events(self, event) -> None:
        """Handle GUI element-specific events. Must be implemented by subclasses."""
        ...

    @abstractmethod
    def render(self, display: pg.Surface) -> None:
        """Render the GUI element. Must be implemented by subclasses."""
        ...

    @abstractmethod
    def get_focused(self) -> bool:
        """Check if the element is currently focused (e.g., for text input). Must be implemented by subclasses."""
        ...
