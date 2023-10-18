import pygame as pg
from pygame.locals import *
from gui.gui_element import GUIElement

class InputEntry(GUIElement):
    """Input text entry GUI element."""

    def __init__(self, x: int, y: int, width: int, height: int, font: str='') -> None:
        """Initialize an input text entry element."""
        super().__init__(x, y, width, height, font, active_color=(255, 255, 255), passive_color=(50, 50, 50))
    
    def handle_events(self, event) -> None:
        """Handle mouse and keyboard events for text entry."""
        if event.type == MOUSEBUTTONDOWN: 
            if self.input_rect.collidepoint(event.pos): 
                self.pressed = True
            else: 
                self.pressed = False
  
        if event.type == KEYDOWN and self.pressed: 
            if event.key == K_BACKSPACE: 
                self.user_text = self.user_text[:-1] 
            else: 
                self.user_text += event.unicode
    
    def render(self, display: pg.Surface) -> None:
        """Render the text entry element on the provided display."""
        if self.pressed: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.user_text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_focused(self) -> bool:
        """Check if the text entry is focused (clicked)."""
        return self.pressed

    def get_entry(self) -> str:
        """Get the text entered in the input field."""
        return self.user_text
