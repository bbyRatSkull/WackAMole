# STARTER
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
from button import Button

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = MOLE
        #self.image = image.load(resource_path("molehole.png")).convert()
        self.rect = self.image.get_rect().move(x,y)

# Colors we want to use
darkbrown = (60,40,37)
pink = (250,110,121)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# set up the display
pygame.init()
# a list in the format [(x,y)]
ratio_sizes = [(1280,720),(1504,846),(1920,1080)]
screenvar = pygame.display.get_desktop_sizes()
for item in ratio_sizes:
    if screenvar[0][0] >= item[0] and screenvar[0][1] >= item[1]:
        GAME_SIZE = item
#the coordinates for window generation
GEN_COORDS = [((screenvar[0][0]-GAME_SIZE[0])/2), ((screenvar[0][1]-GAME_SIZE[1])/2)]


screen = pygame.display.set_mode(GAME_SIZE, FULLSCREEN)
# loads in image and scales it to screen size
BG = transform.scale(pygame.image.load("BG_Menu.PNG").convert(),(GAME_SIZE))
pygame.display.set_caption("Whack a Mole!")

MOLE = transform.scale(pygame.image.load("Sprites/temp_hole.PNG").convert_alpha(),(72,72))

# create some fonts
headerfont = pygame.font.SysFont('helveticaneue', 48)
buttonfont = pygame.font.SysFont('helveticaneue',30)
headerfont.set_bold(True)

def main_menu(): #the main menu screen
    while True:
        screen.fill(black)
        screen.blit(BG, (GEN_COORDS[0], GEN_COORDS[1]))

        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        #menu_text = buttonfont.render("Wack a Mole", True, black)
        #menu_rect = menu_text.get_rect(center=(640, 100))

        #screen.blit(menu_text, menu_rect)

        play_button = Button(None, pos=(364,463), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Play", font=buttonfont, base_color=darkbrown, hovering_color=pink)
        quit_button = Button(None, pos=(1059, 576), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Quit", font=buttonfont, base_color=darkbrown, hovering_color=pink)

        for button in [play_button, quit_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mousePos):
                    tutorial()
                #if shop_button.checkForInput(mousePos):
                    #shop()
                if quit_button.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  

def shop():
    while True:    
        screen.fill(darkblue)

        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        shop_text = buttonfont.render("Welcome to the shop!", True, black)
        shop_rect = shop_text.get_rect(center=(640, 100))
        screen.blit(shop_text, shop_rect)

        back_button = Button(None, pos=(1000, 600),
                                base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                                text_input="Back", font=buttonfont, base_color=black, hovering_color=red)
        
        snow_power = Button(transform.scale(pygame.image.load("Sprites/snow.PNG").convert_alpha(),(72,72)), pos=(100, 600), 
                                base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                                text_input=None, font=buttonfont, base_color=black, hovering_color=red)
        double_power = Button(transform.scale(pygame.image.load("Sprites/double.PNG").convert_alpha(),(72,72)), pos=(150, 600), 
                                base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                                text_input=None, font=buttonfont, base_color=black, hovering_color=red)
        placeholder_power = Button(None, pos=(250, 600), 
                                base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                                text_input="Placeholder", font=buttonfont, base_color=black, hovering_color=red)

        for button in [back_button, snow_power, double_power, placeholder_power]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mousePos):
                        play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if snow_power.checkForInput(mousePos):
                        print("SNOW WORKS")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if double_power.checkForInput(mousePos):
                        print("DOUBLE WORKS")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if placeholder_power.checkForInput(mousePos):
                        print("PLACEHOLDER WORKS")
        
        pygame.display.update()  

def tutorial():
    while True:
        screen.fill(lightblue)

        tutorial_text = buttonfont.render("Let's learn how to play!", True, black)
        tutorial_rect = tutorial_text.get_rect(center=(640, 100))
        screen.blit(tutorial_text, tutorial_rect)
        
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        menu_button = Button(None, pos=(1000, 650), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Main Menu", font=buttonfont, base_color=black, hovering_color=red)
        skip_tutorial_button = Button(None, pos=(100, 650), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Skip Tutorial", font=buttonfont, base_color=black, hovering_color=red)
        
        for button in [menu_button, skip_tutorial_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mousePos):
                    main_menu()
                if skip_tutorial_button.checkForInput(mousePos):
                    play()

        pygame.display.update()

def play():
    while True:
        screen.fill(white)

        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        menu_button = Button(None, pos=(1000, 650), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Main Menu", font=buttonfont, base_color=black, hovering_color=red)
        shop_button = Button(None, pos=(400, 650), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Shop", font=buttonfont, base_color=black, hovering_color=red)
        next_round_button = Button(None, pos=(700, 650), 
                             base_screen_info=(1280, 720), game_size=GAME_SIZE, gen_coords=GEN_COORDS,
                             text_input="Next Round", font=buttonfont, base_color=black, hovering_color=red)

        for button in [menu_button, shop_button, next_round_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mousePos):
                    main_menu()
                if next_round_button.checkForInput(mousePos):
                    play()
                if shop_button.checkForInput(mousePos):
                    shop()

        # create our moles
        moles = [[None for _ in range(5)] for _ in range(5)]
        x = 1280/5
        y = 100
        for i in range(5):
            for j in range(5):
                moles[i][j] = Mole(x,y)
                x += (1280/5)/2
            x = 1280/5
            y += 100

        allmoles = Group(moles)
        allmoles.draw(screen)

        pygame.display.update()

main_menu()