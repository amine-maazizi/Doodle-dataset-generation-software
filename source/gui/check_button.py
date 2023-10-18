import pygame as pg
from pygame.locals import *
from gui.button import Button

class CheckButton(Button):
    """Clickable check button GUI element."""

    def __init__(self, x: int, y: int, width: int, height: int, font: str='', text: str='') -> None:
        """Initialize a check button."""
        super().__init__(x, y, width, height, font, text, (0, 200, 0), (0, 120, 0))
    
    def handle_events(self, event) -> None:
        """Handle mouse events for the check button."""
        if self.input_rect.collidepoint(pg.mouse.get_pos()):
            self.hover = True
            self.pressed = (not self.pressed) if (event.type == MOUSEBUTTONDOWN) else self.pressed
        else:
            self.hover = False
    
    def render(self, display: pg.Surface) -> None:
        """Render the check button on the provided display."""
        if self.hover or self.pressed: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_focused(self) -> bool:
        """Check if the check button is focused (hovered)."""
        return self.hover
    
    def get_pressed(self) -> bool:
        """Check if the check button is pressed."""
        return self.pressed
