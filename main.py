
import pygame
from pygame.locals import *
from data.settings import *
from data.tools import *
from data.level import World
from data.states.intromenu import intromenu
from data.states.pausemenu import pausemenu 
from data.states.menu_main import main_menu 
from data.states.nextlevel import nextLevel
from data.states.narration import narration
import csv


class Game():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ajib")
        self.font = pygame.font.SysFont('Futura', 30)

        # Import bg images
        self.sky_img = scale_image(pygame.image.load("resources/images/Level/Background/Level1/0.png").convert_alpha(),0.24)
        self.cloud_img = scale_image(pygame.image.load("resources/images/Level/Background/Level1/1.png").convert_alpha(), 0.24)
        self.mountain_img = scale_image(pygame.image.load("resources/images/Level/Background/Level1/2.png").convert_alpha(), 0.24)
        self.ground_img = scale_image(pygame.image.load("resources/images/Level/Background/Level1/3.png").convert_alpha(), 0.24)
        self.background_img = scale_image(pygame.image.load("resources/images/Level/Background/Level1/4.png").convert_alpha(), 0.24)

        self.sky2_img = scale_image(pygame.image.load("resources/images/Level/Background/Level2/0.png").convert_alpha(),0.24)
        self.mountain2_img = scale_image(pygame.image.load("resources/images/Level/Background/Level2/1.png").convert_alpha(), 0.26)

        self.sky3_img = scale_image(pygame.image.load("resources/images/Level/Background/Level3/0.png").convert_alpha(),0.24)
        self.mountain3_img = scale_image(pygame.image.load("resources/images/Level/Background/Level3/1.png").convert_alpha(), 0.24)
        self.ground2_img = scale_image(pygame.image.load("resources/images/Level/Background/Level3/2.png").convert_alpha(), 0.24)
        self.background2_img = scale_image(pygame.image.load("resources/images/Level/Background/Level3/4.png").convert_alpha(), 0.24)
    
    def draw_background(self, bg_scroll):
        width = self.sky_img.get_width()

        if level == 3:
            for x in range(20):
                self.screen.blit(self.sky3_img, ((x * width)-bg_scroll*0.5, 0))
                self.screen.blit(self.mountain3_img, ((x * width)-bg_scroll*0.7, 0))
                self.screen.blit(self.background2_img, ((x * width)-bg_scroll*0.75, 100))
                self.screen.blit(self.ground2_img, ((x * width)-bg_scroll*0.75, 0))
        elif level == 4:
            for x in range(20):
                self.screen.blit(self.sky2_img, ((x * width)-bg_scroll*0.75, 0))
                self.screen.blit(self.mountain2_img, ((x * width)-bg_scroll*0.75, 100))
                self.screen.blit(self.mountain2_img, ((x * width)-bg_scroll*0.75, 0))
        else:
            for x in range(20):
                self.screen.blit(self.sky_img, ((x * width)-bg_scroll*0.5, 0))
                self.screen.blit(self.cloud_img, ((x * width)-bg_scroll*0.6, 0))
                self.screen.blit(self.mountain_img, ((x * width)-bg_scroll*0.7, 0))
                self.screen.blit(self.background_img, ((x * width)-bg_scroll*0.75, 100))
                self.screen.blit(self.ground_img, ((x * width)-bg_scroll*0.75, 0))
    
    def EndGame(self, player):
        global game_end
        if pygame.sprite.spritecollide(player, coin_group, False):
            game_end = True

    def Run(self): 
        global bg_scroll, screen_scroll, level, pause_restart, restart_level, pause_restart, game_end
        global start_intro, start_game, level_complete, narration_done
        
        world_data = []
        
        for row in range(ROWS):
            r = [-1] * COLS
        
            world_data.append(r)
        #load in level data and create world
        with open(f'resources/Levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        
        world = World()
        player, health_bar= world.process_data(world_data)    
        # Set wheel and batterfly rotation angle  
        angle = 0
        flyangle = 0

        # Set endgame screen timer
        time = 300
        
        clock = pygame.time.Clock()
        
        run = True
        while run:
            clock.tick(FPS)
                ##start_game == intro()
            if start_game == False:
                # menu
                #screen.fill(NAVY)
                if intromenu():
                # Add buttons
                    if main_menu() == True:    
                        start_game = True
                        start_intro = True
                
            else:
                self.draw_background(bg_scroll)
            
                health_bar.draw(player.health, self.screen)
                

                self.screen.blit(scale_image(pencil_img, 0.5), (10, 45))
                draw_text(f'x{player.pencil}', self.font, WHITE, 35, 40, self.screen)

                self.screen.blit(scale_image(ball_img, 0.5), (95 , 40))
                draw_text(f'x{player.balls}', self.font, WHITE, 120, 40, self.screen)

                draw_text(f'level {level}', self.font, WHITE, SCREEN_WIDTH//2-20, 20, self.screen)
                
                
                for wheelHouse in wheelHouse_group:
                    wheelHouse.draw(self.screen)
                    wheelHouse.update(screen_scroll)
                    wheelHouse.draw_top(self.screen, wheel_img, angle)

                for windmill in windmill_group:
                    windmill.draw(self.screen)
                    windmill.update(screen_scroll)
                    windmill.draw_top(self.screen,topmill_img, angle*2)
                
                angle += 0.5
                flyangle += 0.01

                # Update and draw groups
                item_box_group.update(player, screen_scroll)
                item_box_group.draw(self.screen)
                decoration_group.update(screen_scroll)
                decoration_group.draw(self.screen)
                exit_group.update(screen_scroll)
                exit_group.draw(self.screen)
                branch_group.update(screen_scroll)
                branch_group.draw(self.screen)
                blueFlower_group.update(screen_scroll)
                blueFlower_group.draw(self.screen)
                lightFlower_group.update(screen_scroll)
                lightFlower_group.draw(self.screen)


                #draw world map
                world.draw(screen_scroll,self.screen)

                # Update and draw groups
                ball_group.update(screen_scroll, world)
                attack_group.update(player ,screen_scroll)
                coin_group.update(player, world, screen_scroll)
                pencil_group.draw(self.screen)
                ball_group.draw(self.screen)
                attack_group.draw(self.screen)
                coin_group.draw(self.screen)
                
                for pencil in pencil_group:
                    pencil.update(screen_scroll)

                
                for friend in friend_group:
                    friend.draw(self.screen)
                    friend.update(screen_scroll)
                    friend.player_detected(player)
                    friend.narration(self.screen)   
                    
                player.attack()
                player.update()
                player.draw(self.screen)
                
                for enemy in enemy_group:
                    enemy.draw(self.screen)
                    enemy.update(screen_scroll)
                    enemy.ai(player, world)
                    
                for enemy2 in enemy2_group:
                    enemy2.draw(self.screen)
                    enemy2.update()
                    enemy2.ai(player, world, screen_scroll)
                    
                for flower in flower_group:
                    flower.draw(self.screen)
                    flower.update(screen_scroll)
                    flower.ai(player, world)
                    
                for bridge in bridge_group:
                    bridge.draw(self.screen)
                    bridge.update(screen_scroll)    

                for rockbridge in rockbridge_group:
                    rockbridge.draw(self.screen)
                    rockbridge.update(screen_scroll)
                    rockbridge.draw_top(topbridge_img, self.screen)    

                for bird in bird_group:
                    bird.draw(self.screen)
                    bird.update(screen_scroll)
                    bird.ai(player)
                
                for bigbird in bigbird_group:
                    bigbird.draw(self.screen)
                    bigbird.update(screen_scroll)
                    bigbird.ai(player, self.screen)

                for fish in fish_group:
                    fish.draw(self.screen)
                    fish.update(screen_scroll)
                    fish.ai(player)
                
                for fly in fly_group:
                    for blueFlower in blueFlower_group:
                        fly.flypath(blueFlower.rect.width // 2,flyangle, blueFlower, screen_scroll)
                        fly.draw(self.screen)
                        fly.update()

                for light in light_group:
                    for lightFlower in lightFlower_group:
                        light.path(30,flyangle*2, lightFlower, screen_scroll)
                        light.draw(self.screen)
                        light.update()
                
                if start_intro == True:
                    if intro_fade.fade(self.screen):
                        start_intro = False
                        intro_fade.fade_counter = 0
                        if narration_done == False:
                            narration()
                            narration_done = True
                        
                
                # Update player actions
                if player.alive:
                    if pause_restart == True:
                        player.kill()
                        screen_scroll = 0
                        death_fade.fade_counter = 0
                        start_intro = True
                        bg_scroll = 0
                        world_data = reset_level()

                        #load in level data and create world
                        with open(f'resources/Levels/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar= world.process_data(world_data)
                        pause_restart = False

                    player.set_animation(world, bg_scroll)
                    
                    screen_scroll, level_complete = player.move(world, bg_scroll)
                    bg_scroll -= screen_scroll

                    if level_complete == True:
                        nextLevel()
                        start_intro = True
                        level += 1
                        bg_scroll = 0
                        world_data = reset_level()
                        if level <= MAX_LEVELS:
                            #load in level data and create world
                            with open(f'resources/Levels/level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar= world.process_data(world_data)
                
                else:
                    screen_scroll = 0
                    if death_fade.fade(self.screen):
                        if restart_button.draw(self.screen):
                            restart_level = True
                        if restart_level == True:
                            restart_level = False
                            death_fade.fade_counter = 0
                            start_intro = True
                            bg_scroll = 0
                            world_data = reset_level()
                            #load in level data and create world
                            with open(f'resources/Levels/level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar= world.process_data(world_data)
            
            self.EndGame(player)
            # Check if the player finished the game
            if game_end:
                if time > 0:
                    self.screen.blit(end_img,end_rect)
                    time -= 1
                else: 
                    self.screen.blit(credit_img, credit_rect)
                player.kill()
                screen_scroll = 0
                death_fade.fade_counter = 0
                start_intro = True
                bg_scroll = 0
                world_data = reset_level()
            

            for event in pygame.event.get():
                # Quit game
                if event.type == QUIT:
                    run = False
                # Keyboard presses
                player.get_input()
                # Keyboard presses
                if event.type == KEYDOWN:
                    if event.key == K_s and start_game == False:
                        start_game = True
                    if event.key == K_r:
                        restart_level = True
                    if start_game == True and event.key == pygame.K_RETURN:
                        if pausemenu():
                            pause_restart = True


            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game() 
    game.Run()
