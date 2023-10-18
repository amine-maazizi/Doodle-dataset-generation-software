import pygame as pg

from gui.gui_element import GUIElement

class GUIContainer:
    
    def __init__(self, *args, **kwargs) -> None:
        self.container = []

        for arg in args:
            if isinstance(arg, GUIElement):
                self.container.append(arg)
            else:
                raise TypeError(f"GUICONTAINER: Expected an instance of GUIElement, but got {type(arg)}")

        for _, value in kwargs.items():
            if isinstance(value, GUIElement):
                self.container.append(value)
            else:
                raise TypeError(f"GUICONTAINER: Expected an instance of GUIElement, but got {type(value)}")

    def get(self, index):
        if 0 <= index < len(self.container):
            return self.container[index]
        else:
            raise IndexError(f"GUICONTAINER: Index out of range")

    def append(self, element):
        if isinstance(element, GUIElement):
            self.container.append(element)
        else:
            raise TypeError(f"GUICONTAINER: Expected an instance of GUIElement, but got {type(element)}")

    def remove(self, index):
        if 0 <= index < len(self.container):
            del self.container[index]
        else:
            raise IndexError(f"GUICONTAINER: Index out of range")

    def render(self, display: pg.Surface) -> None:
        for element in self.container:
            element.render(display)
            
    def handle_events(self, event) -> None:
        for element in self.container:
            element.handle_events(event)
    
    def get_focused(self) -> bool:
        return any([element.get_focused() for element in self.container])
    