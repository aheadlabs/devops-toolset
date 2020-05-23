import os
import json

class Settings(object):
    """Application settings"""

    def __init__(self):
        self.load()

    def read_settings_from_file(self):
        """Loads settings from settings.json"""
        
        current_path = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(current_path, "settings.json"), "r") as settings_file:
            settings = json.load(settings_file)

        return settings

    def load(self):
        """Assings settings"""
        
        settings = self.read_settings_from_file()

        # Add your setting mappings here
        self.language = settings["language"]
