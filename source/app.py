import pygame as pg
from pygame.locals import *
import sys
import time
from PIL import Image
import numpy as np

from window import Window
from canvas import Canvas
from config_manager import Config
from data_handler import DataHandler
from data_augmentation import DataAugmentation

from gui.gui_container import GUIContainer
from gui.input_entry import InputEntry
from gui.check_button import CheckButton

class Application:
    instance = None

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
        self.config = Config('./config/config.json')
        self.datahandler = DataHandler('./dataset')
        self.datahandler.clear_dataset()

        self.window_manager = Window(self.config)
        self.clock: pg.time.Clock = pg.time.Clock()

        self.canvas = Canvas(self.config)
        self.index = 0

        self.datagen = DataAugmentation(self.config)

        self.width, self.height = self.config.get('ScreenDim')
        self.label_entry = InputEntry(5, self.height + 2, 100, 20)
        self.datagen_checkbutton = CheckButton(self.width - 175, self.height + 2, 100, 20, text='Activate Data Augmentation')
        self.gui_container = GUIContainer(self.label_entry, self.datagen_checkbutton)

    def process(self, dt: float) -> None:
        """
        Process the application's logic based on the time step 'dt'.
        """
        self.canvas.process(dt)

    def render(self) -> None:
        """
        Render the application's graphical components.
        """
        self.canvas.render(self.window_manager.get_screen())
        self.gui_container.render(self.window_manager.get_screen())

    def launch(self) -> None:
        """
        Start the main application loop.
        """
        dt, last_time = 0.0, time.time()
        while True:
            events = pg.event.get()
            for ev in events:
                if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                    self.datahandler.save_to_csv()
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
            self.clock.tick(self.config.get('FPS'))

    def on_submit(self) -> None:
        original_arr = self.canvas.get_canvas_array()
        image = Image.fromarray(original_arr)
        label = self.label_entry.get_entry()
        label = label if label else '0'

        if self.datagen_checkbutton.get_pressed():
            augmented_data = self.datagen.apply_data_augmentation(original_arr)
            for i, transformed_arr in enumerate(augmented_data):
                image = Image.fromarray(np.fliplr(np.rot90(transformed_arr, k=3)))
                self.datahandler.save_img(image, f'{self.index}_var_{i+1}.png')
                self.datahandler.add_to_dataset({'img_file': [f'{self.index}_var_{i+1}.png'], 'label': [label]})

        # Save the original doodle
        transformed_arr = np.fliplr(np.rot90(original_arr, k=3))
        image = Image.fromarray(transformed_arr)
        self.datahandler.save_img(image, f'{self.index}.png')
        self.datahandler.add_to_dataset({'img_file': [f'{self.index}.png'], 'label': [label]})
        self.index += 1
