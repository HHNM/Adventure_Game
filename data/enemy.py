import os 
import pygame
from pygame.locals import *
import random
from data.settings import *
from data.tools import *
from data.ui import Leaf, HealthBar, Coin, Bubble, Seed


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x, y, j, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 20
        self.max_health = self.health
        self.direction = 1
        self.attacking = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.vel_y = 0
        self.in_air = True
        self.alpha = 255
        self.j = j
        self.ball = None
        self.dead = False
        self.move_counter = 0
        self.ball_collusion = False
        self.vision1 = pygame.Rect(0, 0, 300, 20)
        self.vision2 = pygame.Rect(0, 0, 300, 20)
        self.idling = False
        self.idling_counter = 0
        self.update_time = pygame.time.get_ticks()
        # load all images for the player
        animation_types = ['Idle', 'Walk', 'Die']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/Enemy{j}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/Enemy{j}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self,world, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y


        for tile in world.obstacle_list:
            # Check collisino in the x direction
            tile1 = tile[1].inflate(-40,-40)
            if tile1.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
        # Check collision in the y direction
            if tile1.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the ground, i.e. falling
                self.vel_y = 0
                    
                dy = tile1.top - self.rect.bottom

        self.rect.x += dx 
        self.rect.y += dy

    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)
    
    def update_action(self,new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)  

    def ai(self, player, world):
        self.vision1.center = (self.rect.centerx -170, self.rect.centery)
        self.vision2.center = (self.rect.centerx +170, self.rect.centery)
        self.move(world, moving_left,moving_right)
        if self.alive and player.alive:
            if self.rect.colliderect(player.rect):
                player.health -= 0.1 
            for ball in ball_group:
                if ball.rect.colliderect(self.rect):
                    self.ball_collusion = True
                    self.ball = ball
                    
            if self.ball_collusion == True:
                self.ball.update_action(1)          
                ai_moving_left = False
                ai_moving_right = False
                self.move(world, ai_moving_left, ai_moving_right)
                self.update_action(0)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
                    self.ball.update_action(0)

            elif self.vision1.colliderect(player.rect):
                self.direction == -1
                ai_moving_left = True
                ai_moving_right = False
                self.move(world, ai_moving_left, ai_moving_right)
                self.update_action(1)
            elif self.vision2.colliderect(player.rect):
                self.direction == 1
                ai_moving_left = False
                ai_moving_right = True
                self.move(world, ai_moving_left, ai_moving_right)
                self.update_action(1)
                
            else:
                self.move(world, False, False)
                self.update_action(0)
            
    def update(self, screen_scroll):
        self.update_animation()
        self.check_alive()
        self.rect.x += screen_scroll   
        

          

