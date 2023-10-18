import pygame as pg

class Window:
    def __init__(self, app_config):
        self.app_config = app_config
        self.width, self.height = self.app_config.get('ScreenDim')
        self.g_padding = self.app_config.get('GUIPadding')

        pg.init()
        pg.display.set_caption(self.app_config.get('Title'))
        self.display: pg.Surface = pg.display.set_mode([self.width, self.height + self.g_padding])
        
    def get_screen(self):
        return self.display
