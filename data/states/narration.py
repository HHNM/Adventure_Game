
import pygame
from pygame.locals import *
import sys
from time import *
import json

pygame.init()

clock = pygame.time.Clock()
color = (241, 238, 221)

#dialog variables
phraseNum = 0
finished = False
visible_characters = 0

SCREEN_WIDTH = 1152 # (1920 * 0.6)
SCREEN_HEIGHT = 648 # (1080 * 0.6)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
keys = pygame.key.get_pressed()

pygame.display.set_caption("narration")
play_narra = True

dialog1path = "data/states/dialog.json"


def scale_image(image, scale):
    image_scaled = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image_scaled

def rect_text(text, size, text_col, x, y):
    font = pygame.font.Font('resources/fonts/Monday Monkey.ttf', size)
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    rect.x, rect.y = x, y
    return rect

def draw_text(text, size, text_col, x, y):
    font = pygame.font.Font('resources/fonts/Monday Monkey.ttf', size)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

image_board = pygame.image.load("resources/images/narration/board.png")
# Scaled board image for text
img_board = scale_image(image_board, 0.6)
board_rect = img_board.get_rect()

run = True


def get_dialog(dialogpath):
    f = open(dialogpath)
    data = json.load(f)
    return data

dialog = get_dialog(dialog1path)



def narration():
    run = True
    while run:
        global phraseNum, visible_characters, finished
        if phraseNum >= len(dialog):
            return

        finished = False
        
        text = ''

        # Load text from json file
        string = dialog[phraseNum]["Text"]
        
        # Load buttons from json file
        if dialog[phraseNum]["Button"]:
            button = "resources/images/Level/UI/" + dialog[phraseNum]["Button"] + ".png"
            img_button = scale_image(pygame.image.load(button), 0.6)
            img_button_rect = img_button.get_rect()
            img_button_rect.x, img_button_rect.y =  SCREEN_WIDTH//5, SCREEN_HEIGHT//2
            img_button_width = img_button.get_width() + 10
        else:
            img_button_width = 0

        # Load face image from json file
        image = "resources/images/narration/" + dialog[phraseNum]["Emotion"] + ".png"
        img = scale_image(pygame.image.load(image), 0.6)
        img_rect = img.get_rect()
        

        if visible_characters <len(string):

            screen.blit(img_board,board_rect)
            screen.blit(img,img_rect)
            if dialog[phraseNum]["Button"]:
                screen.blit(img_button, img_button_rect)
            draw_text("click 'N'", 40, 'black', SCREEN_WIDTH*5//6 , SCREEN_HEIGHT*2//3)
        
        while visible_characters < len(string) :

            text += string[visible_characters]
            
            text_rect = rect_text(text, 60, 'Black', SCREEN_WIDTH//5 + img_button_width, SCREEN_HEIGHT//2)
            pygame.draw.rect(screen, color, text_rect)
            draw_text(text, 60, 'Black', SCREEN_WIDTH//5 + img_button_width, SCREEN_HEIGHT//2)
            pygame.time.wait(50)
            visible_characters += 1
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_n:
                        screen.blit(img_board,board_rect)
                        screen.blit(img,img_rect)
                        if dialog[phraseNum]["Button"]:
                            screen.blit(img_button, img_button_rect)
                        draw_text("click 'N'", 40, 'black', SCREEN_WIDTH*5//6, SCREEN_HEIGHT*2//3)
                        draw_text(string, 60, 'Black', SCREEN_WIDTH//5 + img_button_width, SCREEN_HEIGHT//2)
                        visible_characters = len(string)                   

        finished = True
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_n:
                    if finished:
                        visible_characters = 0
                        phraseNum += 1
        pygame.display.update()




