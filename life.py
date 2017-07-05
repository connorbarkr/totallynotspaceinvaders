import pygame

from pygame.sprite import Sprite

class Heart(Sprite):

    def __init__(self, settings, screen):
        """initialize settings"""
        super().__init__()
        self.image = pygame.image.load('images/life.bmp')
        self.rect = self.image.get_rect()

        self.settings = settings
        self.screen = screen

    def rescale(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
