import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

#do another run test with this https://youtu.be/MYaxPa_eZS0?si=iAa8y9Hih0RU0NVn
#for main game, randomly generated map
#for ongoing scrolling background:https://youtu.be/ARt6DLP38-Y?si=RMz8_aSWx42RIo89

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sheet_image = pygame.image.load('long_sheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list = []
animation_steps = [6, 4, 10, 5 ,11, 6]
action = 1
last_update = pygame.time.get_ticks()
animation_cooldown = 70
frame = 0
step_counter = 0 

for animation in animation_steps:
    temp_img_list = []
    for x in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 50, 42, 2, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)


run = True
while run:
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    mouse_presses = pygame.mouse.get_pressed()


    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= (animation_steps[action]):
                frame = 0

    x = 0

    if keys [pygame.K_d]:
        action -= 1
        screen.blit(animation_list[0][frame],(x, 20))
        x += 0.2
    elif mouse_presses[0]:
        action += 3
        screen.blit(animation_list[4][frame],(x, 20))
    elif keys [pygame.K_SPACE]:
        action += 1
        screen.blit(animation_list[2][frame],(x, 20))
        x += 0.1
        y = 20
        y +=0.1
    elif keys [pygame.K_LSHIFT]:
        action += 2
        screen.blit(animation_list[3][frame],(x, 20))
        x += 0.2
 
    else:
        screen.blit(animation_list[1][frame],(x, 20))

    





    pygame.display.update()


pygame.quit()
