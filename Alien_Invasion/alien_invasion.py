import pygame
import sys
from time import sleep

from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    #Class to manage the game assets and behaviour

    def __init__(self):
        #Game init and the resources
        pygame.init()
        #import from settings file
        self.settings = Settings()
        #For users who prefer full screen, comment the code below:)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        #Create an instance to store the game statistics and create a score board
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #import from the ship file 
        self.ship = Ship(self)
        #make the bullets be handled as a single group
        self.bullets = pygame.sprite.Group()
        #Import from the top aliens 
        self.aliens = pygame.sprite.Group()
        #Fleet of aliens
        self._create_fleet()
        #Make the play button
        self.play_button = Button(self, "Play")
        #set the background color
        self.bg_color = (230,230,230)
        
        

    def run_game(self):
        #Starting the main loop for the game
        while True:
            self._check_events()  # User keys anything and it does some commands 
            if self.stats.game_active :
                self.ship.update() #update the ship position 
                self.bullets.update()#update the bullets with each call for a single bullet
                self.update_aliens()#Updating the aliens
                self._update_bullets()
            self._update_screen() #update the screen each time
            
            
    def _check_events(self):
         #Check the keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):        
        #Start a new game when the player clicks play\
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()

            #Reset the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

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
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #Respond to bullet-alien collisions and remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets , self.aliens , True , True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        #Check for any bullets that hit the aliens, if so, get rid of them
        if not self.aliens:
            #Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        #Create the fleet of aliens and find the number of aliens able to fit/row
        #spacing between aliens should be equal to one alien_Width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_X = self.settings.screen_width - (2 * alien_width)
        number_aliens_x =  available_space_X // (2 * alien_width)

        #Determining the no of rows that can fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height)- ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create a full fleet of aliens that fit the screen

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): #create the first row of aliens
                self._create_alien(alien_number , row_number)
        
    def _create_alien(self,alien_number,row_number):
        #create an alien and place in first row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
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
        #Draw the score information
        self.sb.show_score()
        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()#Redraw the screen during each pass through the loop

    def update_aliens(self):
        #Check of the fleet has hit the edge and Updates the positions of the aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()
        #Look for collisions in alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom
    
    def _check_fleet_edges(self):
        #Respond appropriately if any aliens reach the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #Dropping the entire fleet and changing the fleet direction 
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        if self.stats.ships_left > 0:
            #Decrements the ships left and updates the score board
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause the game
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        #Check if aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites:
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship had gotten hit
                self._ship_hit()
                break


if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()        
