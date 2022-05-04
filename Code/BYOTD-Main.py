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

maptiles = [] # World map, follows (tile x, tile y, tile type, tile rect)
objecttiles = [] # Object map, follows (tile x, tile y, tile type, tile rect, tile id, nbt 1)
objectpositions = [] # Object position map, follows (world x, world y)
tilecount = 0
tilecount2 = 0
click = False
mouseholding = -1

loadgrass = pygame.image.load('Tiles\Grass.png').convert()
loadpath = pygame.image.load('Tiles\Path.png').convert()

loadwirerl = pygame.image.load('Tiles\Wire\WireRightLeft.png').convert()
loadwire1rl = pygame.image.load('Tiles\Wire\Wire1RightLeft.png').convert()
loadwireud = pygame.image.load('Tiles\Wire\WireUpDown.png').convert()
loadwire1ud = pygame.image.load('Tiles\Wire\Wire1UpDown.png').convert()
loadwirepartial = pygame.image.load('Tiles\Wire\WirePartial.png').convert()
loadwire1partial = pygame.image.load('Tiles\Wire\Wire1Partial.png').convert()
loadwirespot = pygame.image.load('Tiles\Wire\WireSpot.png').convert()

loadwirerl.set_colorkey((0,0,0))
loadwire1rl.set_colorkey((0,0,0))
loadwireud.set_colorkey((0,0,0))
loadwire1ud.set_colorkey((0,0,0))
loadwirepartial.set_colorkey((0,0,0))
loadwire1partial.set_colorkey((0,0,0))
loadwirespot.set_colorkey((0,0,0))

