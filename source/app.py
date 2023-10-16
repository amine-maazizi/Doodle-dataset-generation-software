import pygame as pg
from pygame.locals import *
import os
import sys
import json
import time
from PIL import Image

from canvas import Canvas


class Application:
    instance = None  
    config: dict = None

    def __new__(cls: type):
        """
        Create a new instance of the Application class if it doesn't already exist.
        """
        if not cls.instance:
            cls.instance = super(Application, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """
        Initialize the Application object.
        """
        with open('./config/config.json') as f:
            Application.config = json.load(f)

        self.dataset_dir = Application.config['DatasetDir']
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)

        pg.init()

        pg.display.set_caption(self.config['Title'])
        self.display: pg.Surface = pg.display.set_mode([self.config['Width'], self.config['Height']])
        self.clock: pg.time.Clock = pg.time.Clock()
        
        self.canvas = Canvas(self.display, 28, 28)
        self.index = 0

    def process(self, dt: float) -> None:
        """
        Process the application's logic based on the time step 'dt'.
        """        
        self.canvas.process(dt)
    

    def render(self) -> None:
        """
        Render the application's graphical components.
        """
        self.canvas.render()

    def launch(self) -> None:
        """
        Start the main application loop.
        """
        dt, last_time = 0.0, time.time()
        events = pg.event.get()
        while True:
            for ev in events:
                if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if (ev.type == KEYDOWN and ev.key == K_RETURN):
                    image = Image.fromarray(self.canvas.get_canvas_array())
                    image.save(f'{self.dataset_dir}/{self.index}.png')   
                    self.index += 1     

            if dt:
                self.process(dt)
            self.render()

            dt, last_time = time.time() - last_time, time.time()
            pg.display.update()
            self.clock.tick(self.config['FPS'])
