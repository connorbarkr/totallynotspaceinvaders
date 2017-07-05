import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

def run_game():

    #Initialize game, setings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #make a play button
    play_button = Button(ai_settings, screen, "Play")
    #make a ship
    ship = Ship(ai_settings, screen)
    #make a bullet group
    bullets = Group()
    #make an alien group
    aliens = Group()
    #make a star group
    stars = Group()
    #make a mine group
    mines = Group()

    #make a fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #make the stars
    gf.create_constellation(ai_settings, screen, stars)

    #initialize stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats,
            play_button, aliens, mines, sb)
        if stats.game_active:
            ship.update()
            gf.update_weapons(bullets, aliens, stats, ai_settings, sb,
                mines)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens,
                bullets, sb)

        gf.update_screen(ai_settings, screen, ship, aliens, stars,
            bullets, stats, play_button, sb, mines)

run_game()
