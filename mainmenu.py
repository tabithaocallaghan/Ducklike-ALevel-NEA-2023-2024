import pygame
import button
import os
from pygame import mixer

#another day.. up at the quack of dawn...seeking justice...and bread.

pygame.init()
mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#likely change the screen size, based on backgrounds
#current size is simply a placeholder for inputing all features

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

#game variables
game_paused = False
menu_state = "main"

bg = pygame.image.load("menu_img.png")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

ducklike = pygame.image.load("menu buttons/ducklike.png").convert_alpha()
play_img = pygame.image.load("menu buttons/play.png").convert_alpha()
options_img = pygame.image.load("menu buttons/options.png").convert_alpha()
credits_img = pygame.image.load("menu buttons/credits.png").convert_alpha()
quit_img = pygame.image.load("menu buttons/quit.png").convert_alpha()
keybinds_img = pygame.image.load("menu buttons/keybinds.png").convert_alpha()
audio_img = pygame.image.load("menu buttons/audio.png").convert_alpha()
back_img = pygame.image.load("menu buttons/back.png").convert_alpha()

music_img = pygame.image.load("menu buttons/music.png").convert_alpha()
music_img = pygame.transform.scale(music_img,(360,81))

less_img = pygame.image.load("menu buttons/less.png").convert_alpha()
more_img = pygame.image.load("menu buttons/more.png").convert_alpha()
dashes_img = pygame.image.load("menu buttons/dashes.png").convert_alpha()
dashes_img = pygame.transform.scale(dashes_img,(360,54))

idle_img = pygame.image.load("idle.jpeg").convert_alpha()
idle_img = pygame.transform.scale(idle_img, (205, 193))


#CREDITS
#GAME DESIGN AND PROGRAMMING ..... TABITHA O'CALLAGHAN
#CHARACTER SPRITES BASE AND ENEMY SLIME..... [ITCH.IO USER]
#OTHER MOB SPRITES ..... [ITCH.IO USER]
#MAIN LEVEL BACKGROUND ..... [ITCH.IO USER]
#MUSIC ..... [LIST SOURCES]


MENU_MOUSE_POS = pygame.mouse.get_pos()

play_button = button.Button(10, 200, play_img)
options_button = button.Button(10, 300, options_img)
credits_button = button.Button(10, 400, credits_img)
quit_button = button.Button(10, 500, quit_img)

keybinds_button = button.Button(100, 200, keybinds_img)
audio_button = button.Button(100, 300, audio_img)
back_button = button.Button(100, 400, back_img)

less_button = button.Button(150, 200, less_img)
more_button = button.Button(300, 200, more_img)

x = 0.7
mixer.music.load('sample.wav')
#mixer.music.play()
click = pygame.mixer.Sound('clicksound.wav')

run= True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg, (0,0))


    if game_paused == False:
        #check menu state
        if menu_state == "main":
            pygame.display.set_caption("Main Menu")
            screen.blit(ducklike, (0,20))
            #draw buttons
            if play_button.draw(screen):
                pygame.mixer.Sound.play(click)
                os.system("ducklike.py")
            if options_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "options"
            if credits_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "credits"
            if quit_button.draw(screen):
                pygame.mixer.Sound.play(click)
                run = False
        if menu_state == "options":
            pygame.display.set_caption("Options")
            if audio_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "audio"
            if keybinds_button.draw(screen):
                pygame.mixer.Sound.play(click)
                pass
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "main"
        if menu_state == "audio":
            pygame.display.set_caption("Audio")
            screen.blit(music_img, (100, 200))
            screen.blit(dashes_img, (200, 200))
            if less_button.draw(screen):
                pygame.mixer.Sound.play(click)
                x -= 0.1
                mixer.music.set_volume(x)
                print(x)
            if more_button.draw(screen):
                pygame.mixer.Sound.play(click)
                x += 0.1
                mixer.music.set_volume(x)
                print(x)
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "options"
        if menu_state == "credits":
            pygame.display.set_caption("Credits")
            screen.blit(idle_img, (100, 200))
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "main"
                   
      
    pygame.display.update()


pygame.quit()
