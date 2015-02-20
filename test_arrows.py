'''
Created on Feb 18, 2015

@author: 33271
'''
import pygame
import math

WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
BROWN    = (139,  69,  19)
DARKGRAY = (128, 128, 128)

WINDOWWIDTH = 800
WINDOWHEIGHT = 600 

pygame.init()
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

arrow = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\selected_arrow.png')

class Arrow():
    def __init__(self):
        self.image = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\selected_arrow.png')
        self.rect = self.image.get_rect()

def getAngle(x1, y1, x2, y2):
    # 0 for right, 90 for up, 180 for left, 270 for down
    rise = y1 - y2
    run = x1 - x2
    angle = math.atan2(run, rise) # get angle in radians
    angle = angle * (180 / math.pi) # convert to degrees
    angle = (angle + 90) % 360 #for right-facing sprite
    return angle