wirerl = pygame.transform.scale(loadwirerl, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wire1rl = pygame.transform.scale(loadwire1rl, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wireud = pygame.transform.scale(loadwireud, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wire1ud = pygame.transform.scale(loadwire1ud, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wirepartialscaled = pygame.transform.scale(loadwirepartial, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wire1partialscaled = pygame.transform.scale(loadwire1partial, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
wirespot = pygame.transform.scale(loadwirespot, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))

wireu = pygame.transform.rotate(wirepartialscaled, 0)
wired = pygame.transform.rotate(wirepartialscaled, 180)
wirel = pygame.transform.rotate(wirepartialscaled, 90)
wirer = pygame.transform.rotate(wirepartialscaled, -90)

wireu1 = pygame.transform.rotate(wire1partialscaled, 0)
wired1 = pygame.transform.rotate(wire1partialscaled, 180)
wirel1 = pygame.transform.rotate(wire1partialscaled, 90)
wirer1 = pygame.transform.rotate(wire1partialscaled, -90)

loadbattery = pygame.image.load('Tiles\\Battery.png').convert()
loadbattery.set_colorkey((0,0,0))

grass = pygame.transform.scale(loadgrass, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
path = pygame.transform.scale(loadpath, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))
battery = pygame.transform.scale(loadbattery, (round(WINDOW_SIZE[1]/14),round(WINDOW_SIZE[1]/14)))

with open('Maps\\1.txt', 'rb') as fp:
                    maptiles = pickle.load(fp)

def tilecheck(tile, check, direction):
    tilex, tiley = tile
    checkx, checky = check
    if direction == 0:
        if checkx == tilex-1 and checky == tiley:
            return True
        else: 
            return False
    elif direction == 1:
        if checkx == tilex+1 and checky == tiley:
            return True
        else: 
            return False
    elif direction == 2:
        if checky == tiley-1 and checkx == tilex:
            return True
        else: 
            return False
    elif direction == 3:
        if checky == tiley+1 and checkx == tilex:
            return True
        else: 
            return False

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
            if event.key == K_9:
                with open('Maps\\1.txt', 'rb') as fp:
                    maptiles = pickle.load(fp)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    screen.fill((0,0,255))

    # MOUSE
    mx, my = pygame.mouse.get_pos()
    mouse = pygame.Rect(mx,my,1,1)

    # MAP
    size = round(WINDOW_SIZE[1]/14)
    
    # MAP HANDLER
    for tile in maptiles:
        # Click Handler
        rect = tile[3]
        # DRAW TILE HANDLER
        if tile[2] == 0:
            pygame.draw.rect(screen, (255,255,255), rect, 1)
        elif tile[2] == 1:
            screen.blit(grass, rect)
        elif tile[2] == 2:
            screen.blit(path, rect)
    
    # INITIALIZE OBJECT MAP
    if tilecount2 <= 293:
        for y in range(14):
            for x in range(21):
                rect = pygame.Rect(0 + (x*size), y*size, size, size)
                objectpositions.append([x, y])
                objecttiles.append([rect.x, rect.y, 1, rect, tilecount2, 0])
                tilecount2 += 1

    # OBJECT MAP HANDLER
    for tile in objecttiles:
        # Click Handler
        rect = tile[3]
        lefttile = tile[4] - 1
        righttile = tile[4] + 1
        toptile = tile[4] - 21
        bottomtile = tile[4] + 21
        if rect.collidepoint((mx, my)):
            pygame.draw.rect(screen, (0,0,255), rect) # Mouse hover
            # CLICK HANDLER
            if click:
                if tile[2] == 3:
                    for tile in objecttiles:
                        if tile[2] == 2:
                            tile[2] = 1
                            tile[5] = 0
                    tile[2] = 0
                tile[2] = mouseholding  
                tile[5] = 0
                if mouseholding != 1: 
                    mouseholding = 0
            print(tile)
        else:
            # DRAW TILE AND TILE MECHANICS HANDLER
            # Wire
            if tile[2] == 1: 
                # Logic
                if tilecheck(objectpositions[tile[4]], objectpositions[lefttile], 0): # if tile is next to left tile
                    if objecttiles[lefttile][2] == 3 or objecttiles[lefttile][2] == 2: # if that tile is lit wire or battery
                        if objecttiles[lefttile][2] == 3: # if its a battery
                            tile[5] = 9 # string count = 9
                            tile[2] = 2 # tile is lit
                        elif objecttiles[lefttile][2] == 2: # if its a lit wire
                            if objecttiles[lefttile][5] > 0 and objecttiles[lefttile][5] > tile[5]: # if left tile's string count is more than 0
                                tile[5] = objecttiles[lefttile][5] - 1 # this string count = left string count - 1
                                tile[2] = 2 # tile is lit

                if righttile < len(objecttiles): # if right tile is valid
                    if tilecheck(objectpositions[tile[4]], objectpositions[righttile], 1): # if tile is next to right tile
                        if objecttiles[righttile][2] == 3 or objecttiles[righttile][2] == 2: # if that tile is a wire or a battery
                            if objecttiles[righttile][2] == 3: # if tile is a battery
                                tile[5] = 9 # string count = 9
                                tile[2] = 2 # tile is lit
                            elif objecttiles[righttile][2] == 2: # if its a lit wire
                                if objecttiles[righttile][5] > 0 and objecttiles[righttile][5] > tile[5]: # if right tile string count is more than 0
                                    tile[5] = objecttiles[righttile][5] - 1 # this string count = right string count - 1
                                    tile[2] = 2 # tile is lit

                if tilecheck(objectpositions[tile[4]], objectpositions[toptile], 2):
                    if objecttiles[toptile][2] == 3 or objecttiles[toptile][2] == 2:
                        if objecttiles[toptile][2] == 3:
                            tile[5] = 9
                            tile[2] = 2
                        else:
                            if objecttiles[toptile][5] > 0 and objecttiles[toptile][5] > tile[5]:
                                tile[5] = objecttiles[toptile][5] - 1
                                tile[2] = 2
                
                if bottomtile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[bottomtile], 3):
                        if objecttiles[bottomtile][2] == 3 or objecttiles[bottomtile][2] == 2:
                            if objecttiles[bottomtile][2] == 3:
                                tile[5] = 9
                                tile[2] = 2
                            else:
                                if objecttiles[bottomtile][5] > 0 and objecttiles[bottomtile][5] > tile[5]:
                                    tile[5] = objecttiles[bottomtile][5] - 1
                                    tile[2] = 2
                
                # Draw Logic
                screen.blit(wirespot, rect)
                # right
                if righttile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[righttile], 1):
                        if objecttiles[righttile][2] == 1 or objecttiles[righttile][2] == 2 or objecttiles[righttile][2] == 3:
                          screen.blit(wirer, rect)
                # left
                if tilecheck(objectpositions[tile[4]], objectpositions[lefttile], 0):
                    if objecttiles[lefttile][2] == 1 or objecttiles[lefttile][2] == 2 or objecttiles[lefttile][2] == 3:
                        screen.blit(wirel, rect)
                # down
                if bottomtile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[bottomtile], 3):
                       if objecttiles[bottomtile][2] == 1 or objecttiles[bottomtile][2] == 2 or objecttiles[bottomtile][2] == 3:
                           screen.blit(wired, rect)
                # up
                if tilecheck(objectpositions[tile[4]], objectpositions[toptile], 2):
                    if objecttiles[toptile][2] == 1 or objecttiles[toptile][2] == 2 or objecttiles[toptile][2] == 3:
                        screen.blit(wireu, rect)

            # Lit Wire
            elif tile[2] == 2:
                # Logic
                if tilecheck(objectpositions[tile[4]], objectpositions[lefttile], 0): # if tile is next to left tile
                    if objecttiles[lefttile][2] == 3 or objecttiles[lefttile][2] == 2: # if that tile is lit wire or battery
                        if objecttiles[lefttile][2] == 3: # if its a battery
                            tile[5] = 9 # string count = 9
                            tile[2] = 2 # tile is lit
                        elif objecttiles[lefttile][2] == 2: # if its a lit wire
                            if objecttiles[lefttile][5] > 0 and objecttiles[lefttile][5] > tile[5]: # if left tile's string count is more than 0
                                tile[5] = objecttiles[lefttile][5] - 1 # this string count = left string count - 1
                                tile[2] = 2 # tile is lit

                if righttile < len(objecttiles): # if right tile is valid
                    if tilecheck(objectpositions[tile[4]], objectpositions[righttile], 1): # if tile is next to right tile
                        if objecttiles[righttile][2] == 3 or objecttiles[righttile][2] == 2: # if that tile is a wire or a battery
                            if objecttiles[righttile][2] == 3: # if tile is a battery
                                tile[5] = 9 # string count = 9
                                tile[2] = 2 # tile is lit
                            elif objecttiles[righttile][2] == 2: # if its a lit wire
                                if objecttiles[righttile][5] > 0 and objecttiles[righttile][5] > tile[5]: # if right tile string count is more than 0
                                    tile[5] = objecttiles[righttile][5] - 1 # this string count = right string count - 1
                                    tile[2] = 2 # tile is lit

                if tilecheck(objectpositions[tile[4]], objectpositions[toptile], 2):
                    if objecttiles[toptile][2] == 3 or objecttiles[toptile][2] == 2:
                        if objecttiles[toptile][2] == 3:
                            tile[5] = 9
                            tile[2] = 2
                        else:
                            if objecttiles[toptile][5] > 0 and objecttiles[toptile][5] > tile[5]:
                                tile[5] = objecttiles[toptile][5] - 1
                                tile[2] = 2
                
                if bottomtile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[bottomtile], 3):
                        if objecttiles[bottomtile][2] == 3 or objecttiles[bottomtile][2] == 2:
                            if objecttiles[bottomtile][2] == 3:
                                tile[5] = 9
                                tile[2] = 2
                            else:
                                if objecttiles[bottomtile][5] > 0 and objecttiles[bottomtile][5] > tile[5]:
                                    tile[5] = objecttiles[bottomtile][5] - 1
                                    tile[2] = 2
                
                # Draw Logic
                # right
                if righttile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[righttile], 1):
                        if objecttiles[righttile][2] == 1 or objecttiles[righttile][2] == 2 or objecttiles[righttile][2] == 3:
                          screen.blit(wirer1, rect)
                # left
                if tilecheck(objectpositions[tile[4]], objectpositions[lefttile], 0):
                    if objecttiles[lefttile][2] == 1 or objecttiles[lefttile][2] == 2 or objecttiles[lefttile][2] == 3:
                        screen.blit(wirel1, rect)
                # down
                if bottomtile < len(objecttiles):
                    if tilecheck(objectpositions[tile[4]], objectpositions[bottomtile], 3):
                       if objecttiles[bottomtile][2] == 1 or objecttiles[bottomtile][2] == 2 or objecttiles[bottomtile][2] == 3:
                           screen.blit(wired1, rect)
                # up
                if tilecheck(objectpositions[tile[4]], objectpositions[toptile], 2):
                    if objecttiles[toptile][2] == 1 or objecttiles[toptile][2] == 2 or objecttiles[toptile][2] == 3:
                        screen.blit(wireu1, rect)
                
                        
            # Battery
            elif tile[2] == 3:
                screen.blit(battery, rect)
            else:
                pygame.draw.rect(screen, (255,255,255), rect, 1)
    
    # OBJECTS
    wirerect = pygame.Rect(1100, 10, size, size)
    screen.blit(wirerl, wirerect)
    batteryrect = pygame.Rect(1100, 10+size, size, size)
    screen.blit(battery, batteryrect)

    if wirerect.collidepoint((mx, my)):
        if click:
            mouseholding = 1
    if batteryrect.collidepoint((mx, my)):
        if click:
            mouseholding = 3
            
    # DRAW
    if mouseholding == -1:
        pygame.draw.rect(screen, (0,255,0), mouse)
    elif mouseholding == 1:
        screen.blit(wirerl, mouse)
    elif mouseholding == 3:
        screen.blit(battery, mouse)
    pygame.display.flip() # Update screen

    click = False
