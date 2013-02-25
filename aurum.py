import pygame, sys
from pygame.locals import *
import level, player, guard
from player import collides

window_width, window_height = 640, 480

pygame.init()
pygame.display.set_caption("Aurum")
fpsClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((window_width, window_height))

import assets

bgColor = pygame.Color(0,0,0)

l = level.Level("level.lvl")

x_corner = (window_width - l.width * level.TILE_SIZE)/2
y_corner = (window_height - l.height * level.TILE_SIZE)/2

# p stands for Peter, not player
p = player.Player(l.start_x,l.start_y)
guards = [guard.Guard(240,0)]

while True:
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
    if keys[K_DOWN]:
        p.move(l,"d")
    if keys[K_z]:
        p.zap(l,True)
    if keys[K_x]:
        p.zap(l,False)
        
    p.update(l)
    for g in guards:
        g.update(l)
    
    windowSurface.fill(bgColor)
    l.draw(windowSurface, x_corner, y_corner, p.gold == l.gold)
    p.draw(windowSurface, x_corner, y_corner)
    for g in guards:
        g.draw(windowSurface, x_corner, y_corner)
    pygame.display.update()

    for g in guards:
        if collides(p,g):
            p.dead = True
    
    if p.dead:
        print "You have died: Game Over"
        pygame.quit()
        sys.exit()
    if p.winner:
        print "You have won!"
        pygame.quit()
        sys.exit()
    
    fpsClock.tick(30)
#finally:
#    # TODO: finalization stuff
#    pygame.quit()
