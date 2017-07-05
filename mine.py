import pygame
from pygame.sprite import Sprite

class Mine(Sprite):

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/mine.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.centery = ship.rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
