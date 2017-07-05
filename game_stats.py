class GameStats():
    """Track stats for alien invader"""

    def __init__(self, ai_settings):
        """Initialize stats"""
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        self.update_highscore()

    def update_highscore(self):
        filename = 'highscore'
        unsplit_contents = ''
        with open(filename) as file_object:
            unsplit_contents = file_object.read()
            s_contents = unsplit_contents.split(".", 1)[0]
        self.high_score = int(str(s_contents))

    def reset_stats(self):
        """Initialize stats that can be changed during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.mines_left = self.ai_settings.mine_limit
        self.score = 0
