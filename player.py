import pygame, sys
import assets
from level import snap, TILE_SIZE

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.gold = 0

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
        if level.take_gold(self.x, self.y):
            self.gold += 1

    def zap(self, level, left):
        if not level.person_collides(snap(self.x), self.y) and\
                level.zap(snap(self.x),self.y,left):
            self.x = snap(self.x)
    
    def update(self, level):
        if level.person_collides(self.x, self.y):
            self.dead = True
            return
        
        if level.person_floats(self.x, self.y):
            if not level.person_collides(snap(self.x), self.y+3):
                self.y += 3
                self.x = snap(self.x)

    def draw(self, windowSurface, xoff=0, yoff=0):
        if not self.dead:
            windowSurface.blit(assets.people.player_stand,\
                                   (self.x+xoff, self.y+yoff))
