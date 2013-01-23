import pygame, sys
from pygame.locals import *
import level, player

pygame.init()
pygame.display.set_caption("Aurum")
fpsClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((640, 480))

import assets

bgColor = pygame.Color(0,0,0)

l = level.Level("level.lvl")

# p stands for Peter, not player
p = player.Player(l.start_x,l.start_y)

while True:
    windowSurface.fill(bgColor)
    l.draw(windowSurface)
    p.draw(windowSurface, 0, 0)
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            # TODO: finalization stuff
            pygame.quit()
            sys.exit()
    if keys[K_LEFT]:
        p.move(l,"l")
    if keys[K_RIGHT]:
        p.move(l,"r")
    if keys[K_UP]:
        p.move(l,"u")
    
    p.update(l)
    pygame.display.update()
    fpsClock.tick(30)
#finally:
#    # TODO: finalization stuff
#    pygame.quit()
