import pygame
import os
from pygame import mixer
import random
import csv
import button

pygame.init()
mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ducklike')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 400
scroll = 0
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 12
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 0
start_game = False
start_intro = False
menu_state = "main"
level_complete = False
convo = False
##
talkedto = False
tutorial = False
boss_beaten = False
main_complete = False
tutorial_complete = False

##dialouge variables
notyet = False
diag_1 = False
diag_2 = False
diag_3 = False
diag_4 = False
diag_5 = False
diag_6 = False
milesdiag_1 = False
milesdiag_2 = False
notyet_sound = False
diag1_sound = False
diag2_sound = False
diag3_sound = False
diag4_sound = False
diag5_sound = False
diag6_sound = False
miles1_sound = False
miles2_sound = False
noexit = False
tut_tile = False
miles_endsound = False

#define player action variables
moving_left = False
moving_right = False
sliding_left = False
sliding_right = False
attacking = False
close = False
taking_damage = False

#define colours
BG = (50, 50, 50)
BLACK = (0,0,0)
RED = (220, 76, 76)
GREEN = (118, 148, 126)
WHITE = (255, 255, 255)
NEWBG = (205, 206, 205)

#define fonts
font = pygame.font.SysFont('static/Oswald-Bold.ttf', 26)
###load images for main menu
bg = pygame.image.load("menu_img.png")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
ducklike = pygame.image.load("menu buttons/ducklike.png").convert_alpha()
##creating button imgs
play_img = pygame.image.load("menu buttons/play.png").convert_alpha()
tutorial_img = pygame.image.load("menu buttons/tutorial.png").convert_alpha()
credits_img = pygame.image.load("menu buttons/credits.png").convert_alpha()
quit_img = pygame.image.load("menu buttons/quit.png").convert_alpha()
back_img = pygame.image.load("menu buttons/back.png").convert_alpha()
restart_img = pygame.image.load("menu buttons/restart.png").convert_alpha()
return_img = pygame.image.load("menu buttons/return to menu.png").convert_alpha()
##loading in sound
click  = pygame.mixer.Sound('music/clicksound.wav')
##tiles for in game info
tut_tileimg = pygame.image.load("icons/tut_tile.png").convert_alpha()
noexitimg = pygame.image.load("icons/noexit.png").convert_alpha()
##miles image for ending
end_art = pygame.image.load("dialouge/miles_end.png").convert_alpha()
##music
pygame.mixer.music.load('music/menu_track.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
##text images
youdied_img = pygame.image.load("text/you died.png").convert_alpha()


##convo dialouge texts - mark
diag_1img = pygame.image.load("dialouge/textboxes/diag1_mark.png").convert_alpha()
diag_1_fx = pygame.mixer.Sound('dialouge/audio/diag_1_mark.wav')
diag_2img = pygame.image.load("dialouge/textboxes/diag2_mark.png").convert_alpha()
diag_2_fx = pygame.mixer.Sound('dialouge/audio/diag_2_mark.wav')
diag_3img = pygame.image.load("dialouge/textboxes/sigh_text.png").convert_alpha()
diag_3_fx = pygame.mixer.Sound('dialouge/audio/sigh.wav')
diag_4img = pygame.image.load("dialouge/textboxes/diag3_mark.png").convert_alpha()
diag_4_fx = pygame.mixer.Sound('dialouge/audio/diag_3_mark.wav')
diag_5img = pygame.image.load("dialouge/textboxes/go_text.png").convert_alpha()
diag_5_fx = pygame.mixer.Sound('dialouge/audio/diag_4_mark.wav')
diag_6img = pygame.image.load("dialouge/textboxes/diag4_mark.png").convert_alpha()
diag_6_fx = pygame.mixer.Sound('dialouge/audio/diag_5_mark.wav')
##convo dialouge - miles
milesdiag_1img = pygame.image.load("dialouge/textboxes/miles_diag.png").convert_alpha()
milesdiag_2img = pygame.image.load("dialouge/textboxes/miles_diag2.png").convert_alpha()
milesdiag_1fx = pygame.mixer.Sound('dialouge/audio/diag_1_miles.wav')
milesdiag_2fx = pygame.mixer.Sound('dialouge/audio/diag_2_miles.wav')

miles_endimg = pygame.image.load("dialouge/textboxes/miles_endbox.png").convert_alpha()
miles_endfx =  pygame.mixer.Sound('dialouge/audio/miles_endaud.wav')
##not yet - mark
notyetimg = pygame.image.load("dialouge/textboxes/notyet_text.png").convert_alpha()
notyet_fx = pygame.mixer.Sound('dialouge/audio/notyet.wav')

##movement
jump_sound = pygame.mixer.Sound('music/jump.wav')
hit_sound = pygame.mixer.Sound('music/hit.wav')

arc = pygame.image.load("Arc.png").convert_alpha()


#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'tilesets/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    
#health    
slice_img = pygame.image.load('icons/Slice.png').convert_alpha()
#slice of life
loaf_img = pygame.image.load('icons/Loaf.png').convert_alpha()
#loaf of vitality
itemdic = {
    'Slice' : slice_img,
    'Loaf'  : loaf_img
    }
#sword
sword_img = pygame.image.load('icons/sword.png').convert_alpha()
#enemy sword
enemy_damage_img = pygame.image.load('icons/testingsword.png').convert_alpha()

#background images
if level == 2:
    bg_images = []
    for i in range(1,7):
        bg_image = pygame.image.load(f'NightForest/NewLayers/{i}.png').convert_alpha()
        bg_image= pygame.transform.scale(bg_image,(int(bg_image.get_width() *1.5), int(bg_image.get_height() *1.5)))
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()
else:
    bg_images = []
    for i in range(1,6):
        bg_image = pygame.image.load(f'NightForest/Layers/{i}.png').convert_alpha()
        bg_image= pygame.transform.scale(bg_image,(int(bg_image.get_width() *1.5), int(bg_image.get_height() *1.5)))
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()


    


#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
##    screen.fill(BG)
##    width = 620
##    for x in range(5):
##        screen.blit(img_1,((x * width) - bg_scroll * 0.5, 0))
##        screen.blit(img_2,((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - img_2.get_height() - 300))
##        screen.blit(img3, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - img_3.get_height() - 150))
##        screen.blit(img_4, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - img_4.get_height()))
        
    for x in range(world.level_length):
        speedbg = 0.3
        for i in bg_images:
            screen.blit(i,((x * bg_width) - bg_scroll * speedbg,0))
            speedbg += 0.2
        
#reset level
def reset_level():
    enemy_group.empty()
    item_group.empty()
    npc_group.empty()
    sword_group.empty()
    enemy_damage_group.empty()
    exit_group.empty()

    #create empty tile list

    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data
    
    
   
####class for player##################################################################################    
class Miles(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.atk_cooldown = 0
        self.slide_cooldown = 0
        self.hp = 150
        self.max_hp = self.hp
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.atk = False
        self.animation_list= []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all images for the players
        animation_types = ['new idle', 'new move', 'new jump', 'newer sliding', 'new atk', 'death', 'hurt']
        #animation_types = ['newer sliding', 'new move', 'new jump', 'new idle', 'new atk', 'death', 'hurt']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f'sprites/miles/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/miles/{animation}/{i}.png').convert_alpha()
                img= pygame.transform.scale(img, (int(img.get_width() *scale), int(img.get_height() *scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
##        self.width = self.image.get_width()
##        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1
        #if self.slide_cooldown
        self.check_alive()

    def move(self, moving_left, moving_right, sliding_left, sliding_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0
        #assign movement variables if moving left or right
        if moving_left:
            dx =- self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx =+ self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        #sliding
        if sliding_left and self.flip:
            dx =- self.speed
            self.flip = True
            self.direction = -1
            self.sliding = False
        elif sliding_right:
            dx =+ self.speed
            self.flip = False
            self.direction = 1
            self.sliding = False


        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.w, self.rect.h):
                dx = 0
                #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.w, self.rect.h):
                #check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    
        #checking if walking off screen?
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            dx = 0  

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

##        if self.action == 3:
##            self.rect.y = 40
            
        #check if off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.hp = 0
            
        #update scroll based on player position
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx

        return screen_scroll

    def attack(self):
        if self.atk_cooldown == 0:
            self.atk_cooldown = 50
            sword = PlayerSword(self.rect.centerx + (0.5*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            sword_group.add(sword)
          
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        bottom = self.rect.bottom
        if self.action == 3: #test if sliding
            self.rect.size = self.animation_list[3][0].get_size()
        else:
            self.rect.size = self.animation_list[0][0].get_size()
        self.rect.bottom = bottom
        
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation has run, reset to start
        if self.frame_index >=len(self.animation_list[self.action]):
            if self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is diff to previous
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.update_action(5)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)


##items########################################
class Item(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = itemdic[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #check if player has picked up the item
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Slice':
                player.hp += 15
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            elif self.item_type == 'Loaf':
                player.hp += 25
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
            self.kill()
            
        self.rect.x += screen_scroll



##health bar###################################
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y= y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calc hp ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, BLACK,(self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED,(self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN,(self.x, self.y, 150 * ratio, 20))
        
##sword class#####################################
class PlayerSword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 15
        self.image = sword_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #move dot
        self.rect.x += (self.direction * self.speed) + screen_scroll
        self.rect.x += screen_scroll
        #check if off screen
        if self.rect.right < (player.rect.left - 30) or self.rect.left > (player.rect.right + 30):
            self.kill()
        #check for collision in level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check collisions with characters
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, sword_group, False):
                if enemy.alive:
                    enemy.hp -= 35
                    print(enemy.hp)
                    self.kill()

class TamikoSword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 50
        self.image = sword_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #move dot
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if off screen
##        if self.rect.right < (enemy.rect.left - 50) or self.rect.left > (enemy.rect.right + 50):
##            self.kill()
        #check for collision in level
##        for tile in world.obstacle_list:
##            if tile[1].colliderect(self.rect):
##                self.kill()
        #check collisions with characters
        if pygame.sprite.spritecollide(player, enemy_damage_group, False):
            if player.alive and sliding_left and sliding_right:
                self.kill()
            elif player.alive:
                player.hp -= 20
                taking_damage = True
                self.kill()

class EnemyDamage(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = enemy_damage_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #move dot
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check collisions with characters
        if pygame.sprite.spritecollide(player, enemy_damage_group, False):
            if player.alive and sliding_left and sliding_right:
                self.kill()
            elif player.alive:
                player.hp -= 15
                player.action = 6
                print(player.action)
                print(player.hp)
                self.kill()
                

###giving the enemies health bars####
class EnemyHealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y= y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calc hp ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, BLACK,(self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED,(self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN,(self.x, self.y, 150 * ratio, 20))

                
#####making a class for mark (npc)#######################################################################
class Mark(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.vel_y = 0
        self.animation_list= []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        num_of_frames = len(os.listdir(f'sprites/mark/new idle'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'sprites/mark/new idle/{i}.png').convert_alpha()
            img= pygame.transform.scale(img, (int(img.get_width() *scale), int(img.get_height() *scale)))
            self.animation_list.append(img)
        
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def move(self):
        #reset movement variables
        dx = 0
        dy = 0

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
  
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x += screen_scroll

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation has run, reset to start
        if self.frame_index >=len(self.animation_list):
            self.frame_index = 0
            
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)




####class for boss############################################################
class Tamiko(pygame.sprite.Sprite):
    def __init__(self,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.cooldown = 0
        self.hp = 500
        self.max_hp = self.hp
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list= []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 100, 20)
        self.close = pygame.Rect(0, 0 , 50, 20)
        self.idling = 0
        self.idling_counter = 0
        

        #load all images for the players
        animation_types = ['idle', 'move', 'new atk','death']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f'sprites/tamiko/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/tamiko/{animation}/{i}.png')
                img= pygame.transform.scale(img, (int(img.get_width() *scale), int(img.get_height() *scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0
        
        if moving_left:
            dx =- self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx =+ self.speed
            self.flip = False
            self.direction = 1

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

    
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self):
        if self.cooldown == 0:
            self.cooldown = 50
            sword = TamikoSword(self.rect.centerx + (0.5*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            enemy_damage_group.add(sword)

    def chase(self,moving_left,moving_right):
        if player.rect.x > self.rect.x:
            if close == False:
                moving_right = True
        if player.rect.x < self.rect.x:
            if close == False:
                moving_left = False

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,500) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            #check if the ai is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                #get close to the player
##                self.chase(moving_left, moving_right)
##                if self.close.colliderect(player.rect):
##                    close = True
                #atk animation
                self.update_action(2)
                #shoot
                self.attack()
##            elif self.hp < self.max_hp:
##                self.direction = player.direction
##                self.update_action(2)
##                self.attack()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    

                    if self.move_counter > 50:
                        self.direction = self.direction * -1
                        self.move_counter = self.move_counter * -1

                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        elif player.alive == False:
            self.update_action(0)

        #scroll
        self.rect.x += screen_scroll
        self.vision.x += screen_scroll
                

    def update(self):
        self.update_animation()
        if self.cooldown > 0:
            self.cooldown -= 1
        self.check_alive()
        
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 150 ## she's calmer therefore she's moving much more slowly. 
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if imation has run, reset to start
        if self.frame_index >=len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is diff to previous
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            boss_beaten = True
            
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)
        #pygame.draw.rect(screen, RED, self.vision, 1)

##class for enemies###############################################
class Enemy(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.cooldown = 0
        self.hp = 50
        self.max_hp = self.hp
        self.char_type = char_type
        self.direction = 1
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.animation_list= []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 80, 10)
        self.idling = 0
        self.idling_counter = 0

        animation_types = ['idle', 'move', 'atk', 'hurt','death']
        for animation in animation_types:
            #reset temp list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f'sprites/{char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'sprites/{char_type}/{animation}/{i}.png').convert_alpha()
                img= pygame.transform.scale(img, (int(img.get_width() *scale), int(img.get_height() *scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0

        if moving_left:
            dx =- self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx =+ self.speed
            self.flip = False
            self.direction = 1

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
    
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

##        self.vision.x += dx
##        self.vision.y += dy

    def attack(self):
        if self.cooldown == 0:
            self.cooldown = 50
            enemy_damage = EnemyDamage(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            enemy_damage_group.add(enemy_damage)


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            #check if the ai is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(2)
                #shoot
                self.attack()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    

                    if self.move_counter > TILE_SIZE:
                        self.direction = self.direction * -1
                        self.move_counter = self.move_counter * -1

                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
        elif player.alive == False:
            self.update_action(0)

        #scroll
        self.rect.x += screen_scroll

        self.vision.x += screen_scroll
       
    def update(self):
        self.update_animation()
        if self.cooldown > 0:
            self.cooldown -= 1
        self.check_alive()

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation has run, reset to start
        if self.frame_index >=len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0
                
    def update_action(self, new_action):
        #check if new action is diff to previous
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)
            if self.frame_index == len(self.animation_list[self.action]) -1:
                self.kill()
            
            
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)
        #pygame.draw.rect(screen, RED, self.vision, 1)
        

####world######################################
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        player = ""
        health_bar = ""
        enemy_bar = ""
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 0: #create exit
                        escape = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(escape)
                        self.obstacle_list.append(tile_data)
                    elif tile >= 1 and tile <=5: 
                        self.obstacle_list.append(tile_data)
                    elif tile == 6:#create slimes
                        slime = Enemy('slime', x * TILE_SIZE, y * TILE_SIZE, 1.5, 1)
                        enemy_group.add(slime)
                    elif tile == 7:#create loaf
                        item = Item('Loaf', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(item)
                    elif tile == 8:#create slice
                        item = Item('Slice', x * TILE_SIZE , y * TILE_SIZE)
                        item_group.add(item)
                    elif tile == 11: #creating tamiko(boss)
                        boss = Tamiko(x * TILE_SIZE, y * TILE_SIZE, 1.5, 1)
                        enemy_bar = EnemyHealthBar(640, 10, boss.max_hp, boss.max_hp)
                        enemy_group.add(boss)
                    elif tile == 9:#create mark(npc)
                        npc = Mark(x * TILE_SIZE, y * TILE_SIZE, 1.75, 3)
                        npc_group.add(npc)
                    elif tile == 10: #creating miles(player)
                        player = Miles(x * TILE_SIZE, y * TILE_SIZE, 1.5, 7)
                        health_bar = HealthBar(10, 10, player.max_hp, player.max_hp)
                    elif tile == 12:#creating arch
                        decoration = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(decoration)
                        

                        
        return player, health_bar, enemy_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

###making the exit###
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


####transitions##
class ScreenFade():
    def __init__(self,direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#whole screen
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.direction == 2:#vertial down
            pygame.draw.rect(screen, self.colour, (0,0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
            
        return fade_complete
    
###cutscene
def CutScene(scene):
    num = len(os.listdir(f'cutscenes/{scene}'))
    for i in range(num):
        img = pygame.image.load(f'cutscenes/{scene}/{i}.png').convert_alpha()
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(img, (0,0))
        pygame.time.wait(510)


#create screen fades
intro_fade = ScreenFade(1, BLACK, 20)
        
########################################
##create buttons
play_button = button.Button(350, 175, play_img)
tutorial_button = button.Button(325, 225, tutorial_img)
credits_button = button.Button(330, 275, credits_img)
quit_button = button.Button(350, 400, quit_img)
back_button = button.Button(350, 350, back_img)
restart_button = button.Button(150, 175, restart_img)
return_button = button.Button(325, 175, return_img)

##create buttons for each dialouge box
notyet_button = button.Button(200, 10, notyetimg)
diag_1_button = button.Button(200, 10, diag_1img)
diag_2_button = button.Button(200, 10, diag_2img)
diag_3_button = button.Button(200, 10, diag_3img)
diag_4_button = button.Button(200, 10, diag_4img)
diag_5_button = button.Button(200, 10, diag_5img)
diag_6_button = button.Button(200, 10, diag_6img)

miles_1_button = button.Button(200, 10, milesdiag_1img)
miles_2_button = button.Button(200, 10, milesdiag_2img)

miles_end_button = button.Button(200, 300, miles_endimg)

##buttons for in game info
tut_tile_button = button.Button(200, 10, tut_tileimg)
noexit_button = button.Button(200, 10, noexitimg)

#groups
enemy_group = pygame.sprite.Group()
enemy_health_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
sword_group = pygame.sprite.Group()
enemy_damage_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


#create empty tles list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline= '') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] =  int(tile)



    
world = World()
player, health_bar, enemy_bar = world.process_data(world_data)



run = True
while run:
    clock.tick(FPS)
    if start_game == False:
        #draw menu
        screen.blit(bg, (0,0))
        screen.blit(ducklike, (175, 10))
        if menu_state == "main":                       
            pygame.display.set_caption("Ducklike - Main Menu")
            if play_button.draw(screen):
                click.play()
                start_game = True
                start_intro = True
                pygame.mixer.music.load('music/tutorial_track.wav')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1, 0.0, 5000)
            if tutorial_button.draw(screen):
                click.play()
                menu_state = "tutorial"
            if credits_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "credits"
            if quit_button.draw(screen):
                pygame.mixer.Sound.play(click)
                run = False
        if menu_state == "tutorial":
            pygame.display.set_caption("Ducklike - Tutorial")
            draw_text(f'Use A to move left, D to move right. Use the Left shift to slide which stops damage being taken.', font, WHITE, 10, 175)
            draw_text('Use the Space Bar to Jump. Use the Left click to attack enemies.', font, WHITE, 150, 200)
            draw_text('Use right-click to interact with character or click the exit to move to the next level.', font, WHITE, 75, 225)
            draw_text('Bread regains your health.', font, WHITE, 280, 250)
            draw_text('All enemies must be defeated before a level can be complete.', font, WHITE, 140, 275)
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "main"
        if menu_state == "credits":
            pygame.display.set_caption("Ducklike - Credits")
            draw_text('Art/ Assets', font, WHITE, 240, 100)
            draw_text('Character Sprites - rvros on itch.io', font, WHITE, 200, 120)
            draw_text('Game background - saukgp on itch.io', font, WHITE, 200, 140)
            draw_text('Health items (bread) - Jan Barboza|GGCoffee on itch.io', font, WHITE, 200, 160)
            draw_text('Tilesets - nortexmkd on itch.io', font, WHITE, 200, 180)
            draw_text('Music and Sound',font, WHITE, 240, 200)
            draw_text('Main Menu sfx - Ellr on itch.io', font, WHITE, 200, 220)
            draw_text('Main Menu Music - "Yugen" by Keys of Moon', font, WHITE, 200, 240)
            draw_text('Tutorial Music - "Flowers Bloom" by Glitch', font, WHITE, 200, 260)
            draw_text('Main Game Music - "Asakusa" by Glitch', font, WHITE, 200, 280)
            draw_text('Boss Fight Music - "Shinkansen 2" by Glitch', font, WHITE, 200, 300)
            draw_text('Character Voices - "animalese.js" by Acedio on Github', font, WHITE, 200, 320)
            draw_text('Sound Effects - JDWasabi on itch.io', font, WHITE, 200, 340)
            
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "main"
                
        if menu_state == "done":
            pygame.display.set_caption("Ducklike - End.")
            screen.fill(BLACK)
            screen.blit(end_art,(125,0))
            #pygame.mixer.Sound.play(miles_endfx)
            if miles_end_button.draw(screen):
                menu_state = "thanks"
                miles_endsound = False

        if menu_state == "thanks":
            screen.blit(bg, (0,0))
            screen.blit(ducklike, (175, 10))
            pygame.display.set_caption("Ducklike - Thank you")
            draw_text('You have defeated Tamiko.', font, WHITE, 275, 175)
            draw_text('Thank you for playing Ducklike.', font, WHITE, 260, 200)
            if back_button.draw(screen):
                pygame.mixer.Sound.play(click)
                menu_state = "main"

        if miles_endsound:
            miles_endfx.play(0)
            mile_endsound = False
                
        

    else:
        pygame.display.set_caption("Ducklike")
        #update background
        draw_bg()
        world.draw()
        #show player heatlh
        health_bar.draw(player.hp)
        draw_text(f'{player.hp}', font, WHITE, 170, 13)

        
        if convo == False:
            for npc in npc_group:
                npc.draw(screen)
                npc.update_animation()
                npc.move()
            
            player.update()
            player.draw()

            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            if level == 2:
                for boss in enemy_group:
                    enemy_bar.draw(boss.hp)
                    draw_text(f'{boss.hp}',font, WHITE, 600, 13)
                    if boss.hp == 0:
                        boss_beaten = True
            
            #update and draw groups
            item_group.update()
            sword_group.update()
            enemy_damage_group.update()
            exit_group.update()
            
            item_group.draw(screen)
            sword_group.draw(screen)
            enemy_damage_group.draw(screen)
            exit_group.draw(screen)

    
        else:
            for npc in npc_group:
                npc.draw(screen)
                npc.update_animation()
                npc.move()
            
            player.update()
            player.draw()

            for enemy in enemy_group:
                enemy.update()
                enemy.draw()

            item_group.update()
            sword_group.update()
            enemy_damage_group.update()
            exit_group.update()
            
            item_group.draw(screen)
            sword_group.draw(screen)
            enemy_damage_group.draw(screen)
            exit_group.draw(screen)

            player.speed = 0

            if noexit:
                if noexit_button.draw(screen):
                    convo = False
                    player.speed = 7
                    noexit = False

            if tut_tile:
                if tut_tile_button.draw(screen):
                    convo = False
                    player.speed = 7
                    tut_tile = False

            if notyet:
                if notyet_button.draw(screen):
                    convo = False
                    player.speed = 7
                    notyet = False
                    notyet_sound = False
                    
            if notyet_sound:
                notyet_fx.play()
                notyet_sound = False

            if diag_1:
                if diag_1_button.draw(screen):
                    diag_1 = False
                    diag1_sound = False
                    print("yes")
                    milesdiag_1 = True
                    miles1_sound = True
                    print("done")

            if diag1_sound:
                diag_1_fx.play()
                diag1_sound = False

            if milesdiag_1:
                if miles_1_button.draw(screen):
                    milesdiag_1 = False
                    miles1_sound = False
                    diag_2 = True
                    diag2_sound = True

            if miles1_sound:
                milesdiag_1fx.play()
                miles1_sound = False

            if diag_2:
                if diag_2_button.draw(screen):
                    diag_2 = False
                    diag2_sound = False
                    diag_3 = True
                    diag3_sound = True

            if diag2_sound:
                diag_2_fx.play()
                diag2_sound = False

            if diag_3:
                if diag_3_button.draw(screen):
                    diag_3 = False
                    diag3_sound = False
                    diag_4 = True
                    diag4_sound = True

            if diag3_sound:
                diag_3_fx.play()
                diag3_sound = False

            if diag_4:
                if diag_4_button.draw(screen):
                    diag_4 = False
                    diag4_sound = False
                    diag_5 = True
                    diag5_sound = True

            if diag4_sound:
                diag_4_fx.play()
                diag4_sound = False

            if diag_5:
                if diag_5_button.draw(screen):
                    diag_5 = False
                    diag5_sound = False
                    diag_6 = True
                    diag6_sound = True

            if diag5_sound:
                diag_5_fx.play()
                diag5_sound = False

            if diag_6:
                if diag_6_button.draw(screen):
                    diag_6 = False
                    diag6_sound = False
                    milesdiag_2 = True
                    miles2_sound = True

            if diag6_sound:
                diag_6_fx.play()
                diag6_sound = False

            if milesdiag_2:
                if miles_2_button.draw(screen):
                    milesdiag_2 = False
                    miles2_sound = False
                    convo = False
                    player.speed = 7      

            if miles2_sound:
                milesdiag_2fx.play()
                miles2_sound = False


        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0


        #update player actions
        if player.alive:
            if player.in_air:
                player.update_action(2) # 2 = jump
            elif moving_left or moving_right:
                player.update_action(1) #1 = run
            elif sliding_left or sliding_right:
                player.update_action(3) #3 = slide
            elif attacking:
                player.update_action(4) #4 = atk
                player.attack()
            else:
                player.update_action(0) #0 = idle
                
            screen_scroll = player.move(moving_left, moving_right, sliding_left, sliding_right)
            bg_scroll -= screen_scroll


            if tutorial_complete:
                start_intro = True
                bg_scroll = 0
                pygame.mixer.music.load('music/maingame_track1.wav')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1, 0.0, 5000)
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] =  int(tile)
                                
                    #making changes to the map so that it is randomly generated
                    for i in range(COLS):
                        try: #using try means that it would only run if not errors occur which likely happen
                            x = random.randint(0,12) #creating coords
                            y = random.randint(0,150)
                            if world_data[x][y] == 10: #stops overriding the player spawn point
                                pass
                            elif world_data[x][y] == 0: #stops overriding the exit 
                                pass 
                            else:
                                length = random.randint(2,5) #creates a platform
                                for j in range(length):
                                    if world_data[x][y+j] == 0: #stops overriding the exit
                                        pass
                                    else:
                                        world_data[x][y+j] = 1 #creates a tile

                        #spawns a slime
                                if i % 20 == 0 and y > 3:
                                    world_data[x][y+2] = 6
                        #spawns health items
                                if i % 30 == 0:
                                    world_data[x+1][y+1] = 8
                                    
                                if i % 50 == 0:
                                    world_data[x+1][y+1] = 7
                        except:
                            pass


                    world = World()
                    player, health_bar, enemy_bar = world.process_data(world_data)
                    
                tutorial_complete = False
            if main_complete:
                start_intro = True
                bg_scroll = 0
                pygame.mixer.music.load('music/maingame_track2.wav')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1, 0.0, 5000)
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] =  int(tile)
                    world = World()
                    player, health_bar, enemy_bar = world.process_data(world_data)
                main_complete = False

                
                        
                        
        else:
            screen_scroll = 0
            screen.blit(youdied_img, (250, 50))
            if level == 2:
                if return_button.draw(screen):
                    bg_scroll = 0
                    level = 1
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] =  int(tile)

                    if level == 1:
                        #making changes to the map so that it is randomly generated
                        for i in range(COLS):
                            try: #using try means that it would only run if not errors occur which likely happen
                                x = random.randint(0,12) #creating coords
                                y = random.randint(0,150)
                                if world_data[x][y] == 10: #stops overriding the player spawn point
                                    pass
                                elif world_data[x][y] == 0: #stops overriding the exit 
                                    pass 
                                else:
                                    length = random.randint(2,5) #creates a platform
                                    for j in range(length):
                                        if world_data[x][y+j] == 0: #stops overriding the exit
                                            pass
                                        else:
                                            world_data[x][y+j] = 1 #creates a tile

                            #spawns a slime
                                    if i % 20 == 0 and y > 3:
                                        world_data[x][y+2] = 6
                            #spawns health items
                                    if i % 30 == 0:
                                        world_data[x+1][y+1] = 8
                                        
                                    if i % 50 == 0:
                                        world_data[x+1][y+1] = 7
                            except:
                                pass
                            
                        else:
                            pass
                        
                    world = World()
                    player, health_bar, enemy_bar = world.process_data(world_data)
                    start_game = False
                    menu_state = "main"
                    
            else:
                if restart_button.draw(screen):
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] =  int(tile)

                    if level == 1:
                        #making changes to the map so that it is randomly generated
                        for i in range(COLS):
                            try: #using try means that it would only run if not errors occur which likely happen
                                x = random.randint(0,12) #creating coords
                                y = random.randint(0,150)
                                if world_data[x][y] == 10: #stops overriding the player spawn point
                                    pass
                                elif world_data[x][y] == 0: #stops overriding the exit 
                                    pass 
                                else:
                                    length = random.randint(2,5) #creates a platform
                                    for j in range(length):
                                        if world_data[x][y+j] == 0: #stops overriding the exit
                                            pass
                                        else:
                                            world_data[x][y+j] = 1 #creates a tile

                            #spawns a slime
                                    if i % 20 == 0 and y > 3:
                                        world_data[x][y+2] = 6
                            #spawns health items
                                    if i % 30 == 0:
                                        world_data[x+1][y+1] = 8
                                        
                                    if i % 50 == 0:
                                        world_data[x+1][y+1] = 7
                            except:
                                pass
                        else: pass
                        
                    world = World()
                    player, health_bar, enemy_bar = world.process_data(world_data)
                    
                if return_button.draw(screen):
                    bg_scroll = 0
                    level = 0
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline= '') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] =  int(tile)


                    if level == 1:
                        #making changes to the map so that it is randomly generated
                        for i in range(COLS):
                            try: #using try means that it would only run if not errors occur which likely happen
                                x = random.randint(0,12) #creating coords
                                y = random.randint(0,150)
                                if world_data[x][y] == 10: #stops overriding the player spawn point
                                    pass
                                elif world_data[x][y] == 0: #stops overriding the exit 
                                    pass 
                                else:
                                    length = random.randint(2,5) #creates a platform
                                    for j in range(length):
                                        if world_data[x][y+j] == 0: #stops overriding the exit
                                            pass
                                        else:
                                            world_data[x][y+j] = 1 #creates a tile

                            #spawns a slime
                                    if i % 20 == 0 and y > 3:
                                        world_data[x][y+2] = 6
                            #spawns health items
                                    if i % 30 == 0:
                                        world_data[x+1][y+1] = 8
                                        
                                    if i % 50 == 0:
                                        world_data[x+1][y+1] = 7
                            except:
                                pass
                        else: pass
                        
                    world = World()
                    player, health_bar, enemy_bar = world.process_data(world_data)
                    start_game = False
                    menu_state = "main"


        
    

    handled = False
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
                jump_sound.play()
            if event.key == pygame.K_LSHIFT and player.alive:
                sliding_right = True
            if event.key == pygame.K_LSHIFT and player.alive:
                sliding_left = True
            if event.key == pygame.K_ESCAPE:
                run = False

        pos = pygame.mouse.get_pos()
 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_game:
                    hit_sound.play()
            
                attacking = True
            if event.button == 3:
                for npc in npc_group:
                    if npc.rect.collidepoint(pos)and not handled and len(enemy_group) == 0:
                        convo = True
                        diag_1 = True
                        diag1_sound = True
                    elif npc.rect.collidepoint(pos) and not handled and len(enemy_group) != 0:
                        convo = True
                        notyet = True
                        notyet_sound = True
                for escape in exit_group:
                    if escape.rect.collidepoint(pos) and not handled and len(enemy_group) == 0:
                        print(level)
                        handled = True
                        if level == 0 :
                            level = 1
                            start_game = True
                            tutorial_complete = True
                        elif level == 1:
                            main_complete = True
                            level = 2
                            bg_images = []
                            for i in range(1,7):
                                bg_image = pygame.image.load(f'NightForest/NewLayers/{i}.png').convert_alpha()
                                bg_image= pygame.transform.scale(bg_image,(int(bg_image.get_width() *1.5), int(bg_image.get_height() *1.5)))
                                bg_images.append(bg_image)
                            bg_width = bg_images[0].get_width()
                            main_complete = True
                    elif escape.rect.collidepoint(pos) and not handled and len(enemy_group) == 0:
                        print("Talk to Mark")
                    elif escape.rect.collidepoint(pos) and not handled and boss_beaten:
                        if intro_fade.fade():
                            intro_fade.fade_counter = 0
                        if level == 2:
                            bg_scroll = 0
                            level = 0
                            bg_images = []
                            for i in range(1,6):
                                bg_image = pygame.image.load(f'NightForest/Layers/{i}.png').convert_alpha()
                                bg_image= pygame.transform.scale(bg_image,(int(bg_image.get_width() *1.5), int(bg_image.get_height() *1.5)))
                                bg_images.append(bg_image)
                            bg_width = bg_images[0].get_width()
                            
                            world_data = reset_level()
                            #load in level data and create world
                            with open(f'level{level}_data.csv', newline= '') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] =  int(tile)
                            world = World()
                            player, health_bar, enemy_bar = world.process_data(world_data)
                            
                            start_game = False
                            menu_state = "done"
                            
                            pygame.mixer.music.load('music/menu_track.wav')
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(-1, 0.0, 5000)
                            
                    elif escape.rect.collidepoint(pos) and not handled and len(enemy_group) != 0:
                        convo = True
                        noexit = True
                    elif escape.rect.collidepoint(pos) and not handled and level == 2 and boss_beaten == False:
                        print("Defeat her!")

   

                

        #key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                #add different facing idle animations
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_LSHIFT:
                sliding_left = False
                sliding_right = False


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                attacking = False
            if event.button == 3:
                handled  = False
                level_complete = False

    pygame.display.update()

pygame.quit()
