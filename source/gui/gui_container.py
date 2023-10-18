import pygame as pg
from gui.gui_element import GUIElement

class GUIContainer:
    """Container for GUI elements."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the GUI container."""
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
        """Get a GUIElement by index."""
        if 0 <= index < len(self.container):
            return self.container[index]
        else:
            raise IndexError(f"GUICONTAINER: Index out of range")

    def append(self, element):
        """Add a GUIElement to the container."""
        if isinstance(element, GUIElement):
            self.container.append(element)
        else:
            raise TypeError(f"GUICONTAINER: Expected an instance of GUIElement, but got {type(element)}")

    def remove(self, index):
        """Remove a GUIElement by index."""
        if 0 <= index < len(self.container):
            del self.container[index]
        else:
            raise IndexError(f"GUICONTAINER: Index out of range")

    def render(self, display: pg.Surface) -> None:
        """Render all GUI elements on the provided display."""
        for element in self.container:
            element.render(display)

    def handle_events(self, event) -> None:
        """Handle events for all GUI elements in the container."""
        for element in self.container:
            element.handle_events(event)

    def get_focused(self) -> bool:
        """Check if any element in the container is currently focused."""
        return any([element.get_focused() for element in self.container])
