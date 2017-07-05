import sys
import pygame

from random import randint
from time import sleep

from bullet import Bullet
from alien import Alien
from star import Star
from mine import Mine

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sb.prep_lives()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(1)

def check_keydown_events(stats, event, ai_settings, screen, ship,
    bullets, aliens, mines, sb):
    """Respond to keypresses."""
    if event.key == 275:
        ship.moving_right = True
    elif event.key == 276:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_RETURN:
        start_game(ai_settings, stats, aliens, bullets, screen, ship,
            sb)
    elif event.key == 303:
        drop_mine(ai_settings, screen, ship, mines)


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == 275:
        ship.moving_right = False
    elif event.key == 276:
        ship.moving_left = False
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_events(ai_settings, screen, ship, bullets, stats,
    play_button, aliens, mines, sb):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(stats, event, ai_settings, screen,
            ship, bullets, aliens, mines, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,
                aliens, bullets, ai_settings, screen, ship, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens,
    bullets, ai_settings, screen, ship, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(ai_settings, stats, aliens, bullets, screen, ship,
            sb)

def update_screen(ai_settings, screen, ship, aliens, stars, bullets,
    stats, play_button, scoreboard, mines):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for mine in mines.sprites():
        mine.blitme()
    stars.draw(screen)
    ship.blitme()
    scoreboard.show_score()
    scoreboard.show_lives()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_weapons(bullets, aliens, stats, ai_settings, scoreboard,
    mines):
    #get rid of disappeared bullets
    bullets.update()
    mines.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_alien_weapon_collisions(bullets, aliens, stats, ai_settings,
        scoreboard, mines)

def check_alien_weapon_collisions(bullets, aliens, stats, ai_settings,
        scoreboard, mines):
    bcollisions = pygame.sprite.groupcollide(bullets, aliens, True,
        True)
    mcollisions = pygame.sprite.groupcollide(mines, aliens, True,
        True)
    if bcollisions:
        for aliens in bcollisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if mcollisions:
        for aliens in mcollisions.values():
            ai_settings.mine_limit -= 1
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets,
        sb):
    """
    Check if fleet is at an edge, and update all positions in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens,
        bullets, sb)
    check_aliens_remaining(ai_settings, screen, bullets, ship, aliens)

    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens,
    bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def drop_mine(ai_settings, screen, ship, mines):
    #create a new mine and add it to the group of mines
    if len(mines) < ai_settings.mine_limit:
        new_mine = Mine(ai_settings, screen, ship)
        mines.add(new_mine)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine how many rows of aliens fit on the screen"""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - alien_width
    return int(available_space_x / (alien_width * 2))

def create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                alien_width, row_number)

def check_aliens_remaining(ai_settings, screen, bullets, ship, aliens):
    if len(aliens) == 0:
        ai_settings.increase_speed()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #pause
        sleep(0.5)

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change its direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """Respond if aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def create_star(ai_settings, screen, stars, row_number, star_number, offset):
    star = Star(ai_settings, screen)
    x_box = screen.get_width() / ai_settings.star_numbers
    y_box = screen.get_height() / ai_settings.star_rows
    star.rect.x = ((x_box * star_number) + (0.5 * x_box) +
                    randint(-offset, offset))
    star.rect.y = ((y_box * row_number) + (0.5 * y_box) +
                    randint(-offset, offset))
    stars.add(star)

def create_constellation(ai_settings, screen, stars):
    rows = ai_settings.star_rows
    cols = ai_settings.star_numbers
    offset = ai_settings.offset
    for row_number in range(rows):
        for star_number in range(cols):
            create_star(ai_settings, screen, stars, row_number, star_number,
                            offset)

def check_high_score(stats, sb):
    """Check to see if the high score needs resetting"""
    if stats.score > stats.high_score:
        filename = 'highscore'
        with open(filename, 'w') as file_object:
            file_object.write(str(stats.score))
        stats.update_highscore()
        sb.prep_high_score()

def start_game(ai_settings, stats, aliens, bullets, screen, ship, sb):
    if not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(0)
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_lives()
