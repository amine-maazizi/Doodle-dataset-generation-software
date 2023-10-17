import pygame as pg
from pygame.locals import *
import os
import sys
import json
import time
from PIL import Image
import numpy as np
import pandas as pd

from canvas import Canvas
from input_entry import InputEntry


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

        self.width, self.height = Application.config['ScreenDim']
        self.g_padding = Application.config['GUIPadding']
        pg.display.set_caption(self.config['Title'])
        self.display: pg.Surface = pg.display.set_mode([self.width, self.height + self.g_padding])
        self.clock: pg.time.Clock = pg.time.Clock()
        
        self.canvas = Canvas(Application.config, 28, 28)
        self.label_entry = InputEntry(5, self.height, 100, 20)
        self.index = 0
        
        self.data = pd.DataFrame(columns=['img_file', 'label'])

    def process(self, dt: float) -> None:
        """
        Process the application's logic based on the time step 'dt'.
        """        
        self.canvas.process(dt)
    

    def render(self) -> None:
        """
        Render the application's graphical components.
        """
        self.canvas.render(self.display)
        self.label_entry.render(self.display)

    def launch(self) -> None:
        """
        Start the main application loop.
        """
        dt, last_time = 0.0, time.time()
        while True:
            events = pg.event.get()
            for ev in events:
                if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    self.data.to_csv(self.dataset_dir + '\data.csv', index=False)
                    pg.quit()
                    sys.exit()
                if (ev.type == KEYDOWN and ev.key == K_RETURN):
                       self.on_submit()
                self.label_entry.handle_events(ev)

            if dt:
                self.process(dt)
            self.render()

            dt, last_time = time.time() - last_time, time.time()
            pg.display.update()
            self.clock.tick(self.config['FPS'])

    def on_submit(self) -> None:
        transformed_arr = np.fliplr(np.rot90(self.canvas.get_canvas_array(), k=3))
        image = Image.fromarray(transformed_arr)
        image.save(f'{self.dataset_dir}/{self.index}.png')   
        
        label = self.label_entry.get_entry()
        label = label if label else '0'
        if label:
            self.data = pd.concat([self.data, pd.DataFrame({'img_file': [f'{self.index}.png'], 'label': [label]})], ignore_index=True)
            
        self.index += 1  