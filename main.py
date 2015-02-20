import pygame
import math
from healthBar import DrawHealthBar
import gui
from cow_walking import Cow, Pig
import test_arrows
import bullet_test

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

BULLET_SPEED = 2

pygame.init()

size=[800,600]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("SEMESTER 2 - PROJECT")
BACKGROUND = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\zfarm_map.png')
clock = pygame.time.Clock()

gui.LoadingBar()

active_cow = pygame.sprite.Group()
cow = Cow()
active_cow.add(cow)
bullet_list = pygame.sprite.Group()

arrow = test_arrows.Arrow()

font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 48)

arrows = True
shooting_arrows= False
done = False
# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done=True        

    screen.blit(BACKGROUND, [0, 0])
    
    if arrows == True:
        for test_arrows.pointingx, test_arrows.pointingy in ((450, 500), (250, 300)):
            shooting_arrows = True
            degrees = test_arrows.getAngle(test_arrows.pointingx, test_arrows.pointingy, cow.rect.x, cow.rect.y)
        
            # rotate arrows
            rotatedSurf = pygame.transform.rotate(test_arrows.arrow, degrees)
            rotatedRect = rotatedSurf.get_rect()
            rotatedRect.center = (test_arrows.pointingx, test_arrows.pointingy)
            screen.blit(rotatedSurf, rotatedRect)
            bullet = bullet_test.Bullet(pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\Airless.png'))       
                
    DrawHealthBar(cow.rect.x -15, cow.rect.y-20)
    """DrawHealthBar.rect_changex -= 1
    print (DrawHealthBar.rect_changex)
    if DrawHealthBar.rect_changex < 0:
        DrawHealthBar.rect_changex = 0
        active_cow.remove(cow)
        active_cow.update()
        text = font.render("Yo cow is dead son", True, RED)
        screen.blit(text, [200, 300])"""
    
    active_cow.update()
    active_cow.draw(screen)
    bullet_list.update()
    bullet_list.draw(screen)
    
    clock.tick(20)

    pygame.display.flip()
    
pygame.quit ()