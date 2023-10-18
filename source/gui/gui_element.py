from abc import ABC, abstractmethod



import pygame as pg
from pygame.locals import *


class GUIElement(ABC):
    
    def __init__(self, x: int, y: int, width: int, height: int, font: str = '', text: str = '', active_color: [int, int, int] = (255, 255, 255),
                passive_color: [int, int, int] = (50, 50, 50)) -> None:
        self.input_rect = pg.Rect(x, y, width, height)
        self.font = pg.font.Font(None, 16)
        if font:
            self.font = pg.font.Font(font, 16) 
        self.text = text
        self.active_color = active_color
        self.passive_color = passive_color
        self.pressed = False
        self.hover = False
        self.user_text = ''
    
    @abstractmethod
    def handle_events(self, event) -> None:
        ...
    
    @abstractmethod
    def render(self, display: pg.Surface) -> None:
        ...

    @abstractmethod
    def get_focused(self) -> bool:
        ...