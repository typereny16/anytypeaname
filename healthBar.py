'''
Created on Feb 18, 2015

@author: 33271
'''
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

pygame.init()

size=[800,600]
screen=pygame.display.set_mode(size)
clock = pygame.time.Clock()

class DrawHealthBar():
    rect_loadx = 105
    rect_loady = 135
    rect_changex = 73

    def __init__(self, rect_x, rect_y):
        self.rect_x= rect_x
        self.rect_y = rect_y
        pygame.draw.rect(screen, WHITE, [self.rect_x, self.rect_y, 80, 15])
        pygame.draw.rect(screen, RED, [self.rect_x+3, self.rect_y+3, self.rect_changex,8])