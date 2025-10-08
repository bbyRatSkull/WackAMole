# Started on AUG 2025
import random
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
from button import Button
import moviepy.editor
import os
import os.path

# need for making .exe later
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Colors we want to use
lightbrown = (134, 94, 54)
darkbrown = (60,40,37)
pink = (250,110,121)
white = (255, 255, 255)
grey = (94, 91, 140)
black = (0, 0, 0)
lightgreen = (166, 203, 150)
darkgreen = (0, 101, 84)
orange = (222, 93, 58)
yellow = (243, 168, 51)

# create some fonts
settingsfont = pygame.font.SysFont('pixelsans', 38)
buttonfont = pygame.font.SysFont('pixelsans',54)
playfont = pygame.font.SysFont('pixelsans', 70)
shopfont = pygame.font.SysFont('pixelsans', 35)
timerfont = pygame.font.SysFont('vtf misterpixel', 50)
timerfont_bigger = pygame.font.SysFont('vtf misterpixel', 54)
initialsfont = pygame.font.SysFont('vtf misterpixel', 32)

#sound and chennels can be initialized here
#sounds themselves are defined in the function they wil be used in
#...this is so they do not play in slow motion :D
pygame.mixer.init()
music_channel = pygame.mixer.Channel(0)
sfx_channel = pygame.mixer.Channel(1)

pygame.init()
screenvar = pygame.display.get_desktop_sizes()
screen = pygame.display.set_mode((screenvar[0][0], screenvar[0][1]), FULLSCREEN)
#the screen ratio all object are placed to match / the base state
GAME_SIZE = (1504,846)
pygame.display.set_caption("Whack a Mole!")

moleabsent = transform.scale(image.load(resource_path("Resources/Sprites/hole_mound.PNG")).convert_alpha(), (225.6,225.6) )
molestage1 = transform.scale(image.load(resource_path("Resources/Sprites/mole_stage1.PNG")).convert_alpha(), (225.6,225.6))
molestage2 = transform.scale(image.load(resource_path("Resources/Sprites/mole_stage2.PNG")).convert_alpha(), (225.6,225.6))
molealive_s = transform.scale(image.load(resource_path("Resources/Sprites/mole_sb.PNG")).convert_alpha(), (225.6,225.6))
molealive_b = transform.scale(image.load(resource_path("Resources/Sprites/mole_bb.PNG")).convert_alpha(), (225.6,225.6))
molefrozen_s = transform.scale(image.load(resource_path("Resources/Sprites/frozen_sb.PNG")).convert_alpha(), (225.6,225.6))
molefrozen_b = transform.scale(image.load(resource_path("Resources/Sprites/frozen_bb.PNG")).convert_alpha(), (225.6,225.6))
moledead_s = transform.scale(image.load(resource_path("Resources/Sprites/red_splat.PNG")).convert_alpha(), (225.6,225.6))
moledead_b = transform.scale(image.load(resource_path("Resources/Sprites/blue_splat.PNG")).convert_alpha(), (225.6,225.6))
rabbitalive = transform.scale(image.load(resource_path("Resources/Sprites/snowdrop.PNG")).convert_alpha(), (225.6,225.6))
rabbitdead = transform.scale(image.load(resource_path("Resources/Sprites/snowdrop_ouch.PNG")).convert_alpha(), (225.6,225.6))

current_cursor = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_orange.PNG").convert_alpha(), (320,180))

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = moleabsent
        self.dead_image = moleabsent
        self.rect = self.image.get_rect().move(x,y)
        self.status = 'absent'

# create our moles
moles = [None for _ in range(9)]
moles[0] = Mole(80, 328) #top 1
moles[1] = Mole(216, 544) #bottom 1
moles[2] = Mole(494, 478) #bottom 2
moles[3] = Mole(348, 257) #top 2
moles[4] = Mole(643, 238) #top 3
moles[5] = Mole(939, 257) #top 4
moles[6] = Mole(794, 478) #bottom 3
moles[7] = Mole(1070, 544) #bottom 4
moles[8] = Mole(1207, 328) #top 5

allmoles = Group(moles)

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds (low=fast)
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

def update_jar(score):
    if score < 2:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_empty.PNG").convert_alpha(),(150,150))
    elif score >= 2 and score < 5:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_low.PNG").convert_alpha(),(150,150))
    elif score >=5 and score < 8:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_low_med.PNG").convert_alpha(),(150,150))
    elif score >= 8 and score < 12:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_med.PNG").convert_alpha(),(150,150))
    elif score >=12 and score <17:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_med_high.PNG").convert_alpha(),(150,150))
    elif score >= 17:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_full.PNG").convert_alpha(),(150,150))
    return(jar)

def intro_sequence():
    intro = moviepy.editor.VideoFileClip(resource_path("Resources/Backgrounds/Intro_video.mov"))
    intro_resized = intro.resize(newsize=(1504, 846))
    intro_resized.preview(fullscreen=True)

