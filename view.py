import yaml
import pygame
class Screen:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def from_yaml(file):
        with open(file, "r") as f:
            config = yaml.safe_load(f)
            return Screen(**config)
    def get_pygame_screen(self):
        return pygame.display.set_mode((self.width, self.height))