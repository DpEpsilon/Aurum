import pygame, sys
import assets
from player import Player
from level import snap, TILE_SIZE

class Guard(Player):
    def __init__(self, x, y):
        super(Guard, self).__init__(x, y)
    
    def zap(self, *args, **kwargs):
        raise NotImplemented("Guard cannot zap the group.")
    
    def update(self, level):
        super(Guard, self).update(level)
        
        # TODO: pathfinding and movement
    
    def draw(self, windowSurface, xoff=0, yoff=0):
        if not self.dead:
            windowSurface.blit(assets.people.guard_stand,\
                                   (self.x+xoff, self.y+yoff))
