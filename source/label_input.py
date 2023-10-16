
import pygame as pg
from pygame.locals import *
import pygame_textinput as pt


class LabelInput:
    
    def __init__(self) -> None:
        pg.init()
        
        self.label_input = textinput = pt.TextInputVisualizer()
        self.manager = pt.TextInputManager(validator = lambda input: len(input) <= 5)
        
        pg.key.set_repeat(200, 25)
    
    
    def process(self, dt: float, events) -> None:
        self.label_input.update(events)




