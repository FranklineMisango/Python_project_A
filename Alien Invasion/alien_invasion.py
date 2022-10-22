import pygame
import sys
from settings import Settings
from ship import Ship


class AlienInvasion:
    #Class to manage the game assets and behaviour

    def __init__(self):
        pygame.init()
        self.settings = Settings() #import from settings file
       
        #Game init and the resources
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) #import from the ship file 
        #set the background color

        self.bg_color = (230,230,230)


    def run_game(self):
        #Starting the main loop for the game
        while True:
            #Check the keyboard and mouse events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #Redraw the screen during each pass with bg:
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme() #redraw the ship graphic at the midbottom screen
            #Redraw the screen during each pass through the loop
            
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()        
