import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #Class to represent a single alien in the fleet

    def __init__(self, ai_game):
        #initialize the alien and set its starting position
        super().__init__()
        self.screen = ai_game.screen
        #Load the alien image and set its rect image
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alien's exact horizontal position
        self.x = float(self.rect.x)