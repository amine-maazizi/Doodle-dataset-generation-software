
import pygame as pg
from pygame.locals import *


class InputEntry:
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str='', active_color: [int, int, int] = (255, 255, 255),
                passive_color: [int, int, int] = (50, 50, 50)) -> None:
        self.input_rect = pg.Rect(x, y, width, height)
        self.font = pg.font.Font(None, 16)
        if font:
            self.font = pg.font.Font(font, 16) 
        self.active_color = active_color
        self.passive_color = passive_color
        self.hover = False
        self.user_text = ''
    
    def handle_events(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN: 
            if self.input_rect.collidepoint(event.pos): 
                self.hover = True
            else: 
                self.hover = False
  
        if event.type == KEYDOWN and self.hover: 
            if event.key == K_BACKSPACE: 
                self.user_text = self.user_text[:-1] 
            else: 
                self.user_text += event.unicode
    
    def render(self, display: pg.Surface) -> None:
        if self.hover: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.user_text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_entry(self) -> str:
        return self.user_text
    