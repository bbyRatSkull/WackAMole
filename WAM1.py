# Started on AUG 2025
import random
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
from button import Button
import moviepy.editor

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Colors we want to use
darkbrown = (60,40,37)
pink = (250,110,121)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# create some fonts
headerfont = pygame.font.SysFont('helveticaneue', 48)
buttonfont = pygame.font.SysFont('helveticaneue',30)
headerfont.set_bold(True)

# Sounds we want to use
pygame.mixer.init()
#hitsound = pygame.mixer.Sound('hit.wav')
#buzzer = pygame.mixer.Sound('buzzer.wav')
#gameover = pygame.mixer.Sound('gameover.mp3')

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
moledead = transform.scale(image.load(resource_path("Resources/Sprites/red_splat.PNG")).convert_alpha(), (225.6,225.6))
rabbitalive = transform.scale(image.load(resource_path("Resources/Sprites/snowdrop.PNG")).convert_alpha(), (225.6,225.6))
rabbitdead = transform.scale(image.load(resource_path("Resources/Sprites/snowdrop_ouch.PNG")).convert_alpha(), (225.6,225.6))

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = moleabsent
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
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

#this does not work and I may murder
#animation_list_mole = [moleabsent, molestage1, molestage2, molealive_s]
#last_update = pygame.time.get_ticks()
#animation_cooldown = 500
#frame = 0

#current_time = pygame.time.get_ticks()
#if current_time - last_update >= animation_cooldown:
#    frame += 1
#    last_update = current_time
#    screen.blit(animation_list_mole[frame])
# the above does not work and murder is feasable 

def update_jar(score):
    if score < 2:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_empty.PNG").convert_alpha(),(150,150))
    elif score >= 2 and score < 5:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_low.PNG").convert_alpha(),(150,150))
    elif score >=5 and score < 8:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_low_med.PNG").convert_alpha(),(150,150))
    elif score >= 8 and score < 12:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_med.PNG").convert_alpha(),(150,150))
    elif score <=12 and score <17:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_med_high.PNG").convert_alpha(),(150,150))
    elif score >= 17:
        jar = transform.scale(pygame.image.load("Resources/Sprites/jar_high.PNG").convert_alpha(),(150,150))
    return(jar)

def intro_sequence():
    intro = moviepy.editor.VideoFileClip("Resources/Backgrounds/Intro_video.mov")
    intro_resized = intro.resize(newsize=(1504, 846))
    intro_resized.preview(fullscreen=True)

