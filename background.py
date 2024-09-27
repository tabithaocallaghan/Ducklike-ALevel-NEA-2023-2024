import pygame
import os.path
import random
from random import randint
import spritesheet
from pygame import mixer

pygame.init()
mixer.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 360

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("parallax")

#define game variables
scroll = 0

ground_image = pygame.image.load("ground1.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height= ground_image.get_height()

#the animation 
##r_run_sheet_image = pygame.image.load('run.png').convert_alpha()
##r_run_sheet = spritesheet.SpriteSheet(r_run_sheet_image)
##idle_image = pygame.image.load('idlenew.png').convert_alpha()
##idle_sheet = spritesheet.SpriteSheet(idle_image)

BLACK = (0,0,0)
animation_list_run = []
animation_list_idle = []
animation_steps_run = 4
animation_steps_idle = 6
last_update = pygame.time.get_ticks()
animation_cooldown= 100
frame = 0

##for i in range(animation_steps_run):
##    animation_list_run.append(r_run_sheet.get_image(i, 50, 37, 2, BLACK))
##for i in range (animation_steps_idle):
##    animation_list_idle.append(idle_sheet.get_image(i, 50, 37, 2, BLACK))

#back to background
bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f'NightForest/Layers/{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(200):
        speed = 1 
        for i in bg_images:
            screen.blit(i,((x * bg_width) - scroll * speed,0))
            speed += 0.2


def draw_ground():
    for x in range (2000):
        screen.blit(ground_image, ((x *ground_width) - scroll * 2.2, SCREEN_HEIGHT - ground_height))



#gameloop
run = True
while run:
    clock.tick(FPS)

    #draw world
    draw_bg()
    draw_ground()

    #create animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= animation_steps_run or frame >= animation_steps_idle:
                frame = 0
    x = 0
    #get keypressed
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and scroll > 0:
        scroll -= 3
    if key[pygame.K_d] and scroll < 3000:
        scroll += 3
        #screen.blit(animation_list_run[frame],(x,225))
        #x += 0.3
    
        #screen.blit(animation_list_idle[frame],(x,220))


    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()




pygame.quit()
