import csv
import pygame
from pygame.locals import *
from data.button import Button
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 864      #(1152 *0.75) game screen width * 0.75
SCREEN_HEIGHT = 486     #(648 *0.75) game screen height * 0.75
LOWER_MARGIN = 200
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# Define level editor variables
ROWS = 9
ROW = 16
MAX_COLS = 1500
TILE_SIZE = SCREEN_WIDTH // ROW
TILE_TYPES = 28
level = 0
current_tile = 0
current_rect = 0
scale = 0.1125 #(0.15 * 0.75)
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
line1, line2, line3 = False, False, False

# Define colors
GREEN = (50, 200, 0)
WHITE = (250, 250, 250)
RED = (250, 0, 0)
GREY = pygame.color.THECOLORS['grey']
BLUE = (0, 128,155)

#define font
font = pygame.font.SysFont('Futura', 30)

# create buttons for list
list1 = Button(SCREEN_WIDTH + 30, 10, font.render('List1', True, BLUE), 1)
list2 = Button(SCREEN_WIDTH + 110, 10, font.render('List2', True, BLUE), 1)
list3 = Button(SCREEN_WIDTH + 190, 10, font.render('List3', True, BLUE), 1)





# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))

# Scale image function
def scale_image(image, scale):
    image_scaled = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image_scaled

# Import bg images
sky_img = scale_image(pygame.image.load("resources/images/LevelEditor/BackGround/0.png").convert_alpha(), scale)
cloud_img = scale_image(pygame.image.load("resources/images/LevelEditor/BackGround/1.png").convert_alpha(), scale)
mountain_img = scale_image(pygame.image.load("resources/images/LevelEditor/BackGround/2.png").convert_alpha(), scale)
ground_img = scale_image(pygame.image.load("resources/images/LevelEditor/BackGround/3.png").convert_alpha(), scale)


# Import save and load button image
save_img = pygame.image.load('resources/images/Level/UI/save_btn.png')
load_img = pygame.image.load('resources/images/Level/UI/load_btn.png')

# create save and load button
save_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + 30, save_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT + 30, load_img, 1)

def draw_bg():
    screen.fill(BLUE)
    width = sky_img.get_width()
    for x in range(70):
        screen.blit(sky_img, ((x * width)-scroll*0.5, 0))
        screen.blit(cloud_img, ((x * width)-scroll*0.6, 0))
        screen.blit(mountain_img, ((x * width)-scroll*0.7, 0))
        screen.blit(ground_img, ((x * width)-scroll*0.75, 0))


# store tiles in a list
def tile_list():
    img_list = []
    num_tile = len(os.listdir(f"resources/images/Level/tileicones"))
    for x in range(num_tile):
        img = pygame.image.load(f'resources/images/Level/tileicones/{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    return img_list


img_list = tile_list()

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)




def draw_grid():
    # Vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE-scroll, 0), (c * TILE_SIZE-scroll, SCREEN_HEIGHT))
    # Horizonal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

def draw_world(img_list):
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x*TILE_SIZE-scroll, y*TILE_SIZE))
    

def list_buttons(img_list):
    # make a button list
    button_list = []
    tile_dict = {}
    button_col = 0
    button_row = 0

    length = range(18)
    if line1:
        length = range(18)
    if line2:
        length = range(18, 36)
    if line3:
        length = range(36, len(img_list))
    for i in length:
        tile_button = Button(SCREEN_WIDTH + (75 * button_col) +40, 60 * button_row + 50, img_list[i], 0.8)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0
        tile_dict[i] = tile_button
    return button_list, tile_dict

run = True
while run:

    clock.tick(FPS)
    
    
    
    draw_bg()
    draw_grid()
    draw_world(img_list)
    button_list, dict = list_buttons(img_list)

    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT + 60))
    
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + 25)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + 55)
    
    # Save level when save button is clicked
    if save_button.draw(screen):
        with open(f'resources/levels/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    
    # Load level when load button is clicked
    if load_button.draw(screen):
        scroll = 0
        with open(f'resources/levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    
    pygame.draw.rect(screen, "White", list1.rect)
    pygame.draw.rect(screen, "White", list2.rect)
    pygame.draw.rect(screen, "White", list3.rect)

    if list1.draw(screen):
        line1, line2, line3 = True, False, False
    if list2.draw(screen):
        line1, line2, line3 = False, True, False
    if list3.draw(screen):
        line1, line2, line3 = False, False, True
    
    # choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            for index, tile in dict.items():
                if i == tile:
                    current_tile = index
            current_rect = button_count
    
    # Highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_rect].rect, 3)

    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < sky_img.get_width()*70:
        scroll += 5 * scroll_speed
    
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                level += 1
            if event.key == K_DOWN and level > 0:
                level -= 1
            if event.key == K_LEFT:
                scroll_left = True
            if event.key == K_RIGHT:
                scroll_right = True
            if event.key == K_LSHIFT:
                scroll_speed = 5
        if event.type == KEYUP:
            if event.key == K_LEFT:
                scroll_left = False
            if event.key == K_RIGHT:
                scroll_right = False
            if event.key == K_LSHIFT:
                scroll_speed = 1

    pygame.draw.rect(screen, RED,(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)

    pygame.display.update()

pygame.quit()