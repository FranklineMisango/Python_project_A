import pygame 

class Ship:

    #Manage the ship

    def __init__(self, ai_game):
        #Initialize ship and its starting class
        
        self.screen = ai_game.screen
        self.screen = ai_game.screen.get_rect()

        #Load the ship image and get its rect.

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom of the screen

        self.rect.midbottom =  self.screen_rect.midbottom
    def blitme(self):
        #Draw the ship at its current location

        self.screen.blit(self.image,self.rect)