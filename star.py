import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """A class representing a star"""

    def __init__(self, settings, screen):
        """Initialize and set start position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = settings
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
