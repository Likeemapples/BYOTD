# BYOTD #
#########

import pygame, sys, random, math, json, pickle
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("BYOTD")
WINDOW_SIZE = (1280,720)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300,200))

tiles = [] # World map, follows (tile x, tile y, tile type)
tilecount = 0
click = False

loadgrass = pygame.image.load('Tiles\Grass.png').convert()
loadpath = pygame.image.load('Tiles\Path.png').convert()

grass = pygame.transform.scale(loadgrass, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
path = pygame.transform.scale(loadpath, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
while True:

    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_0:
                with open('Maps\\1.txt','wb') as fp:
                    pickle.dump(tiles,fp)
            if event.key == K_9:
                with open('Maps\\1.txt', 'rb') as fp:
                    tiles = pickle.load(fp)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    screen.fill((0,0,0))

    # MOUSE
    mx, my = pygame.mouse.get_pos()
    mouse = pygame.Rect(mx,my,1,1)

    # MAP
    size = round(WINDOW_SIZE[1]/14)
    
    # INITIALIZE MAP
    if tilecount <= 293:
        for y in range(14):
            for x in range(21):
                rect = pygame.Rect(0 + (x*size), y*size, size, size)
                tilecount += 1
                tiles.append([rect.x, rect.y, 1, rect, tilecount])
    
    # MAP HANDLER
    for tile in tiles:
        # Click Handler
        rect = tile[3]
        if rect.collidepoint((mx, my)):
            pygame.draw.rect(screen, (0,0,255), rect) # Mouse hover
            #screen.blit(grass, rect)
            # CLICK HANDLER
            if click:
                if tile[2] <= 2:
                    tile[2] += 1
                if tile[2] == 3:
                    tile[2] = 0    
            print(rect.x, rect.y, tile[2], rect, tile[4])
        else:
            # DRAW TILE HANDLER
            if tile[2] == 0:
                pygame.draw.rect(screen, (255,255,255), rect, 1)
            elif tile[2] == 1:
                screen.blit(grass, rect)
            elif tile[2] == 2:
                screen.blit(path, rect)
            
            
            
    
    # DRAW
    pygame.draw.rect(screen, (0,255,0), mouse)
    pygame.display.flip() # Update screen

    click = False
