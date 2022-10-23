import pygame 

class Ship:

    #Manage the ship

    def __init__(self, ai_game):
        #Initialize ship and its starting class
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() #converts the screen from alien invasion to a rectangle object
        self.settings = ai_game.settings #Init to dicate the ship speed


        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() #converts the image to a rect for easy handling in "pygame"

        #start each new ship at the bottom of the screen
        self.rect.midbottom =  self.screen_rect.midbottom

        #store a decimal value position for the ship position cause rect uses int and might ignore the decimal 
        self.x = float(self.rect.x)

        #moving flags
        self.moving_left= False
        self.moving_right = False

    def update(self):
        #update the ship position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right: #the ship not to move outside the right side screen range
            self.x += self.settings.ship_speed   
        if self.moving_left and self.rect.left > 0 : #limit to the left side to keep ship in range 
            self.x -= self.settings.ship_speed
        #update the rect object from self.x
        self.rect.x = self.x
    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image,self.rect)