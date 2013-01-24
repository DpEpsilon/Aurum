import pygame, sys
import assets

PLAYER_SIZE = 24

def snap(d):
    if d % PLAYER_SIZE < PLAYER_SIZE/2:
        d -= d % PLAYER_SIZE
    else:
        d += PLAYER_SIZE - d % PLAYER_SIZE
    return d

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False

    def move(self, level, direction):
        if direction is "l":
            if not level.person_collides(self.x-3,self.y):
                self.x -= 3
        elif direction is "r":
            if not level.person_collides(self.x+3,self.y):
                self.x += 3
        elif direction is "u":
            if level.person_climbs(self.x,self.y) and not\
                    level.person_collides(snap(self.x),self.y-3):
                self.y -= 3
                self.x = snap(self.x)
        elif direction is "d":
            if level.person_climbs(self.x,self.y,False) and not\
                    level.person_collides(snap(self.x),self.y+3):
                self.y += 3
                self.x = snap(self.x)

    def zap(self, level, left):
        if self.y % PLAYER_SIZE == 0 and\
                not level.person_collides(snap(self.x), self.y):
            self.x = snap(self.x)
            level.zap(self.x,self.y,left)
                
    def update(self, level):
        if level.person_collides(self.x, self.y):
            print "HUEH, ur dead"
            self.dead = True
            return
        
        if level.person_floats(self.x, self.y):
            if not level.person_collides(snap(self.x), self.y+3):
                self.y += 3
                self.x = snap(self.x)

    def draw(self, windowSurface, xoff=0, yoff=0):
        windowSurface.blit(assets.people.player_stand,\
                               (self.x+xoff, self.y+yoff))
