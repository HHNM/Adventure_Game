import pygame, sys
from pygame.locals import *
from data.button import Button

pygame.init()

mainclock = pygame.time.Clock()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 648

menu_img = pygame.image.load('resources/images/into/Menu.png').convert_alpha()
img_rect = menu_img.get_rect()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

screen.fill("grey")

font = pygame.font.SysFont('Futura', 35)
fontTitle = pygame.font.SysFont('Futura', 50)
fontback = pygame.font.SysFont('Futura', 27)

credit_img = pygame.image.load("resources/images/Option/Credit.png")
credit_rect = credit_img.get_rect()
# BG = pygame.image.load("Background.png")

click = False

def play():
    while True:
        screen.fill("black")
        play_text = font.render("This is the PLAY screen.", True, 'White')
        play_rect = play_text.get_rect(topleft=(640,240))
        screen.blit(play_text, play_rect)

        play_back_text = font.render("BACK", True, 'White')
        play_back = Button(640, 460, play_back_text, 1)
        play_back.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if play_back.draw(screen):
                    main_menu()

        pygame.display.update()

def sound():
    sounds = True
    while sounds:
        screen.fill("black")
        sound_text = font.render("Sound settings go here.", True, 'White')
        sound_rect = sound_text.get_rect(topleft=(640,240))
        screen.blit(sound_text, sound_rect)

        sound_back_text = fontback.render("BACK", True, 'White')
        sound_back = Button(940, 460, sound_back_text, 1)
        sound_back.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if sound_back.draw(screen):
            sounds = False
    
        pygame.display.update()
        mainclock.tick(60)

def credit():
    credits = True
    while credits:
        screen.blit(credit_img, credit_rect)

        credit_back_text = font.render("Back", True, 'Blue')
        credit_back = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 50, credit_back_text, 1)
        credit_back.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if credit_back.draw(screen):
            credits = False
    
        pygame.display.update()
        mainclock.tick(60)

def options():
    option = True
    while option:

        screen.blit(menu_img,img_rect)

        options_text = fontTitle.render("OPTIONS", True, "Blue")
        options_rect = options_text.get_rect(topleft = (680, 100))
        screen.blit(options_text, options_rect)

        sound_text = font.render("SOUND", True, 'Black')
        sound_button = Button(720, 250, sound_text, 1)
        sound_button.draw(screen)

        credit_text = font.render("CREDIT", True, 'Black')
        credit_button = Button(720, 350, credit_text, 1) 
        credit_button.draw(screen)

        options_back_text = fontback.render("BACK", True, "White")
        options_back = Button(940, 500, options_back_text, 1)
        options_back.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if options_back.draw(screen):
            option = False
        if credit_button.draw(screen):
            credit()
        if sound_button.draw(screen):
            sound()

        pygame.display.update()
        mainclock.tick(60)

def main_menu():
    menu = True
    while menu:
        screen.blit(menu_img,img_rect)

        menu_text = fontTitle.render('MAIN MENU', True, 'Blue')
        menu_rect = menu_text.get_rect(topleft=(650, 100))

        play_text = font.render("PLAY", True, 'Black')
        play_button = Button(720, 250, play_text, 1)
        play_button.draw(screen)

        options_text = font.render("OPTIONS", True, 'Black')
        options_button = Button(700, 400, options_text, 1)
        options_button.draw(screen)

        quit_text = font.render("QUIT", True, 'Black')
        quit_button = Button(730, 550, quit_text, 1)
        quit_button.draw(screen)

        screen.blit(menu_text, menu_rect)
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        if play_button.draw(screen):
            return True
        if options_button.draw(screen):
            options()
        if quit_button.draw(screen):
            pygame.quit()
            sys.exit()

        pygame.display.update()
        mainclock.tick(60)
    
