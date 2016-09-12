from itertools import product
from helpers import *
from random import randint
import math

class Tile:
	def __init__(self, x, y, seed):
		self.x = x
		self.y = y
		self.dampness = randint(50, 200)
#		self.dampness = 500
		self.fuel = randint(30, 50)
		self.seed = seed

		self.surrounding = [
			(self.x+1, self.y),
			(self.x-1, self.y),
			(self.x, self.y+1),
			(self.x, self.y-1)
		]


		self.alt = translate(2*noise2D(self.x, self.y, sharp=30, seed=self.seed), -2, 2, -100, 100)

		self.burning = False
		self.burntout = False

	def interact(self, tile):
		if tile.burning:
			power = 15+tile.alt-self.alt
			if self.dampness > 0:
				self.dampness -= power
			else:
				self.burning = True

	def next_frame(self):
		self.dampness = int(self.dampness)
		if self.burning and self.fuel:
			self.fuel -= 1
		elif not self.fuel:
			self.burning = False
			self.burntout = True

class Environment:
	def __init__(self, size):
		self.size = size
		self.tiles = {}
		self.seed = random_seed()
#		self.seed = "5f20dbec4e3ca3ff404712f841a15904"
		print self.seed

	def generate(self):
		for x,y in product(xrange(self.size[0]), xrange(self.size[1])):
			self.tiles[x, y] = Tile(x, y, self.seed)

		self.tiles[20, 20].burning = True

	def next_frame(self):
		self.changed = []
		for tile in self.tiles:
			tile_obj = self.tiles[tile]
			tile_obj.next_frame()
			try:
				if tile_obj.burning:
					x = tile[0]
					y = tile[1]

					for pos in tile_obj.surrounding:
						self.tiles[pos].interact(tile_obj)
			except KeyError: pass