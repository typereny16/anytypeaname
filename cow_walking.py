'''
Created on Feb 18, 2015

@author: 33271
'''
import pygame
from healthBar import DrawHealthBar

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN    = (   0, 255,   0)
BLUE = (0, 128, 255)
 
class SpriteSheet(object):
    sprite_sheet = None
 
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name)
 
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
     
class Cow(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_up = []
    walking_frames_down = []
    
    first_right = True
    first_down = True
    second_right = True
    third_right = True
    first_up = True
    second_left = True
    third_right = True
    second_down = True
    fourth_right = True

    direction = "R"

    def __init__(self):
        super().__init__()
 
        sprite_sheet = SpriteSheet("I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\cow_walk.png")
        # Right Images
        image = sprite_sheet.get_image(25, 420, 83, 62)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(156, 420, 83, 62)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(287, 420, 83, 62)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(412, 420, 83, 62)
        self.walking_frames_r.append(image)
 
        # Left Images
        image = sprite_sheet.get_image(13, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(139, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(265, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(398, 164, 94, 59)
        self.walking_frames_l.append(image)

        # Up Images
        image = sprite_sheet.get_image(50, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(179, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(306, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(434, 38, 29, 76)
        self.walking_frames_up.append(image)        
 
        # Down Images
        image = sprite_sheet.get_image(50, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(179, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(306, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(434, 301, 28, 60)
        self.walking_frames_down.append(image)    
 
        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()
     
    def update(self):
        DrawHealthBar(cow.rect.x - 100, cow.rect.y - 30)
        self.rect.x += self.change_x
        pos = self.rect.x
        self.rect.y += self.change_y
        posy = self.rect.y
        
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        if self.direction == "UP":
            frame = (posy // 30) % len(self.walking_frames_up)
            self.image = self.walking_frames_up[frame]
        if self.direction == "DOWN":
            frame = (posy//30) % len(self.walking_frames_down)
            self.image = self.walking_frames_down[frame]
        if self.direction == "L":
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        
        if self.rect.x <50 and self.first_right == True:
            self.go_right()
            self.first_right = False
        if self.rect.x >=205 and self.first_right == False and self.first_down == True:
            self.stop()
            self.go_down()
            self.first_down = False
        if self.rect.y >= 350 and self.first_down == False and self.second_right == True:
            self.stop()
            self.go_right()
            self.second_right = False
        if self.rect.x >= 460 and self.first_up == True and self.second_right == False:
            self.stop()
            self.go_up()
            self.first_up = False
        if self.rect.y <=125 and self.first_up == False and self.third_right == True:
            self.stop()
            self.go_right()
            self.third_right = False
        if self.rect.x <= 350 and self.second_left == True and self.third_right == False:
            self.stop()
            self.go_up()
            self.second_left = False
        if self.rect.y <= 50 and self.second_left == False and self.third_right == True:
            self.stop()
            self.go_right()
            self.third_right =False
        if self.rect.x >= 685 and self.third_right==False and self.second_down == True:
            self.stop()
            self.go_down()
            self.second_down =False
        if self.rect.y >= 440 and self.second_down ==False and self.fourth_right==True:
            self.stop()
            self.go_right()
            self.fourth_right= False
     
    def go_left(self):
        self.change_x = -6
        self.direction = "L"
     
    def go_right(self):
        self.change_x = 6
        self.direction = "R"
    
    def go_up(self):
        self.change_y = -6
        self.direction = "UP"
    
    def go_down(self):
        self.change_y = 6
        self.direction = "DOWN"
     
    def stop(self):
        self.change_x = 0
        self.change_y = 0
        
class Pig(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_up = []
    walking_frames_down = []
    
    first_right = True
    first_down = True
    second_right = True
    first_left = True
    first_up = True
    second_left = True
    third_right = True

    direction = "R"

    def __init__(self):
        super().__init__()
 
        sprite_sheet = SpriteSheet("I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\pig_walk.png")
        # Right Images
        image = sprite_sheet.get_image(34, 436, 63, 34)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(163, 436, 63, 34)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(292, 436, 63, 34)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(419, 436, 63, 34)
        self.walking_frames_r.append(image)
 
        # Left Images
        image = sprite_sheet.get_image(13, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(139, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(265, 164, 94, 59)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(398, 164, 94, 59)
        self.walking_frames_l.append(image)

        # Up Images
        image = sprite_sheet.get_image(50, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(179, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(306, 38, 29, 76)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(434, 38, 29, 76)
        self.walking_frames_up.append(image)        
 
        # Down Images
        image = sprite_sheet.get_image(50, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(179, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(306, 301, 28, 60)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(434, 301, 28, 60)
        self.walking_frames_down.append(image)    
 
        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()
     
    def update(self):
        DrawHealthBar(cow.rect.x-100, cow.rect.y-30)
        self.rect.x += self.change_x
        pos = self.rect.x
        self.rect.y += self.change_y
        posy = self.rect.y
        
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        if self.direction == "UP":
            frame = (posy // 30) % len(self.walking_frames_up)
            self.image = self.walking_frames_up[frame]
        if self.direction == "DOWN":
            frame = (posy//30) % len(self.walking_frames_down)
            self.image = self.walking_frames_down[frame]
        if self.direction == "L":
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        
        if self.rect.x <30 and self.first_right == True:
            self.go_right()
            self.first_right = False
        if self.rect.x >=250 and self.first_right == False and self.first_down == True:
            self.stop()
            self.go_down()
            self.first_down = False
        if self.rect.y >= 450 and self.first_down == False and self.second_right == True:
            self.stop()
            self.go_right()
            self.second_right = False
        if self.rect.x >= 650 and self.first_up == True and self.second_right == False:
            self.stop()
            self.go_up()
            self.first_up = False
        if self.rect.y <=250 and self.first_up == False and self.first_left == True:
            self.stop()
            self.go_left()
            self.first_left = False
        if self.rect.x <= 350 and self.second_left == True and self.first_left == False:
            self.stop()
            self.go_up()
            self.second_left = False
        if self.rect.y <= 50 and self.second_left == False and self.third_right == True:
            self.stop()
            self.go_right()
            self.third_right =False
     
    def go_left(self):
        self.change_x = -6
        self.direction = "L"
     
    def go_right(self):
        self.change_x = 6
        self.direction = "R"
    
    def go_up(self):
        self.change_y = -6
        self.direction = "UP"
    
    def go_down(self):
        self.change_y = 6
        self.direction = "DOWN"
     
    def stop(self):
        self.change_x = 0
        self.change_y = 0    
        
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)

clock= pygame.time.Clock()

cow = Cow()
pig = Pig()