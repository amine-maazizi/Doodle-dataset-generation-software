import pygame as pg
from pygame.locals import *

from gui.gui_element import GUIElement


class Button(GUIElement):
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str='', text: str='', active_color: [int, int, int] = (255, 0, 0), 
                 passive_color: [int, int, int] = (120, 0, 0)) -> None:
        super().__init__(x, y, width, height, font, text, active_color, passive_color)
    
    
    def handle_events(self, event) -> None:
        if self.input_rect.collidepoint(pg.mouse.get_pos()):
            self.hover = True
            self.pressed = (event.type == MOUSEBUTTONDOWN)
        else:
            self.hover = self.pressed = False
    
    def render(self, display: pg.Surface) -> None:
        if self.hover: 
            color = self.active_color
        else: 
            color = self.passive_color
        pg.draw.rect(display, color, self.input_rect)  
        text_surface = self.font.render(self.text, True, (0, 0, 0)) 
        display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5)) 
        self.input_rect.w = max(100, text_surface.get_width() + 10) 

    def get_focused(self) -> bool:
        return self.pressed

    def get_pressed(self) -> str:
        return self.pressed
    