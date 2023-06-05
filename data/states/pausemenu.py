import pygame, sys
from pygame.locals import *
from data.button import Button


pygame.init()

SCREEN_WIDTH = 1152
SCREEN_HEIGHT = 648

pygame.display.set_caption("PauseMenu")

font = pygame.font.SysFont('Futura', 30)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

img = pygame.image.load("resources/images/Level/UI/Pause.png")
menu_img = pygame.transform.scale(img,(int(img.get_width() * 0.5), int(img.get_height() * 0.5)))

menu_rect = menu_img.get_rect()
menu_rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5)

controller_img = pygame.image.load("resources/images/Option/Controller.png")
controller_rect = controller_img.get_rect()

controller_back_text = font.render("Back", True, "Black")
controller_back = Button(SCREEN_WIDTH-100, SCREEN_HEIGHT-70, controller_back_text, 1)

controller_exit = False

def controller():
    global controller_exit
    i = True 
    while i == True:
        screen.blit(controller_img, controller_rect)
        controller_back.draw(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if controller_back.draw(screen):
                    i = False
                    controller_exit = True
        pygame.display.update()


def options():
    global controller_exit

    controller_text = font.render("Controller", True, 'Black')
    controller_button = Button(menu_rect.left + menu_rect.width *0.33, menu_rect.top + 150, controller_text, 1)

    options_back_text = font.render("BACK", True, "Black")
    options_back = Button(menu_rect.left + menu_rect.width *0.33 + 100, menu_rect.top + 200, options_back_text, 1)
    option = True
    while option:
        screen.blit(menu_img, menu_rect)
        controller_button.draw(screen)
        options_back.draw(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    option = False
            if options_back.draw(screen):
                option = False
            if controller_button.draw(screen):
                option = False
                controller()

 
        pygame.display.update()

def pausemenu():
        global controller_exit
        
        continue_text = font.render("Continue", True, "Black")
        continue_button = Button(menu_rect.left + menu_rect.width *0.33 + 10, menu_rect.top + 100, continue_text, 1)    
        
        restart_text = font.render("Restart", True, "Black")
        restart_button = Button(menu_rect.left + menu_rect.width *0.33 + 10, menu_rect.top + 150, restart_text, 1)

        options_text = font.render("Options", True, "Black")
        options_button = Button(menu_rect.left + menu_rect.width *0.33 + 10, menu_rect.top + 200, options_text, 1)
        
        quit_text = font.render("Quit", True, "Black")
        quit_button = Button(menu_rect.left + menu_rect.width *0.33 + 10, menu_rect.top + 250, quit_text, 1)

        pause = True
            
        while pause:
            screen.blit(menu_img, menu_rect)
            continue_button.draw(screen)
            restart_button.draw(screen)
            options_button.draw(screen)
            quit_button.draw(screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False

                if continue_button.draw(screen):
                    pause = False
                if controller_exit == True:
                    pause = False
                    controller_exit = False
                if restart_button.draw(screen):
                    return True

                if options_button.draw(screen):
                    options()

                if quit_button.draw(screen):
                    pygame.quit()
                    sys.exit()
                

            pygame.display.update()


