import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

r_run_sheet_image = pygame.image.load('Run.png').convert_alpha()
r_run_sheet = spritesheet.SpriteSheet(r_run_sheet_image)

l_run_sheet_image = pygame.image.load('Run_flip2.png').convert_alpha()
l_run_sheet = spritesheet.SpriteSheet(l_run_sheet_image)

idle_sprite_r = pygame.image.load('idleimage.png').convert_alpha()
idle_sprite_r = pygame.transform.scale(idle_sprite_r,(100,100))

idle_sprite_l = pygame.image.load('idleimage_flipped.png').convert_alpha()
idle_sprite_l = pygame.transform.scale(idle_sprite_l,(100,100))

BG = (50, 50, 50)
BLACK = (0, 0, 0)

#create animation list

animation_list_r = []
animation_list_l = []
animation_steps = 16
last_update = pygame.time.get_ticks()
animation_cooldown = 20
frame = 0


for x in range(animation_steps):
    animation_list_r.append(r_run_sheet.get_image(x, 100, 100, 1, BLACK))

for x in range(animation_steps):
    animation_list_l.append(l_run_sheet.get_image(x, 100, 100, 1, BLACK))

run = True
while run:

    #update background
    screen.fill(BG)

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= animation_steps:
            frame = 0
    

    keys = pygame.key.get_pressed()


    if keys [pygame.K_RIGHT]:
        screen.blit(animation_list_r[frame],(x, 0))
        x += 0.5

    elif keys [pygame.K_LEFT]:
        screen.blit(animation_list_l[frame],(x, 0))
        x -= 0.5

    else:
        screen.blit(idle_sprite_r, (x,0))

        
    if x > 1000:
        x=0
    if x < 0:
        x = 1000
 
    pygame.display.update()


pygame.quit()
