import pygame, sys, time
import assets

ZAP_TIMEOUT = 10.0
ZAPPABLES = '#'
SOLIDS = '#='
LADDER = '^'
WEIGHT_SUPPORTING = '#=^'
PLAYER_START = '$'
GOLD = 'g'
EMPTY = '.'

TILE_SIZE = 24

def snap(d):
    if d % TILE_SIZE < TILE_SIZE/2:
        d -= d % TILE_SIZE
    else:
        d += TILE_SIZE - d % TILE_SIZE
    return d

class Tile(object):
    def __init__(self, character):
        self.zap_time = 0.0
        self.is_gold = character in GOLD
        
        if character in GOLD:
            self.character = EMPTY
        else:
            self.character = character

    def zap(self):
        t = time.time()
        if not self.is_zapped() and self.is_zappable():
            self.zap_time = time.time()
            return True
        return False

    def is_zappable(self):
        return self.character in ZAPPABLES

    def is_zapped(self):
        return self.character in ZAPPABLES and\
            time.time() < self.zap_time + ZAP_TIMEOUT

    def is_solid(self):
        return self.character in SOLIDS and not self.is_zapped()

    def is_weight_supporting(self):
        return self.character in WEIGHT_SUPPORTING and\
            not self.is_zapped()

    def is_climbable(self):
        return self.character in LADDER

    def is_player_start(self):
        return self.character in PLAYER_START

    def is_empty(self):
        return self.character in EMPTY

    def take_gold(self):
        if self.is_gold:
            self.is_gold = False
            return True
        else:
            return False
    
    def draw(self,windowSurface,x,y):
        if not self.is_zapped():
            if self.character == '#':
                windowSurface.blit(assets.tiles.dirt, (x, y))
            elif self.character == '=':
                windowSurface.blit(assets.tiles.stone, (x, y))
            elif self.character == '^':
                windowSurface.blit(assets.tiles.ladder, (x, y))
        if self.is_gold:
            windowSurface.blit(assets.tiles.gold, (x, y))
        
        

class Level(object):
    def __init__(self, location):
        self.tiles = [[Tile(c) for c in line.strip()] for line in open(location)]

        if len(self.tiles) > 0:
            self.width = len(self.tiles[0])
        else:
            self.width = 0
        
        # Check that width is consistent
        i = 0
        while i < len(self.tiles):
            if len(self.tiles[i]) == 0:
                self.tiles.pop(i)
                continue
            if len(self.tiles[i]) != self.width:
                raise Exception("Level file is of inconsistent width")
            i += 1
        
        self.height = len(self.tiles)
        self.start_x = 0
        self.start_y = 0
        self.gold = 0
        
        for y in xrange(self.height):
            for x in xrange(self.width):
                if self.tiles[y][x].is_player_start():
                    self.start_x = x*TILE_SIZE
                    self.start_y = y*TILE_SIZE
                if self.tiles[y][x].is_gold:
                    self.gold += 1

    def person_collides(self, x,y):
        # Boundary test
        if x < 0 or x > (self.width - 1) * TILE_SIZE or\
                y < 0 or y > (self.height - 1) * TILE_SIZE:
            return True
        
        if self.tiles[y/TILE_SIZE][x/TILE_SIZE].is_solid():
            return True
        if x % TILE_SIZE > 0 and\
                self.tiles[y/TILE_SIZE][x/TILE_SIZE+1].is_solid():
            return True
        if y % TILE_SIZE > 0 and\
                self.tiles[y/TILE_SIZE+1][x/TILE_SIZE].is_solid():
            return True
        if x % TILE_SIZE > 0 and y % TILE_SIZE > 0 and\
                self.tiles[y/TILE_SIZE+1][x/TILE_SIZE+1].is_solid():
            return True
        
        return False
    
    
    def person_floats(self,x,y):
        assert(not self.person_collides(x,y))
        
        if y % TILE_SIZE != 0 and\
                not self.tiles[(y+TILE_SIZE-1)/TILE_SIZE][(x+TILE_SIZE/2)/TILE_SIZE]\
                .is_climbable():
            return True
        if y == (self.height - 1) * TILE_SIZE:
            return False
        if x % TILE_SIZE < TILE_SIZE/2:
            return not self.tiles[y/TILE_SIZE+1][x/TILE_SIZE].is_weight_supporting()
        else:
            return not self.tiles[y/TILE_SIZE+1][x/TILE_SIZE+1].is_weight_supporting()

    def person_climbs(self,x,y,up=True):
        assert(not self.person_collides(x,y))

        if not up and y >= TILE_SIZE * (self.height-1):
            return False
        
        shift = 1 if up else 0
        
        if x % TILE_SIZE < TILE_SIZE/2:
            return self.tiles[(y+TILE_SIZE-shift)/TILE_SIZE][x/TILE_SIZE]\
                .is_climbable()
        else:
            return self.tiles[(y+TILE_SIZE-shift)/TILE_SIZE][x/TILE_SIZE+1]\
                .is_climbable()


    def zap(self,x,y,left):
        assert(not self.person_collides(x,y))
        assert(x%TILE_SIZE == 0)
        
        xt = x/TILE_SIZE + (-1 if left else 1)
        yt = y/TILE_SIZE + 1

        if xt >= 0 and xt < self.width and yt < self.height and\
                not self.person_floats(x,y) and\
                self.tiles[yt-1][xt].is_empty():
            return self.tiles[yt][xt].zap()
        return False

    def take_gold(self, x, y):
        xt = snap(x)/TILE_SIZE
        yt = snap(y)/TILE_SIZE
        return self.tiles[yt][xt].take_gold()
        
            
    def draw(self, windowSurface, xoff=0, yoff=0):
        for x in xrange(self.width):
            for y in xrange(self.height):
                self.tiles[y][x].draw(windowSurface,\
                                          x*TILE_SIZE+xoff, y*TILE_SIZE+yoff)
