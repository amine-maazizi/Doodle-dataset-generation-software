import pygame as pg
from pygame.locals import *
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import sys
import json
import time
from PIL import Image
import numpy as np
import pandas as pd

from canvas import Canvas
from gui.gui_container import GUIContainer
from gui.input_entry import InputEntry
from gui.check_button import CheckButton


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

        self.dataset_dir = self.clear_dataset()

        pg.init()

        self.width, self.height = Application.config['ScreenDim']
        self.g_padding = Application.config['GUIPadding']
        pg.display.set_caption(self.config['Title'])
        self.display: pg.Surface = pg.display.set_mode([self.width, self.height + self.g_padding])
        self.clock: pg.time.Clock = pg.time.Clock()
        
        self.img_w, self.img_h = Application.config['ImageSize']
        self.canvas = Canvas(Application.config, self.img_w, self.img_h)
        self.index = 0
        
        self.datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        self.label_entry = InputEntry(5, self.height, 100, 20)
        self.datagen_checkbutton = CheckButton(self.width - 130, self.height, 100, 20, text='Activate ImgDataGen')
        self.gui_container = GUIContainer(self.label_entry, self.datagen_checkbutton)
        
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
        self.gui_container.render(self.display)

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
                self.gui_container.handle_events(ev)
                if ev.type == KEYDOWN and not self.gui_container.get_focused():
                    if ev.key == K_RETURN:
                        self.on_submit()
                    if ev.key == K_BACKSPACE:
                        self.canvas.clear_canvas()

            if dt:
                self.process(dt)
            self.render()

            dt, last_time = time.time() - last_time, time.time()
            pg.display.update()
            self.clock.tick(self.config['FPS'])

    def clear_dataset(self) -> str:
        dataset_dir = Application.config['DatasetDir']
        if os.path.exists(dataset_dir):
            file_list = os.listdir(dataset_dir)
            for filename in file_list:
                file_path = os.path.join(dataset_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(dataset_dir)
        return dataset_dir

    def on_submit(self) -> None:
        original_arr = self.canvas.get_canvas_array()
        image = Image.fromarray(original_arr)
        label = self.label_entry.get_entry()
        label = label if label else '0'

        if self.datagen_checkbutton.get_pressed():
            n = Application.config['NumberOfVersion']
            for i in range(n):  # Save n augmented versions
                transformed_arr = self.datagen.random_transform(original_arr)
                image = Image.fromarray(np.fliplr(np.rot90(transformed_arr, k=3)))
                image.save(os.path.join(self.dataset_dir, f'{self.index}_var_{i+1}.png'))

                if label:
                    self.data = pd.concat([self.data, pd.DataFrame({'img_file': [f'{self.index}_var_{i+1}.png'], 'label': [label]})], ignore_index=True)

        # Save the original doodle
        transformed_arr = np.fliplr(np.rot90(original_arr, k=3))
        image = Image.fromarray(transformed_arr)
        image.save(os.path.join(self.dataset_dir, f'{self.index}.png'))

        if label:
            self.data = pd.concat([self.data, pd.DataFrame({'img_file': [f'{self.index}.png'], 'label': [label]})], ignore_index=True)

        self.index += 1