class Enemy2(Enemy):
    def __init__(self,x, y, j, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 25
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.attacking = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.throw_cooldown = 0
        self.ball = None
        self.ball_collusion = False
        self.alpha = 255
        self.hit_balls = 0
        self.ball_set = set()
        self.j = j
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 500, 20)
        self.idling = False
        self.idling_counter = 0

        # load all images for the player
        animation_types = ['Idle', 'Walk', 'Die', 'Hurt']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/Enemy{j}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/Enemy{j}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1
        

    def throw_leaf(self):
        if self.throw_cooldown == 0 :
            self.throw_cooldown = 150
            leaf = Leaf(self, self.rect.centerx, self.rect.centery , self.direction,0.5)
            attack_group.add(leaf)
            self.update_action(0)
            

    def ai(self, player, world, screen_scroll):
        
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            for ball in ball_group:
                if ball.rect.colliderect(self.rect):
                    self.ball_set.add(ball)
                if len(self.ball_set) == 2:
                    self.ball_collusion = True
                    self.ball = ball
                    
            if self.ball_collusion == True:
                self.ball.update_action(1)          
                ai_moving_left = False
                ai_moving_right = False
                self.move(world, ai_moving_left, ai_moving_right)
                self.update_action(0)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
                    self.ball.update_action(0)
			#check if the ai in near the player
            elif self.vision.colliderect(player.rect):
				#stop running and face the player
                self.update_action(0)#0: idle
				#shoot
                self.throw_leaf()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(world, ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    
                    self.move_counter += 1
					#update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 250 * self.direction, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
        self.rect.x += screen_scroll
        self.vision.x += screen_scroll


class Bird(Enemy):
    # no need for other class for enemy maybe add 
    # a condition for the j that represents the id
    # of the  enemy
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.moving_left = False
        self.moving_right = False
        self.health = 25
        self.max_health = self.health
        self.direction = 1
        self.attacking = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.move_counter = 0
        self.vision1 = pygame.Rect(0, 0, 400, 800)
        self.vision2 = pygame.Rect(0, 0, 400, 800)
        self.idling = False
        self.idling_counter = 0
        self.alpha = 255
        self.hit_balls = 0
        self.ball_collusion = False
        self.ball_set = set()
        self.update_time = pygame.time.get_ticks()
        # load all images for the player
        animation_types = ['Fly', 'Attack', 'Die']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/Bird/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/Bird/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):

        dx = 0
        dy = 0

        if self.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        self.rect.x += dx
        self.rect.y += dy

    def move_towards_player(self, player):
        if player.rect.x > self.rect.x :
            self.rect.x += self.speed
        if player.rect.x < self.rect.x :
            self.rect.x -= self.speed
        if player.rect.y > self.rect.y :
            self.rect.y += self.speed
        if player.rect.y < self.rect.y :
            self.rect.y -= self.speed

    def ai(self, player):
        self.vision1.center = (self.rect.centerx -230, self.rect.bottom)
        self.vision2.center = (self.rect.centerx +230, self.rect.bottom)
        self.moving_left = False
        self.moving_right = False
        if self.alive and player.alive:
            if self.rect.colliderect(player.rect):
                player.health -= 0.2
            for ball in ball_group:
                if ball.rect.colliderect(self.rect):
                    self.ball_set.add(ball)
                if len(self.ball_set) == 4:
                    self.ball_collusion = True
                    self.ball = ball
                    
            if self.ball_collusion == True:
                self.ball.update_action(1)         
                self.update_action(0)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
                    self.ball.update_action(0)
            if self.vision1.colliderect(player.rect):
                self.flip = True
                self.move_towards_player(player)
                self.update_action(1)
            elif self.vision2.colliderect(player.rect):
                self.flip = False
                self.move_towards_player(player)
                self.update_action(1)
                
            else:
                self.move()
                self.update_action(0)

    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def update(self, screen_scroll):
        self.update_animation()
        self.check_alive()
        self.rect.x += screen_scroll


          
class Flower(Enemy):
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 30
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.attacking = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.throw_cooldown = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.ball = False
        self.vision1 = pygame.Rect(0, 0, 500, 20)
        self.vision2 = pygame.Rect(0, 0, 500, 20)
        self.idling = False
        self.idling_counter = 0
        self.alpha = 255
        self.hit_balls = 0
        self.ball_collusion = False
        self.ball_set = set()
        # load all images for the player
        animation_types = ['Idle', 'Walk', 'Die', 'Hurt']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/Flower/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/Flower/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self, screen_scroll):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        self.rect.x += screen_scroll

    def throw_seed(self):
        if self.throw_cooldown == 0 :
            self.throw_cooldown = 100
            seed = Seed(self.rect.centerx, self.rect.centery , self.direction,0.5)
            attack_group.add(seed)
            self.update_action(0)
            

    def ai(self, player, world):
        self.vision1.center = (self.rect.centerx -270, self.rect.centery)
        self.vision2.center = (self.rect.centerx +270, self.rect.centery)
        self.move(world, moving_left, moving_right)

        if self.alive and player.alive:
            for ball in ball_group:
                if ball.rect.colliderect(self.rect):
                    self.ball_set.add(ball)
                if len(self.ball_set) == 3:
                    self.ball_collusion = True
                    self.ball = ball
                    
                    
            if self.ball_collusion == True:
                self.ball.update_action(1)         
                ai_moving_left = False
                ai_moving_right = False
                self.move(world, ai_moving_left, ai_moving_right)
                self.update_action(0)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
                    self.ball.update_action(0)
            elif self.vision1.colliderect(player.rect):
                self.direction == -1
                ai_moving_left = True
                ai_moving_right = False
                if abs(self.rect.centerx - player.rect.centerx) < 150:
                    ai_moving_left = False
                    self.update_action(0)
                self.move(world, ai_moving_left, ai_moving_right)
                self.throw_seed()
                self.update_action(1)
            elif self.vision2.colliderect(player.rect):
                self.direction == 1
                ai_moving_left = False
                ai_moving_right = True
                if abs(self.rect.centerx - player.rect.centerx) < 150:
                    ai_moving_right = False
                    self.update_action(0)
                self.move(world, ai_moving_left, ai_moving_right)
                self.throw_seed()
                self.update_action(1)
                
            else:
                self.update_action(0)
 
       
