import pygame as pg
from pygame.locals import *
import numpy as np

class Canvas:
    """Canvas for drawing on a Pygame surface."""

    def __init__(self, config: dict) -> None:
        """Initialize the Canvas."""
        self.arr_w, self.arr_h = config.get('ImageSize')
        self.win_w, self.win_h = config.get('ScreenDim')
        self.canvas_array: np.ndarray = np.zeros((self.arr_w, self.arr_h, 3), dtype=np.uint8)
        
    def process(self, dt: float) -> None:
        """Process user input to draw on the canvas."""
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
        """Render the canvas on the display surface."""
        base_surface = pg.surfarray.make_surface(self.canvas_array)
        scaled_surface = pg.transform.scale(base_surface, (self.win_w, self.win_h))
        display.blit(scaled_surface, (0, 0))

    def get_canvas_array(self) -> np.array:
        """Get the canvas array."""
        return self.canvas_array
    
    def get_canvas_dimensions(self) -> (int, int):
        """Get the dimensions of the canvas."""
        return self.arr_w, self.arr_h
    
    def clear_canvas(self) -> None:
        """Clear the canvas by setting all pixels to black."""
        self.canvas_array = np.zeros((self.arr_w, self.arr_h, 3), dtype=np.uint8)
