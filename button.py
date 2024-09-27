import pygame

class Button():
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.image = pygame.transform.scale(self.image, (int(width*0.5), int(height*0.5)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self,screen):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked coniditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
   
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
