import os
import pygame
from pygame.locals import *
from data.settings import GRAVITY, SCREEN_WIDTH,SCREEN_HEIGHT, SCROLL_THRESH, TILE_SIZE
from data.tools import pencil_group, bridges_group, ball_group, enemies_group, bigbird_group, friend_group
from data.ui import Ball, Pencil



class Character(pygame.sprite.Sprite):    
    def __init__(self,x, y, scale, speed, pencil,balls):
        pygame.sprite.Sprite.__init__(self)
        self.hurt = False
        self.ball = False
        self.ball_thrown = False
        self.alive = True
        self.moving_right = False
        self.moving_left = False
        self.speed = speed
        self.pencil = pencil
        self.balls = balls
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.attacking = False
        self.throw_cooldown = 0
        self.throwing_pencil = False
        self.throwing_ball = False
        self.running = False
        self.jump = False
        self.in_air = True
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # load all images for the player
        animation_types = ['Idle', 'Walk', 'Run', 'Jump', 'Attack1', 'Attack2', 'Throw', 'Hurt', 'Die','Attack3']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"resources/images/Level/Sprite/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"resources/images/Level/Sprite/{animation}/{i}.png").convert_alpha()
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

    def move(self, world, bg_scroll):
        screen_scroll = 0
        dx = 0
        dy = 0

        if self.running:
            drun = self.speed
        else: 
            drun = 0
        
        if self.moving_right:
            dx = self.speed + drun  
            self.flip = False
            self.direction = 1
            if self.in_air:
                dx += 1

        if self.moving_left:
            dx = -self.speed - drun
            self.flip = True
            self.direction = -1
            if self.in_air:
                dx += -1
        
        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -10
            self.jump = False
            self.in_air = True
            
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        # Check for collision
        for tile in world.obstacle_list:
            # Check collisino in the x direction
            tile1 = tile[1].inflate(-40,-25)
            if tile1.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
        # Check collision in the y direction
            if tile1.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile1.bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile1.top - self.rect.bottom

        #check if going off the edges of the screen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            dx = 0
        
        # Collusion with bridges
        for p in bridges_group:     
            if p.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    offset = (p.rect.x - self.rect.x), (p.rect.y - self.rect.y)
                    if self.mask.overlap(p.mask, offset):
                        self.vel_y = 0
                        self.in_air = False
                        y = self.mask.overlap(p.mask, offset)[1]
                        self.rect.bottom = y + self.rect.y + 7

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT + self.height:
            self.health = 0

        # Check if fallen off the map
        level_complete = False
        for friend in friend_group:
            if friend.rect.colliderect(self.rect.x, self.rect.y , self.rect.width, self.rect.height):
                level_complete = True
        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
        # Update scroll based on player position
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH  and bg_scroll < world.level_length * TILE_SIZE) or (self.rect.left < SCREEN_WIDTH - SCROLL_THRESH - 100 and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx
        return screen_scroll, level_complete

    def throw_pencil(self):
        if self.throw_cooldown == 0  and self.pencil > 0:
            self.throw_cooldown = 30
            pencil = Pencil(self.rect.centerx, self.rect.centery + 5 , self.direction, self, 0.5)
            pencil_group.add(pencil)
            self.update_action(4)
            # Reduce pencil
            self.pencil -= 1
    
    def throw_ball(self):
        if  self.ball_thrown == False and self.balls > 0:
            ball = Ball(self.rect.centerx, self.rect.centery, self.direction, 0.5)
            ball_group.add(ball)
            self.update_action(6)
            # Reduce balls
            self.balls -= 1
            self.ball_thrown = True
    
    def attack(self):
        if self.alive:
            if self.attacking:
                for e in enemies_group:
                    if self.rect.colliderect(e.rect):
                        e.health -= 0.2
                for e in bigbird_group:
                    if self.rect.colliderect(e.rect):
                        e.health -= 1


    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 200
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 8:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
            if self.action == 5 and self.attacking == True:
                self.attacking = False
            if self.action == 4 and  self.throwing_pencil == True:
                self.throwing_pencil = False
            if self.action == 6 and  self.throwing_ball == True:
                self.throwing_ball = False
            if self.action == 7 and  self.hurt == True:
                self.hurt = False
            if self.action == 1:
                bottom = self.rect.bottom
                x = self.rect.x
                y = self.rect.y
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x
                self.rect.y = y
                
            self.mask = pygame.mask.from_surface(self.image)


    def update_action(self,new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(8)
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.moving_left = True
            self.moving_right = False
        elif keys[pygame.K_RIGHT]:
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_left = False
            self.moving_right = False
        if keys[pygame.K_e] and self.hurt == False:
            self.attacking = True
        if keys[pygame.K_t] and self.hurt == False and self.attacking == False and self.pencil>0:
            self.throwing_pencil = True
        if keys[pygame.K_r] and self.hurt == False and self.attacking == False:
            self.throwing_ball = True
        else:
            self.throwing_ball = False
            self.ball_thrown = False
        if keys[pygame.K_LSHIFT] and (self.moving_left or self.moving_right):
            self.running = True
        else:
            self.running = False

        if keys[pygame.K_UP] and self.alive and self.hurt == False:
            self.jump = True
        else:
            self.jump = False
    
    def set_animation(self, world, bg_scroll):
         # Update player actions
        if self.in_air:
            self.update_action(3)
        # Throw pencils
        elif self.throwing_pencil:
            self.throw_pencil() 
        # Throw balls
        elif self.throwing_ball:
            self.throw_ball()
        elif self.attacking:
            self.moving_left, self.moving_right = False, False 
            self.update_action(5)
        elif self.hurt:
            self.update_action(7)
            self.moving_left, self.moving_right = False, False
        elif self.running:
            self.update_action(2)
        elif self.moving_left or self.moving_right:
            self.update_action(1)
        else:
            self.update_action(0)
        self.move(world, bg_scroll)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
