import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #Class that manages the bullets fired from the ship

    def __init__(self, ai_game):
        #create the bullet object at the ship current position
        super().__init__() #inherited from sprite to group bullets together and act on them all at once
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        #create a bullet at rect (0,0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,self.settings.bullet_height) #rectangle the bullets as we dont use images
        self.rect.midtop = ai_game.ship.rect.midtop #make bullets appear as if they are coming from the top of the ship

        #store the bullet's position as a decimal value
        self.y = float(self.rect.y)
    def update(self):
        #move the bullet upscreen to attack aliens
        #update the moving position of the bullet
        self.y -= self.settings.bullet_speed
        #update the rect position
        self.rect.y = self.y
    def draw_bullet(self):
        #draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)