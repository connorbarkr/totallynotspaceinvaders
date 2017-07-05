class Settings():
    """A class to store settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #ship settings
        self.ship_limit = 3

        #mine settings
        self.mine_limit = 3

        #bullet settings
        self.bullet_width = 7
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #alien settings
        self.fleet_drop_speed = 20
        self.alien_points = 10

        #star settings
        self.star_rows = 6
        self.star_numbers = 8
        self.offset = 200
        self.scale_limit = 3

        #speedup settings
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialise settings that change throughout the game"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 15
        self.alien_speed_factor = 10
        self.fleet_direction = 1 #right

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= (self.speedup_scale)