class Fish(Enemy):
    def __init__(self,x, y, j, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = 5
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.max_health = self.health
        self.direction = 1
        self.attacking = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.throw_cooldown = 0
        self.alpha = 255
        self.hit_balls = 0
        self.ball_collusion = False
        self.ball_set = set()
        self.update_time = pygame.time.get_ticks()

        # ai specific variables
        self.vision1 = pygame.Rect(0, 0, 300, 10)
        self.vision2 = pygame.Rect(0, 0, 300, 10)
        self.idling = False
        self.idling_counter = 0

        # load all images for the player
        animation_types = ['Idle', 'Attack', 'Die']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/Fish/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/Fish/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dy = 0
        
        if self.moving_up:
            dy = -self.speed
        
        if self.moving_down:
            dy = self.speed

        self.rect.y += dy
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2)
            self.moving_down = True
            self.move()
            if self.rect.top > SCREEN_HEIGHT + 10:
                self.speed = 0
                self.kill()

    def update(self, screen_scroll):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        self.rect.x += screen_scroll

    def spit_bubble(self):
        if self.throw_cooldown == 0 :
            self.throw_cooldown = 150
            bubble = Bubble(self.rect.centerx, self.rect.centery , self.direction,0.5)
            attack_group.add(bubble)
            self.update_action(0)
            

    def ai(self, player):
        self.vision1.center = (self.rect.centerx -170, self.rect.centery+10)
        self.vision2.center = (self.rect.centerx +170, self.rect.centery+10)
        if self.alive and player.alive:
            
            self.moving_up = True
            self.update_action(0)
            if self.rect.colliderect(player.rect):
                player.health -= 0.1  
            for ball in ball_group:
                if ball.rect.colliderect(self.rect):
                    self.ball_set.add(ball)
                if len(self.ball_set) == 2:
                    self.ball_collusion = True
                    self.ball = ball
                    
            if self.ball_collusion == True:
                self.ball.update_action(1)          
                self.moving_down = False
                self.moving_up = False
                self.move()
                self.update_action(0)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
                    self.ball.update_action(0)
            elif self.vision1.colliderect(player.rect):
                #self.moving_up, self.moving_down = False, False
                self.flip = False
                self.moving_left = True
                self.direction = -1
                self.spit_bubble()
                self.update_action(1)
            elif self.vision2.colliderect(player.rect):
                #self.moving_up, self.moving_down = False, False
                self.flip = True
                self.direction = 1
                self.spit_bubble()
                self.update_action(1)
            if self.rect.top < SCREEN_HEIGHT-150 and self.moving_up:
                self.moving_up = False
                self.moving_down = True
            if self.rect.top > SCREEN_HEIGHT+60 and self.moving_down:
                self.moving_up = True
                self.moving_down = False
            self.move()


