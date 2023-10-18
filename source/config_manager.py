import json

class Config:
    """Configuration manager for loading and accessing JSON configuration files."""

    def __init__(self, path: str):
        """Initialize the configuration manager by loading a JSON configuration file."""
        with open(path) as f:
            self.config = json.load(f)

    def get(self, key, default=None):
        """Get the value associated with a key from the configuration, with an optional default value."""
        return self.config.get(key, default)
