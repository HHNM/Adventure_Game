import pygame
from pygame.locals import *
from data.player import Character
from data.ui import *
from data.enemy import Enemy, Enemy2, Bird, BigBird, Flower, Fish 


class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self, data):
        self.level_length = len(data[0])
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0 and tile <= 13:
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.45)
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    self.obstacle_list.append(tile_data)
                elif tile >= 14 and tile <= 35 and tile != 25 and tile != 26 and tile != 31:
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.5)
                    decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE + 4)
                    decoration_group.add(decoration)
                elif tile == 31 or tile == 36:
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.5)
                    decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE + 4)
                    blueFlower_group.add(decoration)
                elif tile == 26 :
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.5)
                    branch = Branch(img, x * TILE_SIZE, y * TILE_SIZE + 20)
                    branch_group.add(branch)
                elif tile == 25 :
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.5)
                    lightFlower = Decoration(img, x * TILE_SIZE, y * TILE_SIZE + 4)
                    lightFlower_group.add(lightFlower)
                elif tile >= 40 and tile <= 42:
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.5)
                    decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE + 3)
                    decoration_group.add(decoration)
                elif tile == 43:
                    wheelHouse = WheelHouse(house_img, x * TILE_SIZE, y * TILE_SIZE + 57, 0.5)
                    wheelHouse_group.add(wheelHouse)
                elif tile == 44:
                    windmill = WindMill(mill_img, x * TILE_SIZE, y * TILE_SIZE + 12 , 0.5)
                    windmill_group.add(windmill)
                elif tile == 45:
                    bridge = Bridge(bridge_img, x * TILE_SIZE, y * TILE_SIZE , 0.4)
                    bridge_group.add(bridge)
                    bridges_group.add(bridge)
                elif tile == 46:
                    rockbridge = Rockbridge(rockbridge_img, x * TILE_SIZE, y * TILE_SIZE-10 , 0.56)
                    rockbridge_group.add(rockbridge)
                    bridges_group.add(rockbridge)
                elif tile == 57:
                    friend = Friend(x * TILE_SIZE, y * TILE_SIZE + 2, 0.6)
                    friend_group.add(friend)
                elif tile == 56:
                    player = Character(x * TILE_SIZE, y * TILE_SIZE , 0.6, 3, 20, 20)
                    health_bar = HealthBar(10, 10, player.health, player.health, healthbar_img)
                elif tile == 50:
                    enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE, 1, 0.6, 2)
                    enemy_group.add(enemy)
                    ballcollusion_group.add(enemy)
                elif tile == 51:
                    enemy2 = Enemy2(x * TILE_SIZE, y * TILE_SIZE, 2, 0.6, 2)
                    enemy2_group.add(enemy2)
                    ballcollusion_group.add(enemy2)
                elif tile == 54:
                    bird = Bird(x * TILE_SIZE, y * TILE_SIZE, 0.4, 2)
                    bird_group.add(bird)
                    ballcollusion_group.add(bird)
                elif tile == 55:
                    bigbird = BigBird(x * TILE_SIZE, y * TILE_SIZE, 0.5, 5)
                    bigbird_group.add(bigbird)
                elif tile == 52:
                    flower = Flower(x * TILE_SIZE, y * TILE_SIZE, 0.55, 2)
                    flower_group.add(flower)
                    ballcollusion_group.add(flower)
                elif tile == 53:
                    fish = Fish(x * TILE_SIZE, y * TILE_SIZE, 2, 0.55, 2)
                    fish_group.add(fish)
                    ballcollusion_group.add(fish)
                elif tile == 47:#create health box
                    item_box = ItemBox('Pokeball', x * TILE_SIZE, y * TILE_SIZE, 0.6)
                    item_box_group.add(item_box)
                elif tile == 48:#create pencil box
                    item_box = ItemBox('Pencil', x * TILE_SIZE, y * TILE_SIZE, 0.8)
                    item_box_group.add(item_box)
                elif tile == 49:#create health box
                    item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE, 0.2)
                    item_box_group.add(item_box)
                elif tile == 37:
                    batterfly = Fly(x * TILE_SIZE, y * TILE_SIZE,0.4)
                    fly_group.add(batterfly)
                elif tile == 38:
                    light = Light(x * TILE_SIZE, y * TILE_SIZE,0.4)
                    light_group.add(light)      
                elif tile == 39:#create exit
                    img = scale_image(pygame.image.load(f'resources/images/Level/tileicones/{tile}.png').convert_alpha(), 0.6)
                    exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE + 25)
                    exit_group.add(exit)
                for enemy in enemy_group:
                    enemies_group.add(enemy)
                for enemy2 in enemy2_group:
                    enemies_group.add(enemy2)
                for flower in flower_group:
                    enemies_group.add(flower)
                for fish in fish_group:
                    enemies_group.add(fish)
                for bird in bird_group:
                    enemies_group.add(bird)

        return player, health_bar


    def draw(self, screen_scroll, screen):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