class BigBird(Enemy):
    # no need for other class for enemy maybe add 
    # a condition for the j that represents the id
    # of the  enemy
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.moving_left = False
        self.moving_right = False
        self.health = 250
        self.max_health = self.health
        self.direction = 1
        self.attacking = False
        self.flip = False
        self.init_x = x
        self.init_y = y
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 40
        self.attack_counter = 40
        self.back = False
        self.move_to_player = False
        self.touchplayer = False
        self.coin_drawn = False
        self.alpha = 255
        self.coin_counter = 40
        self.healthbar_enemy = HealthBar(SCREEN_WIDTH - 160, 10, self.health, self.health)

        self.vision = pygame.Rect(0, 0, SCREEN_WIDTH-20, 800)
        self.update_time = pygame.time.get_ticks()
        # load all images for the player
        animation_types = ['Fly', 'Attack']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Enemy/BigBird/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Enemy/BigBird/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):

        dx = 0
        dy = 0

        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        if self.moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1

        self.rect.x += dx
        self.rect.y += dy

    def move_to(self, init_x, init_y):

        if init_x > self.rect.x :
            self.rect.x += self.speed
        if init_x < self.rect.x :
            self.rect.x -= self.speed
        if init_y > self.rect.y :
            self.rect.y += self.speed
        if init_y < self.rect.y :
            self.rect.y -= self.speed
        if self.rect.y + self.speed > init_y and self.rect.x + self.speed > init_x:
            self.back = True

    def move_towards_player(self, player):
            if player.rect.x > self.rect.x :
                self.rect.x += self.speed
            if player.rect.x < self.rect.x :
                self.rect.x -= self.speed
            if player.rect.y > self.rect.y :
                self.rect.y += self.speed
            if player.rect.y < self.rect.y :
                self.rect.y -= self.speed

    def move_to_topbranch(self):
        for branch in branch_group:

            if branch.rect.x - 20 > self.rect.x :
                self.rect.x += self.speed
            if branch.rect.x - 20 < self.rect.x :
                self.rect.x -= self.speed
            if branch.rect.y - 300 > self.rect.y :
                self.rect.y += self.speed
            if branch.rect.y - 300 < self.rect.y :
                self.rect.y -= self.speed
            if self.rect.y + self.speed > branch.rect.y - 300 and self.rect.x + self.speed > branch.rect.x - 20:
                self.back = True

            
    def ai(self, player,screen):
        self.vision.center = (self.rect.centerx -230, self.rect.bottom)
        self.moving_left = False
        self.moving_right = False
        self.back = False
        if self.alive and player.alive:
            if self.vision.colliderect(player.rect):
                self.healthbar_enemy.draw(self.health, screen)
                if self.touchplayer == False:
                    self.move_towards_player(player)

                    self.update_action(0)

                    if self.rect.colliderect(player.rect):
                        self.update_action(1)
                        player.health -= 0.5 
                        self.attack_counter -=1
                        if self.attack_counter <0:
                            self.touchplayer = True
                            self.attack_counter = 40
                                
                
                if self.touchplayer:
                    self.move_to_topbranch()
                    self.flip = True
                    self.update_action(0)
                    if self.back == True:
                        self.flip = False
                        self.idling_counter -= 1 
                        if self.idling_counter <0:
                            self.touchplayer = False
                            self.idling_counter = 40
        if self.coin_drawn == True:
            self.coin_counter -=1
            if self.coin_counter <0:
                self.move_to(self.rect.x, -self.rect.height)
                self.image.set_alpha(self.alpha)
                self.alpha -= 2
                if self.alpha <= 0:
                    self.kill()
        elif self.alive == False and self.back == False:
            self.move_to_topbranch()
            if self.back == True and self.coin_drawn == False:
                coin = Coin(self.rect.x,100, 0.5)
                coin_group.add(coin)
                self.coin_drawn = True
                    
    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            #self.move_to(self.rect.x, -self.rect.height)
            self.alive = False
            #self.kill()
            

    def update(self, screen_scroll):
        self.update_animation()
        self.check_alive()
        self.rect.x += screen_scroll