def main_menu(volume, music, current_cursor, inventory): #the main menu screen
    base_music = pygame.mixer.Sound(resource_path('Resources/Audio/cute_creatures.mp3'))
    base_music.set_volume(0.5)
    if music_channel.get_busy() is False and music is True:
        music_channel.play(base_music, -1)
    while True:
        screen.fill(black)
        # loads in image and scales it to screen size
        BG = transform.scale(pygame.image.load(resource_path("Resources/Backgrounds/BG_Menu.PNG")).convert(),GAME_SIZE)
        screen.blit(BG, BG.get_rect(center = screen.get_rect().center)) 

        mousePos = pygame.mouse.get_pos()

        play_button = Button(None, pos=(432,610), 
                             text_input="Play", font=buttonfont, base_color=darkbrown, hovering_color=pink)
        quit_button = Button(None, pos=(1250, 742), 
                             text_input="Quit", font=buttonfont, base_color=darkbrown, hovering_color=pink)
        settings_button = Button(transform.scale(pygame.image.load(resource_path("Resources/Sprites/gear.PNG")).convert_alpha(),(50,50)), pos=(1458, 118),
                                 text_input="", font=buttonfont, base_color=grey, hovering_color=grey)
        
        for button in [play_button, quit_button, settings_button]:
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
                    volume, music = tutorial(volume,music, current_cursor, inventory)
                if settings_button.checkForInput(mousePos):
                    volume, music, current_cursor, inventory = settings(volume, music, current_cursor, inventory)
                if quit_button.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  

