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


start_text = font.render("Start", True, "White")
start = Button(SCREEN_WIDTH-100, SCREEN_HEIGHT-100, start_text, 1)

intro_img = pygame.image.load('resources/images/into/Intro.png').convert_alpha()
intro_rect = intro_img.get_rect()



def intromenu():
    i = True
    while i == True:
        screen.blit(intro_img,intro_rect)
        start.draw(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    i = False
                    return True
            if event.type == MOUSEBUTTONDOWN:
                if start.draw(screen):
                    i = False
                    return True
        pygame.display.update()

