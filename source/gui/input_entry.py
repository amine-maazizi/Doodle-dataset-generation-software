
import pygame as pg
from pygame.locals import *

from gui.gui_element import GUIElement


class InputEntry(GUIElement):
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str='') -> None:
        super().__init__(x, y, width, height, font, active_color=(255, 255, 255), passive_color=(50, 50, 50))
    
    def handle_events(self, event) -> None:
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
        if self.pressed: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.user_text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_focused(self) -> bool:
        return self.pressed

    def get_entry(self) -> str:
        return self.user_text
    