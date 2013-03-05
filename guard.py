import pygame
import sys
import assets
import random
import Queue
from player import Player
from level import snap, TILE_SIZE

# directions
dx = [0,1,0,-1]
dy = [-1,0,1,0]
dd = ['u','r','d','l']

# directions for ladder-start pathfinding special case
# see ai_search()
ladder_dx = [0,1,1,0,-1,-1]
ladder_dy = [-1,0,0,1,0,0]
ladder_dd = ['u','u','d','d','d','u']

class Guard(Player):
	def __init__(self, x, y):
		super(Guard, self).__init__(x, y)
	
	def zap(self, *args, **kwargs):
		raise NotImplemented("Guard cannot zap the group.")
	
	def update(self, level, player):
		search_result = ai_search(self.x, self.y, None, player.y,\
								  level, player.gold==level.gold)
		print search_result
		self.move(level, search_result)
		
		super(Guard, self).update(level)
				
	def draw(self, windowSurface, xoff=0, yoff=0):
		if not self.dead:
			windowSurface.blit(assets.people.guard_stand,\
								   (self.x+xoff, self.y+yoff))

	def take_gold(self, level):
		pass # TODO: randomly take gold
	
def ai_search(x,y,x_goal,y_goal,level,got_all_gold=False):
	q = Queue.Queue()
	seen = [[False for i in xrange(level.width)]\
				for j in xrange(level.height)]
	
	# corresponding tile coordinates
	tx = snap(x)/TILE_SIZE
	ty = (y+TILE_SIZE-1)/TILE_SIZE
	tx_goal = None
	ty_goal = None
	if x_goal is not None:
		tx_goal = snap(x_goal)/TILE_SIZE
	if y_goal is not None:
		ty_goal = (y_goal+TILE_SIZE-1)/TILE_SIZE
	
	if level.person_floats(x,y,got_all_gold):
		return "s" # you're already falling, why fight it?
	
	if y % TILE_SIZE == 0 or not level.tiles[ty][tx].is_climbable():
		for i in xrange(len(dx)):
			if dd[i] != 'u':
				q.put((tx+dx[i],ty+dy[i],dd[i]))
	else:
		# ladder special case
		# enemy may not be able to move if it is on a ladder
		# and it is not snapped because there may be
		# solid blocks either side of it.
		for i in xrange(len(ladder_dx)):
			q.put((tx+ladder_dx[i],ty+ladder_dy[i],ladder_dd[i]))
	
	while not q.empty():
		cur = q.get()
		# bounds check
		if cur[0] < 0 or cur[0] >= level.width or\
				cur[1] < 0 or cur[1] >= level.height:
			continue
		# collision
		if level.tiles[cur[1]][cur[0]].is_solid():
			continue
		# seen
		if seen[cur[1]][cur[0]]:
			continue
		seen[cur[1]][cur[0]] = True

		# if one of the arguments are None, it means we
		# don't pay attention to that axis
		if (tx_goal is None or cur[0] == tx_goal) and\
				(ty_goal is None or cur[1] == ty_goal):
			return cur[2]

		for i in xrange(len(dx)):
			if dd[i] != 'u' or level.tiles[cur[1]][cur[0]].is_climbable():
				q.put((cur[0]+dx[i],cur[1]+dy[i],cur[2]))
			
	# if we can't get to him, just stand still
	return "s"
