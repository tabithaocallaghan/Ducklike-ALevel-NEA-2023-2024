import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

r_run_sheet_image = pygame.image.load('newrun.png').convert_alpha()
r_run_sheet = spritesheet.SpriteSheet(r_run_sheet_image)

idle_image = pygame.image.load('idlenew.png').convert_alpha()
idle_sheet = spritesheet.SpriteSheet(idle_image)

attack_image = pygame.image.load('attacking.png').convert_alpha()
attack_sheet = spritesheet.SpriteSheet(attack_image)

jump_image = pygame.image.load('jumpingnew.png').convert_alpha()
jump_sheet = spritesheet.SpriteSheet(jump_image)

slide_image = pygame.image.load('sliding.png').convert_alpha()
slide_sheet = spritesheet.SpriteSheet(slide_image)

defeat_image = pygame.image.load('defeat.png').convert_alpha()
defeat_sheet = spritesheet.SpriteSheet(defeat_image)
defeat_final = pygame.image.load('defeatfinal.png').convert_alpha()
#defeat_final = pygame.transform.scale(defeat_final(50,37))

mark_image = pygame.image.load('markidle.png').convert_alpha()
mark_sheet = spritesheet.SpriteSheet(mark_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list_r = []
animation_list_idle = []
animation_list_atk = []
animation_list_jump = []
animation_list_slide = []
animation_list_defeat = []
animation_list_mark = []


animation_steps = [4, 6, 10, 5, 11, 6, 4] 
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0

action = 0

if action == 0:
    for a in range(animation_steps[0]):
        animation_list_idle.append(idle_sheet.get_image(a, 50, 37, 2, BLACK))
elif action == 1:
    for x in range(animation_steps[1]):
        animation_list_r.append(r_run_sheet.get_image(x, 50, 37, 2, BLACK))
elif action ==  2:
    for x in range(animation_steps[2]):
        animation_list_jump.append(jump_sheet.get_image(x, 50, 37, 2, BLACK))
elif action == 3:
    for x in range(animation_steps[3]):
        animation_list_slide.append(slide_sheet.get_image(x, 50, 37, 2, BLACK))
elif action == 4:
    for x in range(animation_steps[4]):
        animation_list_atk.append(attack_sheet.get_image(x, 50, 37, 2, BLACK))
elif action == 5:
    for x in range(animation_steps[5]):
        animation_list_atk.append(death_sheet.get_image(x, 50, 37, 2, BLACK))

for x in range(animation_steps[6]):
    animation_list_mark.append(mark_sheet.get_image(x, 50, 37, 2, BLACK))
    
    

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
            if frame >= (animation_steps[action]):
                frame = 0

    screen.blit(animation_list_mark[frame], (250,250))

    keys = pygame.key.get_pressed()
    mouse_presses = pygame.mouse.get_pressed()


    y =20
    x =0
    
    if keys [pygame.K_d]:
        for a in range(animation_steps[1]):
            animation_list_r.append(r_run_sheet.get_image(a, 50, 37, 2, BLACK))
        screen.blit(animation_list_r[frame],(x, y))
        x =+ 2
    elif mouse_presses[0]:
        for a in range(animation_steps[4]):
            animation_list_atk.append(attack_sheet.get_image(a, 50, 37, 2, BLACK))
        screen.blit(animation_list_atk[frame],(x,20))
    elif keys [pygame.K_SPACE]:
        for a in range(animation_steps[2]):
            animation_list_jump.append(jump_sheet.get_image(a, 50, 37, 2, BLACK))
        screen.blit(animation_list_jump[frame],(x , 20))
        x += 0.1
        y = 20
        y +=0.1
    elif keys [pygame.K_LSHIFT]:
        for a in range(animation_steps[3]):
            animation_list_slide.append(slide_sheet.get_image(a, 50, 37, 2, BLACK))
        screen.blit(animation_list_slide[frame],(x, 20))
        x += 0.2
    elif keys [pygame.K_e]:
        for a in range(animation_steps[5]):
            animation_list_defeat.append(defeat_sheet.get_image(a, 50, 37, 2, BLACK))
        screen.blit(animation_list_defeat[frame], (x, 20))
        x = 0
    else:
        action = 0
        screen.blit(animation_list_idle[frame], (x, y))

    

    

        
    if x > 500:
        x=0
    if x < 0:
        x = 500
 
    pygame.display.update()


pygame.quit()

