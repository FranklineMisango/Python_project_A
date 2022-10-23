import pygame
import sys
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:
    #Class to manage the game assets and behaviour

    def __init__(self):
        pygame.init()
        self.settings = Settings() #import from settings file
        #Game init and the resources
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #For users who prefer full screen, comment the code below:)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) #import from the ship file 
        self.bullets = pygame.sprite.Group() #make the bullets be handled as a single group
        self.aliens = pygame.sprite.Group()#Import from the top aliens
        self._create_fleet() #Fleet of aliens
        #set the background color
        self.bg_color = (230,230,230)

    def run_game(self):
        #Starting the main loop for the game
        while True:
            self._check_events()  # User keys anything and it does some commands 
            self.ship.update() #update the ship position 
            self.bullets.update()#update the bullets with each call for a single bullet
            self._update_screen() #update the screen each time
            self._update_bullets()
            

    def _check_events(self):
         #Check the keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        #Respond to the key presses
        if event.key == pygame.K_RIGHT:
            #Move the ship to the Right by 1
            self.ship.moving_right = True #check ship class that moves it right/left by 1
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: #Quit game
            sys.exit()
        elif event.key == pygame.K_SPACE:#space bar pressed -"Fire" a bullet 
            self._fire_bullet()

    def _check_keyup_events(self,event):
        #Respond to key releases
        if event.key == pygame.K_RIGHT: #when player release the right key / left key, respond to up events and set "moving right" to false
            self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #create a bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        #update the positions of the bullets and rid the old bullets
        #update bullet positions
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)   
    def _create_fleet(self):
        #Create the fleet of aliens and find the number of aliens able to fit/row
        #spacing between aliens should be equal to one alien_Width
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_X = self.settings.screen_width - (2 * alien_width)
        number_aliens_x =  available_space_X // (2 * alien_width)
        for alien_number in range(number_aliens_x): #create the first row of aliens
            self._create_alien(alien_number)
    
    def _create_alien(self,alien_number):
        #create an alien and place in first row
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        self.aliens.add(alien)  
            
    def _update_screen(self):
        #update the image and the screen
         #Redraw the screen during each pass with bg:
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme() #redraw the ship graphic at the midbottom screen
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            #Redraw the screen during each pass through the loop
            self.aliens.draw(self.screen) #call aliens before screen reconfiguration

            pygame.display.flip()#Redraw the screen during each pass through the loop
if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()        
