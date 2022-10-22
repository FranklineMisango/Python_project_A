import pygame
import sys
from settings import Settings
from ship import Ship

class AlienInvasion:
    #Class to manage the game assets and behaviour

    def __init__(self):
        pygame.init()
        self.settings = Settings() #Import screen definition from the settings py

        #Game init and the resources

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #set background color

        self.bg_color = (230,230,230)

        self.ship = Ship(self) #The ship class called
    def run_game(self):
        #Starting the main loop for the game
        while True:
            #Check the keyboard and mouse events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #Redraw the screen during each pass with bg:

            self.screen.fill(self.settings.bg_color)
            self.ship.blitme() #Define the location of the ship in the midbottom range
           #Make the last display visible

            pygame.display.flip()

if __name__ == '__main___':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()        
