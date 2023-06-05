import pygame
from data.settings import *
from data.states.fade import ScreenFade
from data.button import Button



# Scale image function
def scale_image(image, scale):
    image_scaled = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image_scaled

# Draw text function
def draw_text(text, font, text_col, x, y, screen):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Reset game level function
def reset_level():
    item_box_group.empty()
    enemy_group.empty()
    enemy2_group.empty()
    enemies_group.empty()
    friend_group.empty()
    pencil_group.empty()
    ball_group.empty()
    attack_group.empty()
    decoration_group.empty()
    exit_group.empty()
    bird_group.empty()
    bigbird_group.empty()
    fish_group.empty()
    flower_group.empty()
    coin_group.empty()
    bridge_group.empty()
    rockbridge_group.empty()
    bridges_group.empty()
    branch_group.empty()
    wheelHouse_group.empty()
    windmill_group.empty()
    fly_group.empty()
    blueFlower_group.empty()
    light_group.empty()
    lightFlower_group.empty()
    ballcollusion_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

# Load image
pencil_img = pygame.image.load("resources/images/Level/tileicones/48.png")
ball_img = pygame.image.load("resources/images/Level/tileicones/47.png")
health_img = pygame.image.load("resources/images/Level/tileicones/49.png")
leaf_img = pygame.image.load("resources/images/Level/Enemy/Enemy2/attack.png")
seed_img = pygame.image.load("resources/images/Level/Enemy/Flower/seed.png")
spit_img = pygame.image.load("resources/images/Level/Enemy/Fish/spit.png")
healthbar_img= pygame.image.load("resources/images/Level/UI/Healthbar.png")

# End game image
end_img = pygame.image.load('resources/images/End/End.png')
end_rect = end_img.get_rect()

# bridge images
bridge_img = pygame.image.load("resources/images/Level/tileicones/45.png")

# rockbridge images
rockbridge_img = pygame.image.load("resources/images/Level/pont/0.png")
topbridge_img = pygame.image.load("resources/images/Level/tileicones/46.png")

# Wheel house image
house_img = pygame.image.load("resources/images/Level/WheelHouse/House.png")
wheel_img = pygame.image.load("resources/images/Level/WheelHouse/Wheell.png")

# Windmill image
mill_img = pygame.image.load("resources/images/Level/Windmill/Windmill.png")
topmill_img = pygame.image.load("resources/images/Level/Windmill/Whee.png")

# Create buttons
restart_img = pygame.image.load('resources/images/Level/UI/restart_btn.png')
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# Credit image
credit_img = pygame.image.load("resources/images/Option/Credit.png")
credit_rect = credit_img.get_rect()

# Game items dict
item_boxes = {
    'Health': health_img,
    'Pencil': pencil_img,
    'Pokeball': ball_img
}


# Create sprite groups
item_box_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
friend_group = pygame.sprite.Group()
pencil_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
attack_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bigbird_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
flower_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
rockbridge_group = pygame.sprite.Group()
bridges_group = pygame.sprite.Group()
branch_group = pygame.sprite.Group()
wheelHouse_group = pygame.sprite.Group()
windmill_group = pygame.sprite.Group()
fly_group = pygame.sprite.Group()
blueFlower_group = pygame.sprite.Group()
light_group = pygame.sprite.Group()
lightFlower_group = pygame.sprite.Group()
ballcollusion_group = pygame.sprite.Group()


# Create screen fades 
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, RED, 4)