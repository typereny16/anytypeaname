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

class LoadingBar():
    
    global LOADING_SCREEN, LOADING_PAGE    

    number_done = 0
    percentage = None
    percent = None

    def update(self):
        logo = pygame.image.load("I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\main_log.jpg")
        screen.blit(logo, [0, 0])
        
loading_bar = LoadingBar()

font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 48)

fontes = pygame.font.get_fonts()
print (fontes)

arrow = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\selected_arrow.png')
desk_easy = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\desk.png')
desk_medium = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\desk2.png')
desk_hard=pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\desk3.png')

LOADING_SCREEN = True
LOADING_PAGE =1
(posX, posY) = pygame.mouse.get_pos()
selected_easy = False
selected_medium = False
selected_hard = False
# -------- Instruction Page Loop -----------
while LOADING_SCREEN:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done=True 
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 2 and posX > 208 and posY > 239 and posX < 375 and posY < 260:
            LOADING_PAGE = 3
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 2 and posX > 196 and posY > 179 and posX < 389 and posY < 203:
            LOADING_PAGE = 4
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 3 and posX < 104 and posY < 578 and posX > 13 and posY > 553:
            LOADING_PAGE = 2
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 3 and posX<251 and posY<205 and posX >201 and posY>187:
            selected_easy = True
            selected_hard=False
            selected_medium=False
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 3 and posX<375 and posY<205 and posX>286 and posY>186:
            selected_easy = False
            selected_medium = True
            selected_hard= False
        if event.type == pygame.MOUSEBUTTONDOWN and LOADING_PAGE == 3 and posX<461 and posY<205 and posX>406 and posY>187:
            selected_hard = True
            selected_easy=False
            selected_medium=False


    screen.fill(BLACK)

    if LOADING_PAGE == 1: 
        screen.fill(WHITE)
        loading_bar.number_done +=1
        print (loading_bar.number_done)
        if loading_bar.number_done>30:
            loading_bar.update()
        if loading_bar.number_done ==50:
            LOADING_PAGE = 2
            
    if LOADING_PAGE == 2:
        background = pygame.image.load('I:\Mr. Neville\HS Computers\Tower Defense\Project\Project\mayb_menu_background.png')
        screen.blit(background, [0,0]) 
        (posX, posY) = pygame.mouse.get_pos()
        
        text=menu_font.render('PLAY GAME', True, WHITE)
        screen.blit(text, [194, 175])
        if posX > 196 and posY > 179 and posX < 389 and posY < 203:
            text = menu_font.render('PLAY GAME', True, GREEN)
            screen.blit(text, [194, 175])
            
        text=menu_font.render('SETTINGS', True, WHITE)
        screen.blit(text, [208, 235])
        if posX > 208 and posY > 239 and posX < 375 and posY < 260:
            text = menu_font.render('SETTINGS', True, GREEN)
            screen.blit(text, [208, 235])        
    
    if LOADING_PAGE == 3:
        posX, posY = pygame.mouse.get_pos()
        print (posX, posY)
        text = menu_font.render('--- SETTINGS ---', True, WHITE)
        screen.blit(text, [280, 15])
        
        text = menu_font.render('BACK', True, WHITE)
        screen.blit(text, [10, 550])
        if posX < 104 and posY < 578 and posX > 13 and posY > 553:
            text = menu_font.render('BACK', True, GREEN)
            screen.blit(text, [10, 550])
            
        text = font.render('MODE:', True, RED)
        screen.blit(text, [200, 150])
        
        text = font.render('Easy', True, WHITE)
        screen.blit(text, [200, 185])
        if posX<251 and posY<205 and posX >201 and posY>187:
            text = font.render('Easy', True, GREEN)
            screen.blit(text, [200, 185])
        if selected_easy == True:
            screen.blit(arrow, [180, 185])
            screen.blit(desk_easy, [450, 250])
            
        text = font.render('Medium', True, WHITE)
        screen.blit(text, [285, 185])
        if posX<375 and posY<205 and posX>286 and posY>186:
            text = font.render('Medium', True, GREEN)
            screen.blit(text, [285, 185])  
        if selected_medium == True:
            screen.blit(arrow, [265, 185])  
            screen.blit(desk_medium, [450, 250])
            
        text = font.render('Hard', True, WHITE)
        screen.blit(text, [405, 185])
        if posX<461 and posY<205 and posX>406 and posY>187:
            text = font.render('Hard', True, GREEN)
            screen.blit(text, [405, 185])
        if selected_hard == True:
            screen.blit(arrow, [385, 185])
            screen.blit(desk_hard, [450, 250])
            
    if LOADING_PAGE == 4:
        LOADING_SCREEN = False    
        
    clock.tick(60)

    pygame.display.flip()