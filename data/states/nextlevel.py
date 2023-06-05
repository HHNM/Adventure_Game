import pygame
import sys
from pygame.locals import *
from data.button import Button
from data.tools import scale_image

SCREEN_WIDTH = 1152 # (1920 * 0.6)
SCREEN_HEIGHT = 648

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("intro")
font = pygame.font.SysFont('Futura', 30)


start_text = font.render("Next", True, "Black")
start = Button(SCREEN_WIDTH-100, SCREEN_HEIGHT-70, start_text, 1)


intro_img = pygame.image.load('resources/images/nextlevel/Next.png').convert_alpha()
intro_rect = intro_img.get_rect()

def nextLevel():
    i = True
    time = 1000
    while i == True and time > 0:
        screen.blit(intro_img,intro_rect)
        start.draw(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if start.draw(screen):
                    i = False
                    return True
        time -= 1
        pygame.display.update()


