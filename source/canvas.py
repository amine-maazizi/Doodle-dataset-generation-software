import pygame as pg
from pygame.locals import *
import numpy as np


class Canvas:
    def __init__(self, config: dict, array_width: int, array_height: int) -> None:
        """
        Initialize the Canvas.

        Args:
            display (pg.Surface): The Pygame surface for displaying the canvas.
            array_width (int): Width of the canvas array.
            array_height (int): Height of the canvas array.
        """
        self.arr_w, self.arr_h = array_width, array_height
        self.win_w, self.win_h = config['ScreenDim']
        self.canvas_array: np.ndarray = np.zeros((array_width, array_height, 3), dtype=np.uint8)
        
    def process(self, dt: float) -> None:
        """
        Process user input to draw on the canvas.

        Args:
            dt (float): Time elapsed since the last frame (not used in this method).
        """
        left_pressed, _, right_pressed = pg.mouse.get_pressed()
        paint = left_pressed and not right_pressed
        if left_pressed or right_pressed:
            x, y = pg.mouse.get_pos()
            
            if (0 <= x < self.win_w) and (0 <= y < self.win_h):
                x_scale = self.arr_w / self.win_w
                y_scale = self.arr_h / self.win_h
                x_target, y_target = int(x * x_scale), int(y * y_scale)
                self.canvas_array[x_target, y_target] = (255, 255, 255) if paint else (0, 0, 0)
    
    def render(self, display: pg.Surface) -> None:
        """
        Render the canvas on the display surface.
        """
        base_surface = pg.surfarray.make_surface(self.canvas_array)
        scaled_surface = pg.transform.scale(base_surface, (self.win_w, self.win_h))
        display.blit(scaled_surface, (0, 0))

    def get_canvas_array(self) -> np.array:
        return self.canvas_array
    
    def get_canvas_dimensions(self) -> (int, int):
        return self.arr_w, self.arr_h
    
    def clear_canvas(self) -> None:
        self.canvas_array = np.zeros((self.arr_w, self.arr_h, 3), dtype=np.uint8)
        