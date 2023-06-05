
import os
import pygame
from pygame.locals import *
from data.tools import *
from data.settings import *
import math


class HealthBar():
    def __init__(self, x, y, health, max_health, img = None):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        if img != None:
            self.image = pygame.transform.scale(img, (int(img.get_width() * 0.4), int(img.get_height() * 0.4)))
            self.img_rect = self.image.get_rect()
            self.img_rect.topleft = (self.x-9, self.y-6)
            
        else:
            self.image = None

    def draw(self, health, screen):
        # update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, "BLACK", (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, "RED", (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, "GREEN", (self.x, self.y, 150 * ratio, 20))
        if self.image != None:
            screen.blit(self.image, self.img_rect)

class Pencil(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, player, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        image = pygame.transform.scale(pencil_img,(int(pencil_img.get_width() * scale), int(pencil_img.get_height() * scale)))
        self.image = pygame.transform.flip(image, player.flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, screen_scroll, enemy=[],enemy2=[]):
        # Move pencil
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Check collision with characters
        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if enemy.alive:
                    enemy.health -= 7
                    self.kill()
        for enemy2 in enemy2_group:
            if enemy2.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if enemy2.alive:
                    enemy2.health -= 4
                    self.kill()
        for flower in flower_group:                    
            if flower.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if flower.alive:
                    flower.health -= 4
                    self.kill()
        for fish in fish_group:
            if fish.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if fish.alive:
                    fish.health -= 5
                    self.kill()
        for bird in bird_group:
            if bird.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if bird.alive:
                    bird.health -= 4
                    self.kill()
        for bigbird in bigbird_group:
            if bigbird.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                if bigbird.alive:
                    bigbird.health -= 4
                    self.kill()
        

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -5
        self.speed = 7
        self.direction = direction
        self.frame_index = 0
        self.action = 0
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()

        # Load all images for the player
        animation_types = ['Move', 'Idle']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'resources/images/Level/Asset/pokeball/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'resources/images/Level/Asset/pokeball/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, screen_scroll,world):
        self.update_animation()
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
    
		#check for collision with level
        for tile in world.obstacle_list:
			#check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
			#check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        for enemy in ballcollusion_group:
            if enemy.rect.colliderect(self.rect):
                
                self.direction *= -1
                dx = self.direction * self.speed           

        # Update ball position
        self.rect.x += dx + screen_scroll
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
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        if self.speed == 0:
            self.frame_index = 0

    def update_action(self,new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = pygame.transform.scale(item_boxes[self.item_type],(int(item_boxes[self.item_type].get_width() * scale), int(item_boxes[self.item_type].get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll):
        self.rect.x += screen_scroll
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # Check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Pencil':
                player.pencil += 15
            elif self.item_type == 'Pokeball':
                player.balls += 5
            # Delete the item box
            self.kill()


class Leaf(pygame.sprite.Sprite):

    def __init__(self, enemy, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        image = pygame.transform.scale(leaf_img,(int(leaf_img.get_width() * scale), int(leaf_img.get_height() * scale)))
        self.image = pygame.transform.flip(image, enemy.flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player, screen_scroll):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Check collision with characters
        if pygame.sprite.spritecollide(player, attack_group, False):
            if player.alive:
                player.health -= 5
                player.hurt = True
                self.kill()
        
        self.rect.x += screen_scroll

class Bubble(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.transform.scale(spit_img,(int(spit_img.get_width() * scale), int(spit_img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player, screen_scroll):
        # Move bubble
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Check collision with characters
        if pygame.sprite.spritecollide(player, attack_group, False):
            if player.alive:
                player.health -= 5
                player.hurt = True
                self.kill()
        self.rect.x += screen_scroll

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y,  scale):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        #reset temporary list of images
        self.animation_list = []
        #count number of files in the folder
        num_of_frames = len(os.listdir(f'resources/images/Level/Asset/coin'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'resources/images/Level/Asset/coin/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, player, world, screen_scroll):
        global game_end
        self.update_animation()
        self.vel_y += GRAVITY
        dy = self.vel_y
    
        for tile in world.obstacle_list:

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                self.speed = 0
                #check if below the ground, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom


        self.rect.y += dy
        # Check collision with the player
        if pygame.sprite.spritecollide(player, coin_group, False):
            self.kill()
        self.rect.x += screen_scroll

    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0



class Seed(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.transform.scale(seed_img,(int(seed_img.get_width() * scale), int(seed_img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player, screen_scroll):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # Check collision with characters
        if pygame.sprite.spritecollide(player, attack_group, False):
            if player.alive:
                player.health -= 5
                player.hurt = True
                self.kill()
        
        self.rect.x += screen_scroll


class Friend(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("resources/images/Level/tileicones/57.png")
        self.image = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.vision = Rect(self.rect.x - 100, self.rect.y, 10,SCREEN_HEIGHT)
        self.vision.centery = SCREEN_HEIGHT//2 
        self.end_lvl = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def player_detected(self, player):
        if self.vision.colliderect(player.rect):
            self.end_lvl = True

    def narration(self,screen):
        if self.end_lvl:
            font = pygame.font.Font('resources/fonts/Monday Monkey.ttf', 28)
            draw_text("Good Job", font, "White", self.rect.x-50, self.rect.y-22, screen)
            draw_text("Good Job", font, "White", self.rect.x-50, self.rect.y-27, screen)
            draw_text("Good Job", font, "White", self.rect.x-48, self.rect.y-25, screen)
            draw_text("Good Job", font, "White", self.rect.x-52, self.rect.y-25, screen)
            draw_text("Good Job", font, "Black", self.rect.x-50, self.rect.y-25, screen)
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.vision.x += screen_scroll


class Branch(pygame.sprite.Sprite):
    
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll


class Bridge(pygame.sprite.Sprite):
    def __init__(self, img, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Rockbridge(pygame.sprite.Sprite):
    def __init__(self, img, x, y, scale):
        self.scale = scale
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def draw_top(self, img, screen):
        image = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        screen.blit(image, self.rect)
    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class WheelHouse(pygame.sprite.Sprite):
    def __init__(self, img, x, y, scale):
        self.scale = scale
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def draw_top(self, screen, img, angle):
        image = pygame.transform.scale(img.convert_alpha(), (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        rotated_image = pygame.transform.rotate(image, angle)
        px,py = (self.rect.centerx - 55, self.rect.centery + 115)
        screen.blit(rotated_image, (px - int(rotated_image.get_width() / 2), py - int(rotated_image.get_height() / 2)))
        
    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class WindMill(pygame.sprite.Sprite):
    def __init__(self, img, x, y, scale):
        self.scale = scale
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def draw_top(self, screen, img, angle):
        image = pygame.transform.scale(img.convert_alpha(), (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        rotated_image = pygame.transform.rotate(image, angle)
        px,py = (self.rect.centerx, self.rect.centery - 35)
        screen.blit(rotated_image, (px - int(rotated_image.get_width() / 2), py - int(rotated_image.get_height() / 2)))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Fly(pygame.sprite.Sprite):

    def __init__(self, x, y,  scale):
        pygame.sprite.Sprite.__init__(self)
        self.flip = False
        self.x = x
        self.y = y
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        #reset temporary list of images
        self.animation_list = []
        #count number of files in the folder
        num_of_frames = len(os.listdir(f'resources/images/Level/batterfly'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'resources/images/Level/batterfly/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def flypath(self, distance, angle, blueFlower, screen_scroll):
        self.rect.x = blueFlower.rect.x + distance*math.cos(angle) +screen_scroll
        self.rect.y = blueFlower.rect.top + distance*math.sin(angle) -15
        if math.sin(angle) > 0:
            self.flip = True
        else:
            self.flip = False

    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        

    def update(self):
        self.update_animation()

class Light(pygame.sprite.Sprite):
    def __init__(self, x, y,  scale):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y        
        img = pygame.image.load("resources/images/Level/tileicones/38.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect1 = self.image.get_rect()
        self.rect1.center = (x, y)
    
    def path(self, distance, angle, lightFlower, screen_scroll):
        x,y = lightFlower.rect.midleft
        self.rect.x = x + distance*math.cos(angle) +screen_scroll
        self.rect.y = y -20 + distance*math.sin(angle)
        x1,y1 = lightFlower.rect.topright
        self.rect1.x = x1 -30 + distance*math.cos(angle+2) +screen_scroll
        self.rect1.y = y1+20 + distance*math.sin(angle+2)
 

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect1)