class GameStats:

    #Track the statistics for alien_invasion
    def __init__(self , ai_game):
        #Initialize the statistics
        self.settings = ai_game.settings
        self.reset_stats()
        #High score should never be reset
        self.high_score = 0
    

    def reset_stats(self):
        #Initialize the stats that can change during the game 
        self.ships_left = self.settings.ship_limit
        #Start Alien Invasion in an Inactive state.
        self.game_active = False
        #Scores
        self.score = 0
        self.level = 1

        