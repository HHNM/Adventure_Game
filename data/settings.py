import pygame

SCREEN_WIDTH = 1152 # (1920 * 0.6)
SCREEN_HEIGHT = 648 # (1080 * 0.6)

Title = "Ajib"
FPS = 60
# Define game variables
GRAVITY = 0.32
SCROLL_THRESH = 600
ROWS = 9
ROW = 16
COLS = 1500
TILE_SIZE = SCREEN_WIDTH // ROW
TILE_TYPES = 25
MAX_LEVELS = 5
screen_scroll = 0
bg_scroll = 0
scale = 0.15
level = 1

start_game = False
restart_level = False
level_complete = False
game_end = False
pause_restart = False
narration_done = False

# Define player action variables
moving_left = False
moving_right = False
ball = False
ball_thrown = False
show_credit = False

# Define color
NAVY = (95, 158, 160)
GREY = pygame.color.THECOLORS['grey']
BLUE = (0, 0, 250)
RED = (250, 0, 0)
GREEN = (0, 250, 0)
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
s = 17