def settings(volume, music, current_cursor, inventory):
    BG = transform.scale(pygame.image.load("Resources/Backgrounds/overlay.PNG").convert_alpha(),GAME_SIZE)
    screen.blit(BG, BG.get_rect(center = screen.get_rect().center))

    #the game_size will have to change to the size of the image * by the ratio from bkg old to bkg new
    #will also have to manually place... again... yay
    volume_on_image = pygame.image.load("Resources/Sprites/volume_on.PNG").convert_alpha()
    volume_off_image = pygame.image.load("Resources/Sprites/volume_off.PNG").convert_alpha()
    music_on_image = pygame.image.load("Resources/Sprites/music_on.PNG").convert_alpha()
    music_off_image = pygame.image.load("Resources/Sprites/music_off.PNG").convert_alpha()
    tutorial_sign_image = pygame.image.load("Resources/Sprites/tutorial_sign.PNG").convert_alpha()
    intro_sign_image = pygame.image.load("Resources/Sprites/intro_sign.PNG").convert_alpha()
    back_sign_image = pygame.image.load("Resources/Sprites/back_sign.PNG").convert_alpha()

    volume_button = Button(volume_on_image, pos=(1400,108),
                         text_input="Sounds      ", font=settingsfont, base_color=darkbrown, hovering_color=pink)
    music_button = Button(music_on_image, pos=(1400,190),
                         text_input="Music     ", font=settingsfont, base_color=darkbrown, hovering_color=pink)
    tutorial_button = Button(tutorial_sign_image, pos=(1400,265),
                         text_input="Tutorial", font=settingsfont, base_color=darkbrown, hovering_color=pink)
    intro_button = Button(intro_sign_image, pos=(1400,340),
                         text_input="Replay Intro", font=settingsfont, base_color=darkbrown, hovering_color=pink)
    back_button = Button(back_sign_image, pos=(1445,410),
                         text_input="Back", font=settingsfont, base_color=darkbrown, hovering_color=pink)

    while True: 
        mousePos = pygame.mouse.get_pos()

        #trying to get an image to appear behind the buttons
        #screen.blit(myimage, (1458, 118))
        if volume is False:
            volume_button.image = volume_off_image
        if music is False:
            music_button.image = music_off_image

        for button in [volume_button, music_button, tutorial_button, intro_button, back_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return volume, music, current_cursor, inventory
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_button.checkForInput(mousePos):
                    if volume is False:
                        volume = True
                        volume_button.image = volume_on_image
                        sfx_channel.unpause()
                    else: 
                        volume = False
                        volume_button.image = volume_off_image
                        sfx_channel.pause()
                    volume_button.update(screen)
                if music_button.checkForInput(mousePos):
                    if music is False:
                        music = True
                        music_button.image = music_on_image
                        music_channel.unpause()
                    else: 
                        music = False
                        music_button.image = music_off_image
                        music_channel.pause()
                if tutorial_button.checkForInput(mousePos):
                    volume, music, current_cursor, inventory = tutorial(volume,music, current_cursor, inventory)
                    return volume, music, current_cursor, inventory
                if intro_button.checkForInput(mousePos):
                    intro_sequence()
                    main_menu(volume, music, current_cursor, inventory)
                if back_button.checkForInput(mousePos):
                    return volume, music, current_cursor, inventory

        pygame.display.update()  

def shop(volume,music, current_cursor, inventory):
    pie_image = transform.scale(pygame.image.load("Resources/Sprites/pie.PNG").convert_alpha(), (80,80))

    settings_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 118),
                             text_input="", font=buttonfont, base_color=grey, hovering_color=grey)
    back_button = Button(transform.scale(pygame.image.load("Resources/Sprites/back_arrow.PNG").convert_alpha(),(68,68)), pos=(54, 118),
                             text_input="", font=buttonfont, base_color=black, hovering_color=white)
    next_button = Button(transform.scale(pygame.image.load("Resources/Sprites/next_arrow.PNG").convert_alpha(),(50,50)), pos=(944,438),
                         text_input="", font=shopfont, base_color=darkbrown, hovering_color=pink)
    yes_button = Button(transform.scale(pygame.image.load("Resources/Sprites/yes.PNG").convert_alpha(),(50,50)), pos=(944,438),
                         text_input="", font=shopfont, base_color=darkbrown, hovering_color=pink)
    no_button = Button(transform.scale(pygame.image.load("Resources/Sprites/no.PNG").convert_alpha(),(50,50)), pos=(855,438),
                         text_input="", font=shopfont, base_color=darkbrown, hovering_color=pink)   

    speech_bubble = pygame.image.load("Resources/Sprites/speech_bubble.PNG").convert_alpha()
        
    snow_power = Button(pygame.image.load("Resources/Sprites/snow_shop.PNG").convert_alpha(), pos=(587, 549), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    double_power = Button(pygame.image.load("Resources/Sprites/double_shop.PNG").convert_alpha(), pos=(359, 490), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    hourglass_power = Button(pygame.image.load("Resources/Sprites/hourglass_shop.PNG").convert_alpha(), pos=(442, 524), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    bell_power = Button(pygame.image.load("Resources/Sprites/bell_shop.PNG").convert_alpha(), pos=(467, 433), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
        
    red_paint = Button(pygame.image.load("Resources/Sprites/red_paint.PNG").convert_alpha(), pos=(1078, 490), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    orange_paint = Button(pygame.image.load("Resources/Sprites/orange_paint.PNG").convert_alpha(), pos=(1110, 551), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    green_paint = Button(pygame.image.load("Resources/Sprites/green_paint.PNG").convert_alpha(), pos=(1078, 308), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    teal_paint = Button(pygame.image.load("Resources/Sprites/teal_paint.PNG").convert_alpha(), pos=(1158, 368), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    blue_paint = Button(pygame.image.load("Resources/Sprites/blue_paint.PNG").convert_alpha(), pos=(1158, 490), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    purple_paint = Button(pygame.image.load("Resources/Sprites/purple_paint.PNG").convert_alpha(), pos=(1110, 368), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    pink_paint = Button(pygame.image.load("Resources/Sprites/pink_paint.PNG").convert_alpha(), pos=(1195, 551), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    black_paint = Button(pygame.image.load("Resources/Sprites/black_paint.PNG").convert_alpha(), pos=(1195, 430), 
                             text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    
    red_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_red.PNG").convert_alpha(), (320,180))
    orange_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_orange.PNG").convert_alpha(), (320,180))
    green_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_green.PNG").convert_alpha(), (320,180)) 
    teal_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_teal.PNG").convert_alpha(), (320,180))
    blue_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_blue.PNG").convert_alpha(), (320,180))
    purple_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_purple.PNG").convert_alpha(), (320,180))
    pink_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_pink.PNG").convert_alpha(), (320,180))
    black_hammer = transform.scale(pygame.image.load("Resources/Sprites/hammer_cursor_black.PNG").convert_alpha(), (320,180))

    screen.fill(black)
    BG = transform.scale(pygame.image.load(resource_path("Resources/Backgrounds/BG_Shop.PNG")).convert(),GAME_SIZE)

    line1_text = "Well hello!"
    line2_text = "Welcome to"
    line3_text = "my shop."
    line4_text = ""
    dialogue = True
    item_clicked = False
    current_power = None
    pending_cursor = None
    cost = 9999

    while True:    
        screen.blit(BG, BG.get_rect(center = screen.get_rect().center)) 
        screen.blit(pie_image, (24, 835))
        screen.blit(timerfont.render("=" + str(inventory[0][1]), True, darkbrown), (110, 850))
        
        screen.blit(speech_bubble, (800,270))

        shop_text1 = shopfont.render(line1_text, True, darkbrown)
        shop_rect1 = shop_text1.get_rect(center=(640, 100))
        screen.blit(shop_text1, (552+(shop_rect1[0]/2),285))

        shop_text2 = shopfont.render(line2_text, True, darkbrown)
        shop_rect2 = shop_text2.get_rect(center=(640, 100))
        screen.blit(shop_text2, (552+(shop_rect2[0]/2),310))

        shop_text3 = shopfont.render(line3_text, True, darkbrown)
        shop_rect3 = shop_text3.get_rect(center=(640, 100))
        screen.blit(shop_text3, (552+(shop_rect3[0])/2,335))

        shop_text4 = shopfont.render(line4_text, True, darkbrown)
        shop_rect4 = shop_text4.get_rect(center=(640, 100))
        screen.blit(shop_text4, (552+(shop_rect4[0]/2),360))

        mousePos = pygame.mouse.get_pos()

        for button in [back_button, settings_button, snow_power, double_power, hourglass_power, bell_power,
                       red_paint, orange_paint, green_paint, teal_paint, blue_paint, purple_paint, pink_paint, black_paint]:
            button.changeColor(mousePos)
            button.update(screen)
        if dialogue:
            for button in [next_button]:
                button.changeColor(mousePos)
                button.update(screen)
                no_button.enabled = False
                yes_button.enabled = False
        elif not item_clicked:
            for button in [no_button, yes_button, next_button]:
                button.enabled = False
        if item_clicked: 
            for button in [no_button, yes_button]:
                button.enabled = True
                button.changeColor(mousePos)
                button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return volume, music, current_cursor, inventory
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mousePos):
                    volume, music, current_cursor, inventory = play(volume, music, current_cursor, inventory)

                if settings_button.checkForInput(mousePos):
                    volume, music, current_cursor, inventory = settings(volume, music, current_cursor, inventory)
                if snow_power.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "I so do love"
                    line2_text = "the snow!"
                    line3_text = "I'll trade you"
                    line4_text = "six pies?"
                    current_power = "snow"
                    cost = 6
                if double_power.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "It's like I'm"
                    line2_text = "seeing double!"
                    line3_text = "I'll trade you"
                    line4_text = "four pies?"
                    current_power = "double"
                    cost = 4
                if hourglass_power.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "More time is"
                    line2_text = "a luxury here."
                    line3_text = "I'll trade you"
                    line4_text = "three pies?"
                    current_power = "hourglass"
                    cost = 3
                if bell_power.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "A bell's not a"
                    line2_text = "bell 'til it's rung."
                    line3_text = "I'll trade you"
                    line4_text = "two pies?"
                    current_power = "bell"
                    cost = 2

                if red_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "red paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = red_hammer
                    cost = 1
                if orange_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "orange paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = orange_hammer
                    cost = 1
                if green_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "green paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = green_hammer
                    cost = 1
                if teal_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "teal paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = teal_hammer
                    cost = 1
                if blue_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "blue paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = blue_hammer
                    cost = 1
                if purple_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "purple paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = purple_hammer
                    cost = 1
                if pink_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "pink paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = pink_hammer
                    cost = 1
                if black_paint.checkForInput(mousePos):
                    item_clicked = True
                    dialogue = False
                    line1_text = "Nice! That's"
                    line2_text = "black paint."
                    line3_text = "I'll trade you"
                    line4_text = "one pie?"
                    pending_cursor = black_hammer
                    cost = 1

                if next_button.checkForInput(mousePos):
                    if line1_text == "Well hello!":
                        line1_text = "Just call me"
                        line2_text = "Granny Plum."
                        line3_text = "It's very nice"
                        line4_text = "to see you!"
                    elif line1_text == "Just call me":
                        line1_text = "Do you"
                        line2_text = "see anything"
                        line3_text = "that you like?"
                        line4_text = ""
                        dialogue = False

                if yes_button.checkForInput(mousePos):
                    if pending_cursor is not None and inventory[0][1] >= cost:
                        current_cursor = pending_cursor
                        inventory[0][1] -= cost
                        line1_text = ""
                        line2_text = "Alrighty roo!"
                        line3_text = "Thank you!"
                        line4_text = ""
                        item_clicked = False
                        pending_cursor = None
                    elif current_power is not None and inventory[0][1] >= cost:
                        inventory[0][1] -= cost
                        for item in inventory:
                            if item[0] == current_power:
                                i = inventory.index(item)
                                inventory[i][1] += 1
                        line1_text = ""
                        line2_text = "Alrighty roo!"
                        line3_text = "Thank you!"
                        line4_text = ""
                        item_clicked = False
                        current_power = None
                    else: 
                        line1_text = "Oh, I'm sorry."
                        line2_text = "You don't have"
                        line3_text = "enough for"
                        line4_text = "that, Dear."
                        item_clicked = False
                        current_power = None
                        pending_cursor = None
                if no_button.checkForInput(mousePos):
                    line1_text = "Oh, okay."
                    line2_text = "No problem,"
                    line3_text = "Dear."
                    line4_text = ""
                    pending_cursor = current_cursor
                    item_clicked = False
                    current_power = None
                    pending_cursor = None
        
        pygame.display.update()  

def tutorial(volume,music, current_cursor, inventory):
    while True:
        screen.fill(pink)

        tutorial_text = buttonfont.render("Let's learn how to play!", True, black)
        tutorial_rect = tutorial_text.get_rect(center=(640, 100))
        screen.blit(tutorial_text, tutorial_rect)
        
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        menu_button = Button(None, pos=(1000, 650), 
                             text_input="Main Menu", font=buttonfont, base_color=black, hovering_color=white)
        skip_tutorial_button = Button(None, pos=(100, 650), 
                             text_input="Skip Tutorial", font=buttonfont, base_color=black, hovering_color=white)
        
        for button in [menu_button, skip_tutorial_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return volume, music
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mousePos):
                    main_menu(volume, music, current_cursor, inventory)
                if skip_tutorial_button.checkForInput(mousePos):
                    volume, music = play(volume,music, current_cursor, inventory)

        pygame.display.update()

def play(volume,music, current_cursor, inventory):
    gameStarted = False
    gameCompleted = False
    hardmode = False
    time_added = 0
    doubling = False
    time_at_double = 0

    #higher odds = appears less often
    aliveodds = 10
    absentodds = 3
    halfupodds = 20
    rabbitodds = 7

    for i in range(9):
        moles[i].image = moleabsent
        moles[i].status = 'absent'
        
    back_button = Button(transform.scale(pygame.image.load("Resources/Sprites/back_arrow.PNG").convert_alpha(),(68,68)), pos=(54, 118),
                             text_input="", font=buttonfont, base_color=black, hovering_color=white)
    shop_button = Button(None, pos=(890, 850), 
                         text_input="Shop", font=playfont, base_color=darkbrown, hovering_color=pink)
    start_button = Button(None, pos=(610, 850), 
                         text_input="Start", font=playfont, base_color=darkbrown, hovering_color=pink)
    mode_button = Button(None, pos=(730, 890), 
                         text_input="Hard Mode =", font=settingsfont, base_color=darkbrown, hovering_color=pink)
    settings_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 118),
                         text_input="", font=buttonfont, base_color=grey, hovering_color=grey)
    
    snow_power = Button(transform.scale(pygame.image.load("Resources/Sprites/snow.PNG").convert_alpha(),(96,96)), pos=(970, 860), 
                         text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    double_power = Button(transform.scale(pygame.image.load("Resources/Sprites/double.PNG").convert_alpha(),(96,96)), pos=(830, 860), 
                         text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    bell_power = Button(transform.scale(pygame.image.load("Resources/Sprites/bell.PNG").convert_alpha(),(96,96)), pos=(550, 860), 
                         text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    hourglass_power = Button(transform.scale(pygame.image.load("Resources/Sprites/hourglass.PNG").convert_alpha(),(96,96)), pos=(690, 860), 
                         text_input=None, font=buttonfont, base_color=black, hovering_color=white)
    
    heart_full = transform.scale(image.load(resource_path("Resources/Sprites/heart_full.PNG")).convert_alpha(), (50, 50))
    heart_empty = transform.scale(image.load(resource_path("Resources/Sprites/heart_empty.PNG")).convert_alpha(), (50, 50))

    mode_string = "OFF"
    #sfx and music
    bonk = pygame.mixer.Sound(resource_path('Resources/Audio/bonk.mp3'))
    gameover = pygame.mixer.Sound(resource_path('Resources/Audio/gameover.mp3'))
    buzzer = pygame.mixer.Sound(resource_path('Resources/Audio/buzzer.mp3'))
    buzzer.set_volume(.40)
    power_up = pygame.mixer.Sound(resource_path('Resources/Audio/power_up.mp3'))
    power_up.set_volume(0.55)
    bell = pygame.mixer.Sound(resource_path('Resources/Audio/bell.mp3'))
    sand = pygame.mixer.Sound(resource_path('Resources/Audio/sand.mp3'))
    sand.set_volume(0.9)
    icy = pygame.mixer.Sound(resource_path('Resources/Audio/icy.mp3'))
    play_music = pygame.mixer.Sound(resource_path('Resources/Audio/play_music.mp3'))
    play_music.set_volume(0.7)
    base_music = pygame.mixer.Sound(resource_path('Resources/Audio/cute_creatures.mp3'))
    base_music.set_volume(0.5)
    if music_channel.get_busy() is False and music is True:
        music_channel.play(base_music, -1)

    # loads in image and scales it to screen size
    BG = transform.scale(pygame.image.load("Resources/Backgrounds/BG_Play.PNG").convert(),GAME_SIZE)
    while True:
        snow_text = shopfont.render(str(inventory[4][1]), True, darkbrown)
        double_text = shopfont.render(str(inventory[3][1]), True, darkbrown)
        bell_text = shopfont.render(str(inventory[1][1]), True, darkbrown)
        hourglass_text = shopfont.render(str(inventory[2][1]), True, darkbrown)

        mode_text = settingsfont.render(mode_string, True, darkbrown)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if gameStarted:
                        if volume is True:
                            sfx_channel.play(gameover)
                        gameStarted = False
                        for i in range(9):
                            moles[i].image = moleabsent
                            moles[i].status = 'absent'
                    gameCompleted = False
                    pygame.mouse.set_visible(True)
                    if music is True:
                        music_channel.play(base_music)
                    main_menu(volume, music, current_cursor, inventory)

            # find mouse position
            mousePos = pygame.mouse.get_pos()
            mousex = mousePos[0]
            mousey = mousePos[1]

            if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set moles to be up or down
                if gameStarted:
                    secondsRemaining -= 1
                    for i in range(9):
                        # if mole was absent, randomly makeit alive
                        if moles[i].status == 'absent':
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                moles[i].status = 'alive'
                                r = random.randint(0,rabbitodds)
                                if r == 1:
                                    moles[i].image = rabbitalive
                                    moles[i].dead_image = rabbitdead
                                    moles[i].status = 'rabbitalive'
                                elif r%2 == 0:
                                    moles[i].image = molealive_s
                                    moles[i].dead_image = moledead_s
                                else: 
                                    moles[i].image = molealive_b
                                    moles[i].dead_image = moledead_b
                            elif hardmode:
                                #this is all the code for half up and a vairalbe at the top -- might be confusing?? 
                                r = random.randint(1, halfupodds)
                                if r == 1:
                                    moles[i].image = molestage1
                                elif r == 2:
                                    moles[i].image = molestage2
                                else:
                                    moles[i].image = moleabsent
                        # if alive, randomly make it absent
                        elif moles[i].status == 'alive' or moles[i].status == 'rabbitalive':
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i].status = 'absent'
                                moles[i].image = moleabsent
                        elif moles[i].status == 'dead':
                            moles[i].status = 'absent'
                            moles[i].image = moleabsent

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mousePos):
                    if gameStarted:
                        if volume is True:
                            sfx_channel.play(gameover)
                        for i in range(9):
                            moles[i].image = moleabsent
                            moles[i].status = 'absent'
                        gameStarted = False
                    gameCompleted = False
                    pygame.mouse.set_visible(True)
                    if music is True:
                        music_channel.play(base_music)
                    main_menu(volume, music, current_cursor, inventory)
                if shop_button.checkForInput(mousePos):
                    volume, music, current_cursor, inventory = shop(volume,music, current_cursor, inventory)
                if settings_button.checkForInput(mousePos):
                    pygame.mouse.set_visible(True)
                    volume, music, current_cursor, inventory = settings(volume, music, current_cursor, inventory)
                    pygame.mouse.set_visible(False)
                if mode_button.checkForInput(mousePos):
                    if hardmode:
                        hardmode = False
                        mode_string = "OFF"
                    else:
                        hardmode = True
                        mode_string = "ON"
                if start_button.checkForInput(mousePos):
                    gameStarted = True
                    heart1 = True
                    heart2 = True
                    heart3 = True
                    secondsRemaining = 20
                    score = 0
                    pygame.mouse.set_visible(False)
                    cursor_image = current_cursor
                    cursor_rect = cursor_image.get_rect()
                    if music is True:
                        music_channel.play(play_music, -1)
                if bell_power.checkForInput(mousePos):
                    if inventory[1][1] > 0:
                        inventory[1][1] -= 1
                        aliveodds = 1
                        absentodds = 10
                        sfx_channel.play(bell)
                if hourglass_power.checkForInput(mousePos):
                    if inventory[2][1] > 0:
                        inventory[2][1] -= 1
                        secondsRemaining += 20
                        if doubling is True:
                            time_added += 20
                        sfx_channel.play(sand)
                if double_power.checkForInput(mousePos):
                    if inventory[3][1] > 0:
                        inventory[3][1] -= 1
                        doubling = True
                        time_at_double = secondsRemaining
                    sfx_channel.play(power_up)
                if snow_power.checkForInput(mousePos):
                    if inventory[4][1] > 0:
                        inventory[4][1] -= 1
                        for i in range(9):
                            if moles[i].status == "alive":
                                if moles[i].image == molealive_s:
                                    moles[i].image = molefrozen_s
                                else:
                                    moles[i].image = molefrozen_b
                                moles[i].status = 'frozen'
                        sfx_channel.play(icy)

                if gameStarted:
                    if music is True and music_channel.get_busy() is False:
                        music_channel.play(play_music, -1)
                    for i in range(9):
                        if mousex >= moles[i].x and mousex <= moles[i].x + 225.6 and \
                            mousey >= moles[i].y and mousey <= moles[i].y + 225.6:
                            if moles[i].status == 'alive' or moles[i].status == 'frozen':
                                if volume is True:
                                    sfx_channel.play(bonk)
                                moles[i].image = moles[i].dead_image
                                moles[i].status = 'dead'
                                if doubling is True:
                                    score += 1
                                    if hardmode is True:
                                        score += 1
                                score += 1
                                if hardmode is True:
                                    score += 1
                                if aliveodds == 1:
                                    aliveodds = 10
                                    absentodds = 3
                            elif moles[i].status == 'rabbitalive':
                                moles[i].image = moles[i].dead_image
                                moles[i].status = 'dead'
                                if volume is True:
                                    sfx_channel.play(buzzer)
                                if heart1: 
                                    heart1 = False
                                elif heart2: 
                                    heart2 = False
                                elif heart3: 
                                    heart3 = False
                                    gameStarted = False
                                    score = -9999
                                    for i in range(9):
                                        moles[i].image = moleabsent
                                        moles[i].status = 'absent'
                                    gameCompleted = True
                                    if volume is True:
                                        sfx_channel.play(gameover)
                                    pygame.mouse.set_cursor(pygame.cursors.Cursor())
                                    
                                if doubling is True:
                                    if hardmode is True:
                                        score -= 1
                                    score -= 1
                                if hardmode is True:
                                    score -= 1
                                score -= 1
                            else:
                                moles[i].image = moleabsent
                                if volume is True:
                                    sfx_channel.play(buzzer)
                                if doubling is True:
                                    if hardmode is True:
                                        score -= 1
                                    score -= 1
                                if hardmode is True:
                                    score -= 1
                                score -= 1
            
            #This has to be here, not sure why, but now it doesnt "glitch"
            screen.fill(black)
            # blits the image to the center of the surface "screen"
            screen.blit(BG, BG.get_rect(center = screen.get_rect().center))

            allmoles.draw(screen)

            if gameStarted:
                for button in [back_button, settings_button, snow_power, double_power, bell_power, hourglass_power]:
                    button.changeColor(mousePos)
                    button.update(screen)
                for button in [shop_button, start_button, mode_button]:
                    button.enabled = False
                for button in [bell_power, hourglass_power, double_power, snow_power]:
                    button.enabled = True
                screen.blit(bell_text, (580, 805))
                screen.blit(hourglass_text, (730, 805))
                screen.blit(double_text, (880, 805))
                screen.blit(snow_text, (1004, 805))

                if heart1: screen.blit(heart_full, (255, 850))
                else: screen.blit(heart_empty, (255, 850))
                if heart2 : screen.blit(heart_full, (315, 850))
                else: screen.blit(heart_empty, (315, 850))
                if heart3 : screen.blit(heart_full, (375, 850))
                else: screen.blit(heart_empty, (375, 850))

                minutes = str(secondsRemaining // 60)
                seconds = str(secondsRemaining % 60)
                if len(minutes) < 2:
                    minutes = "0" + minutes
                if len(seconds) < 2:
                    seconds = "0" + seconds
                    
                timerText = timerfont.render(minutes + ":" + seconds, True, white, None)
                timerRect = timerText.get_rect()
                timerRect.center = (150, 600)
                if doubling:
                    timerText = timerfont.render(minutes + ":" + seconds +" x2", True, yellow, None)
                    timerRect2 = timerText.get_rect()
                    timerRect2.center = (150, 600)
                    timerText2 = timerfont_bigger.render(minutes + ":" + seconds +" x2", True, orange, None)
                    screen.blit(timerText2, (750-timerRect[0],68))
                screen.blit(timerText, (756-timerRect[0],68))
            
                jar = update_jar(score)
                screen.blit(jar, (1350, 740))

                cursor_rect.center = pygame.mouse.get_pos()
                screen.blit(cursor_image, (cursor_rect[0] + 138, cursor_rect[1]-2))

                if secondsRemaining == 0:
                    gameStarted = False
                    for i in range(9):
                        moles[i].image = moleabsent
                        moles[i].status = 'absent'
                    gameCompleted = True
                    #idk if this next line is needed
                    pygame.mouse.set_cursor(pygame.cursors.Cursor())
            
                if time_at_double - 10 + time_added == secondsRemaining:
                    doubling = False

            else: 
                pygame.mouse.set_visible(True)

                for button in [back_button, shop_button, start_button, settings_button, mode_button]:
                    button.changeColor(mousePos)
                    button.update(screen)
                for button in [back_button, shop_button, start_button, settings_button, mode_button]:
                    button.enabled = True
                for button in [bell_power, hourglass_power, double_power, snow_power]:
                    button.enabled = False
                screen.blit(mode_text, (803, 872))

                if gameCompleted:
                    if volume is True:
                        sfx_channel.play(gameover)
                    game_finished(volume, music, current_cursor, inventory, score)
                    gameCompleted = False



        pygame.display.update()

def game_finished(volume, music, current_cursor, inventory, score):
    current_input = ""
    asking = False
    did_ask = False
    
    pie_image = transform.scale(pygame.image.load("Resources/Sprites/pie.PNG").convert_alpha(), (125,125))
    pie_positions = [(55, 430), (180, 430), (305, 430), (430, 430), (55, 266), (180, 266), (305, 266), (430, 266)]
    pies_earned = score // 8
    if score > 0:
        inventory[0][1] += pies_earned

    kitchen_music = pygame.mixer.Sound(resource_path('Resources/Audio/kitchen_music.mp3'))
    kitchen_music.set_volume(0.9)
    base_music = pygame.mixer.Sound(resource_path('Resources/Audio/cute_creatures.mp3'))
    base_music.set_volume(0.5)
    if music is True:
        music_channel.play(kitchen_music, -1)

    screen.fill(black)
    # loads in image and scales it to screen size
    BG = transform.scale(pygame.image.load("Resources/Backgrounds/BG_Final.PNG").convert(),GAME_SIZE)
    OVERLAY = transform.scale(pygame.image.load("Resources/Backgrounds/overlay.PNG").convert_alpha(),GAME_SIZE)

    continue_button = Button(transform.scale(pygame.image.load("Resources/Sprites/back_arrow.PNG").convert_alpha(),(68,68)), pos=(64, 118), 
                 text_input="", font=buttonfont, base_color=black, hovering_color=white)
    
    line1_text = ""
    line2_text = ""

    #gets the user's home directory. works on macOS, Linux, Windows
    home_dir = os.path.expanduser("~")
    #creates a path to the folder the txt file will go in
    folder_path = os.path.join(home_dir, "WackAMole", "highscores.txt")
    #creates the directory for the folder if it does not already exist
    os.makedirs(folder_path, exist_ok=True)
    #defined the path to the txt file
    file_path = os.path.join(folder_path, "highscores.txt")

    highscores = [x for x in range(4)]
    try: #will work if the file exists/ has been written in
        with open(file_path, "r") as file:
            x = -1
            for line in file:
                x += 1
                (name, round_score) = line.strip().split(": ")
                highscores[x] = (name, round_score)

    except Exception: #will run if the file has not been written in yet
        #this writes in 0 scores for all 5 possible highscores. Will overwrite data in the file
        with open(file_path, "w") as file:
            for i in range(4):
                file.write("000: 000\n")
        #same code as above, will correctly run this time
        with open(file_path, "r") as file:
            x = -1
            for line in file:
                x += 1
                (name, round_score) = line.strip().split(": ")
                highscores[x] = (name, round_score)

    if pies_earned > 0 and pies_earned > int(highscores[3][1]):
        asking = True
        did_ask = True

    while True:
        mousePos = pygame.mouse.get_pos()
        screen.blit(BG, BG.get_rect(center = screen.get_rect().center))

        if did_ask:
            text4 = settingsfont.render("Wow, you got a top score!", True, darkgreen, lightgreen)
            screen.blit(text4, (640, 496))
        if asking:
            prompt = settingsfont.render(" Enter your initials: ", True, darkgreen, lightgreen)
            input_box = settingsfont.render(current_input, True, darkgreen, lightgreen)
            screen.blit(prompt, (925, 496))
            screen.blit(input_box, (1145, 496))

        continue_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if music is True:
                        music_channel.play(base_music)
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.checkForInput(mousePos):
                    if music is True:
                        music_channel.play(base_music)
                    return
            
            # maybe only do this is their score is able to be a highscore
            #for typing
            if event.type == pygame.KEYDOWN and asking:
                #if enter is clicked, save name and score
                if event.key == pygame.K_RETURN:
                    if len(current_input) == 2:
                        current_input += " "
                    elif len(current_input) == 1:
                        current_input += "  "
                    else:
                        current_input += "---" 
                    with open(file_path, "a") as file:
                        file.write(f"{current_input}: {int(pies_earned)}\n")
                    print(f"Saved: {current_input} - {int(pies_earned)}")
                    asking = False
                    #resort highscores
                    manage_highscores(file_path)
                    #grab the new top scores
                    with open(file_path, "r") as file:
                        x = -1
                        for line in file:
                            x += 1
                            (name, round_score) = line.strip().split(": ")
                            highscores[x] = (name, round_score)

                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    if len(current_input) < 3:  #limit to 3 intials only
                        current_input += event.unicode.upper()
        
        if pies_earned > 0:
            for i in range(pies_earned):
                if i == 8:
                    break
                screen.blit(pie_image, pie_positions[i])

            if pies_earned > 8:
                line1_text = "Good job! You collected enough jam to make " + str(pies_earned) + " pies."
                line2_text = "You even ran out of room with that many!"
            else:
                line1_text = "Good job! You collected enough jam to make " + str(pies_earned) + " pies."
                line2_text = "Mmm. Smells yummy!"

        elif score > -9990:
            #better luck next time
            line1_text = "Awe, looks like you couldn't get enough jam for a pie."
            line2_text = "Better luck next time."
        else:
            #bad ending, hit rabbits to get here
            line1_text = "Oh no! Poor snowdrop!"
            line2_text = "Be more careful not to hit her next time."
        
        text = settingsfont.render(line1_text, True, darkbrown, lightbrown)
        screen.blit(text, (650,130))
        text2 = settingsfont.render(line2_text, True, darkbrown, lightbrown)
        screen.blit(text2, (658,165))
        text4 = shopfont.render("Most Pies Baked", True, grey)
        screen.blit(text4, (1240, 315))
        names_lines = [["","",""] for x in range(4)]
        scores_lines = [0 for x in range(4)]
        #currently does work for one two or three digits of score, will not do the same for initials. 
        #maybe hard lock in the initials in the above bit where theire typing it
        for i in range(4):
            screen.blit(initialsfont.render(":", True, darkgreen), (1355, 378+(i*40)))
            try:
                names_lines[i][0] = initialsfont.render(highscores[i][0][0], True, darkgreen)
                names_lines[i][1] = initialsfont.render(highscores[i][0][1], True, darkgreen)
                names_lines[i][2] = initialsfont.render(highscores[i][0][2], True, darkgreen)
                scores_lines[i] = initialsfont.render(highscores[i][1][0] + "   " + highscores[i][1][1] + "   " + highscores[i][1][2], True, darkgreen)
                screen.blit(names_lines[i][0], (1230, 379+(i*40)))
                screen.blit(names_lines[i][1], (1272, 379+(i*40)))
                screen.blit(names_lines[i][2], (1315, 379+(i*40)))
                screen.blit(scores_lines[i], (1365, 378+(i*40)))
            except Exception:
                try:
                    names_lines[i][0] = initialsfont.render(highscores[i][0][0], True, darkgreen)
                    names_lines[i][1] = initialsfont.render(highscores[i][0][1], True, darkgreen)
                    names_lines[i][2] = initialsfont.render(highscores[i][0][2], True, darkgreen)
                    scores_lines[i] = initialsfont.render(highscores[i][1][0] + "   " + highscores[i][1][1], True, darkgreen)
                    screen.blit(names_lines[i][0], (1230, 379+(i*40)))
                    screen.blit(names_lines[i][1], (1272, 379+(i*40)))
                    screen.blit(names_lines[i][2], (1315, 379+(i*40)))
                    screen.blit(scores_lines[i], (1365, 378+(i*40)))
                except Exception:
                    names_lines[i][0] = initialsfont.render(highscores[i][0][0], True, darkgreen)
                    names_lines[i][1] = initialsfont.render(highscores[i][0][1], True, darkgreen)
                    names_lines[i][2] = initialsfont.render(highscores[i][0][2], True, darkgreen)                    
                    scores_lines[i] = initialsfont.render(highscores[i][1][0], True, darkgreen)
                    screen.blit(names_lines[i][0], (1230, 379+(i*40)))
                    screen.blit(names_lines[i][1], (1272, 379+(i*40)))
                    screen.blit(names_lines[i][2], (1315, 379+(i*40)))
                    screen.blit(scores_lines[i], (1365, 378+(i*40)))

        if score <= -9990:
            screen.blit(OVERLAY, OVERLAY.get_rect(center = screen.get_rect().center))
            text = settingsfont.render(line1_text, True, black)
            screen.blit(text, (650,130))
            text2 = settingsfont.render(line2_text, True, black)
            screen.blit(text2, (658,165))
            continue_button.update(screen)
        pygame.display.update()

def manage_highscores(file_path):
    highscores = []
    #read in existing scores
    with open(file_path, "r") as file:
        for line in file:
            entry = line.strip().split(": ")
            name = entry[0]
            score = int(entry[1])
            highscores.append((name, score))

    top_scores = sorted(highscores, key=lambda x: x[1], reverse=True)[:4]

    #rewrite top 4 to file
    with open(file_path, "w") as file:
        for entry in top_scores:
            file.write(f"{entry[0]}: {entry[1]}\n")

game_finished(volume= True, music= True, current_cursor=current_cursor, inventory = [["pies", 20],["bell", 0],["hourglass", 0],["double", 1],["snow", 0]], score=-9990)

intro_sequence()

# For demo purposes, pies is set to 20
main_menu(volume= True, music= True, current_cursor=current_cursor, inventory = [["pies", 20],["bell", 5],["hourglass", 5],["double", 5],["snow", 5]])