import pygame as pg
from pygame.locals import *

from gui.button import Button


class CheckButton(Button):
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str='', text: str='') -> None:
        super().__init__(x, y, width, height, font, text, (0, 200, 0), (0, 120, 0))
    
    
    def handle_events(self, event) -> None:
        if self.input_rect.collidepoint(pg.mouse.get_pos()):
            self.hover = True
            self.pressed = (not self.pressed) if (event.type == MOUSEBUTTONDOWN) else self.pressed
        else:
            self.hover = False
    
    def render(self, display: pg.Surface) -> None:
        if self.hover or self.pressed: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_focused(self) -> bool:
        return self.hover
    
    def get_pressed(self) -> bool:
        return self.pressed
    