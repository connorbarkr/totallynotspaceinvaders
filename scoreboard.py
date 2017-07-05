import pygame.font
from pygame.sprite import Group

from life import Heart

class Scoreboard():
    """A class to represent the score information"""

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = ai_settings
        self.stats = stats

        #font text settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 48)

        self.prep_score()
        self.prep_lives()
        self.prep_high_score()

    def prep_score(self):
        """turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str = "Score: " + str(score_str)
        self.score_image = self.font.render(score_str, True,
            self.text_color, self.settings.bg_color)

        #display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """turn the high score into a rendered image"""
        rounded_hscore = int(round(self.stats.high_score, -1))
        hscore_str = "{:,}".format(rounded_hscore)
        hscore_str = "High score: " + str(hscore_str)
        self.hscore_image = self.font.render(hscore_str, True,
            self.text_color, self.settings.bg_color)

        #display the score at the top right of the screen
        self.hscore_rect = self.hscore_image.get_rect()
        self.hscore_rect.centerx = self.screen_rect.centerx
        self.hscore_rect.top = 20

    def prep_lives(self):
        """Display lives remaining"""
        self.lives = Group()
        for life_number in range(self.stats.ships_left + 1):
            life = Heart(self.settings, self.screen)
            life.rect.x = 10 + life_number * life.rect.width
            life.rect.y = 10
            life.rescale(50, 50)
            self.lives.add(life)

    def show_score(self):
        """Draw score to screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hscore_image, self.hscore_rect)

    def show_lives(self):
        """Draw lives to screen"""
        self.lives.draw(self.screen)