def main_menu(): #the main menu screen
    while True:
        screen.fill(black)
        # loads in image and scales it to screen size
        BG = transform.scale(pygame.image.load("Resources/Backgrounds/BG_Menu.PNG").convert(),GAME_SIZE)
        screen.blit(BG, BG.get_rect(center = screen.get_rect().center)) 
        

        mousePos = pygame.mouse.get_pos()

        play_button = Button(None, pos=(431.7,612.025), 
                             text_input="Play", font=buttonfont, base_color=darkbrown, hovering_color=pink)
        quit_button = Button(None, pos=(1248.325, 744.8), 
                             text_input="Quit", font=buttonfont, base_color=darkbrown, hovering_color=pink)
        settings_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 118),
                                 text_input="", font=buttonfont, base_color=white, hovering_color=white)

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
                    tutorial()
                if settings_button.checkForInput(mousePos):
                    settings()
                if quit_button.checkForInput(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  

def settings():
    while True: 
        #AHHHHHH
        mousePos = pygame.mouse.get_pos()

        #trying to get an image to appear behind the buttons
        #screen.blit(myimage, (1458, 118))

        vol_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 118),
                                 text_input="Volume", font=buttonfont, base_color=white, hovering_color=white)
        music_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 178),
                                 text_input="Music", font=buttonfont, base_color=white, hovering_color=white)
        exit_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 238),
                                 text_input="Close Menu", font=buttonfont, base_color=white, hovering_color=white)
        
        for button in [vol_button, music_button, exit_button]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if vol_button.checkForInput(mousePos):
                    volume = 0
                if music_button.checkForInput(mousePos):
                    music = 0
                if exit_button.checkForInput(mousePos):
                    return

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
                                text_input="Back", font=buttonfont, base_color=black, hovering_color=red)
        
        snow_power = Button(transform.scale(pygame.image.load("Resources/Sprites/snow.PNG").convert_alpha(),(72,72)), pos=(100, 600), 
                                text_input=None, font=buttonfont, base_color=black, hovering_color=red)
        double_power = Button(transform.scale(pygame.image.load("Resources/Sprites/double.PNG").convert_alpha(),(72,72)), pos=(150, 600), 
                                text_input=None, font=buttonfont, base_color=black, hovering_color=red)
        placeholder_power = Button(None, pos=(250, 600), 
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
                             text_input="Main Menu", font=buttonfont, base_color=black, hovering_color=red)
        skip_tutorial_button = Button(None, pos=(100, 650), 
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
        gameStarted = False
        gameCompleted = False

        menu_button = Button(None, pos=(1000, 650), 
                             text_input="Main Menu", font=buttonfont, base_color=black, hovering_color=red)
        shop_button = Button(None, pos=(400, 650), 
                             text_input="Shop", font=buttonfont, base_color=black, hovering_color=red)
        start_button = Button(None, pos=(400, 450), 
                             text_input="Start", font=buttonfont, base_color=black, hovering_color=red)
        next_round_button = Button(None, pos=(700, 650), 
                             text_input="Next Round", font=buttonfont, base_color=black, hovering_color=red)
        settings_button = Button(transform.scale(pygame.image.load("Resources/Sprites/gear.PNG").convert_alpha(),(50,50)), pos=(1458, 118),
                                 text_input="", font=buttonfont, base_color=white, hovering_color=white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

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
                        aliveodds = 10
                        absentodds = 3
                        rabbitodds = 10
                        if moles[i].status == 'absent':
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                moles[i].status = 'alive'
                                r = random.randint(0,rabbitodds)
                                if r == 1:
                                    moles[i].image = rabbitalive
                                    moles[i].status = 'rabbitalive'
                                elif r%2 == 0:
                                    moles[i].image = molealive_s
                                else: moles[i].image = molealive_b
                        # if alive, randomly make it absent
                        elif moles[i].status == 'alive':
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i].status = 'absent'
                                moles[i].image = moleabsent
                        elif moles[i].status == 'dead':
                            moles[i].status = 'absent'
                            moles[i].image = moleabsent

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(mousePos):
                    main_menu()
                if next_round_button.checkForInput(mousePos):
                    play()
                if shop_button.checkForInput(mousePos):
                    shop()
                if settings_button.checkForInput(mousePos):
                    settings()
                if start_button.checkForInput(mousePos):
                    gameStarted = True
                    secondsRemaining = 120
                    score = 0
                    #pygame.mouse.set_visible(False)
                    #cursor_image = pygame.image.load("hammer.png")
                    #cursor_rect = cursor_image.get_rect()

                if gameStarted:
                    for i in range(9):
                        if mousex >= moles[i].x and mousex <= moles[i].x + 80 and \
                            mousey >= moles[i].y and mousey <= moles[i].y + 62:
                            if moles[i].status == 'alive':
                                moles[i].image = moledead
                                moles[i].status = 'dead'
                                #hitsound.play()
                                score += 2
                            elif moles[i].status == 'rabbitalive':
                                moles[i].image = rabbitdead
                                moles[i].status = 'dead'
                                #hitsound.play()
                            else:
                                #buzzer.play()
                                score -= 1
            
            #This has to be here, not sure why, but now it doesnt "glitch"
            screen.fill(black)
            # loads in image and scales it to screen size
            BG = transform.scale(pygame.image.load("Resources/Backgrounds/BG_Play.PNG").convert(),GAME_SIZE)
            # blits the image to the center of the surface "screen"
            screen.blit(BG, BG.get_rect(center = screen.get_rect().center))

            allmoles.draw(screen)

            if gameStarted:
                #cursor_rect.center = pygame.mouse.get_pos()
                #screen.blit(cursor_image, cursor_rect)

                for button in [menu_button, settings_button]:
                    button.changeColor(mousePos)
                    button.update(screen)

                minutes = str(secondsRemaining // 60)
                seconds = str(secondsRemaining % 60)
                if len(minutes) < 2:
                    minutes = "0" + minutes
                if len(seconds) < 2:
                    seconds = "0" + seconds
                    
                timerText = buttonfont.render(minutes + ":" + seconds, True, black, pink)
                timerRect = timerText.get_rect()
                timerRect.center = (150, 600)
                pygame.draw.rect(screen, pink, timerRect)
                screen.blit(timerText, timerRect)
            
                jar = update_jar(score)
                screen.blit(jar, (1350, 740))

                if secondsRemaining < 0:
                    gameStarted = False
                    for i in range(9):
                        moles[i].image = moleabsent
                        moles[i].status = 'absent'
                    gameCompleted = True
                    gameover.play()
                    pygame.mouse.set_cursor(pygame.cursors.Cursor())

            else: 
                pygame.mouse.set_visible(True)

                for button in [menu_button, shop_button, start_button, next_round_button, settings_button]:
                    button.changeColor(mousePos)
                    button.update(screen)

                if gameCompleted:
                    print("the game finished")



        pygame.display.update()

intro_sequence()
# maybe have it play a 7 sec empty audio then restart the previosuly playing aufio that way
# it doesnt overlap music sewuence and sfx
main_menu()