from lib.helpers import *
from lib.environment import *
import pygame, time
pygame.M_1 = 323
pygame.M_2 = 324
pygame.M_3 = 325

class Game:
	def __init__(self):
		pygame.init()

		self.title = "Template Game"
		self.rate = 60
		self.size = [500, 500]
		self.background = (0, 0, 0)

		self.tickspeed = 1

		self.tilesize = 5
		self.env = Environment([self.size[0]/self.tilesize, self.size[1]/self.tilesize])
		self.env.generate()

		self.running = False
		self.frame = 0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)
		self.font = pygame.font.Font('freesansbold.ttf', 12)

		pygame.display.set_caption(self.title)

	def movement(self):
		keys = control_check()
		mouse = pygame.mouse.get_pos()

		self.mousex = mouse[0]/self.tilesize
		self.mousey = mouse[1]/self.tilesize


		if keys[pygame.M_1]:
			self.env.tiles[self.mousex, self.mousey].fuel = 0
		if keys[pygame.M_3]:
			self.env.tiles[self.mousex, self.mousey].burning = True	

	def draw_tile(self, tile):
		x = tile.x * self.tilesize
		y = tile.y * self.tilesize

		if tile.burning:
			color = (255, 0, 0)
		elif tile.burntout:
			color = (25, 25, 25)
		else:
			alt = translate(tile.alt, -100, 100, 0, 255)
			fuel = translate(tile.fuel, 30, 50, 0, 10)
			color = (0, alt+fuel, 0)

		pygame.draw.rect(self.screen, color, [x, y, self.tilesize, self.tilesize])

	def draw(self):
		self.screen.fill(self.background)

		for tile in self.env.tiles:
			self.draw_tile(self.env.tiles[tile])

		text = self.font.render("%iFPS" % (self.fps), True, (255, 255, 255))
		self.screen.blit(text, (10, 10))

		curtil = self.env.tiles[self.mousex, self.mousey]
		d = curtil.__dict__
		text = self.font.render(str(d), True, (255, 255, 255))
		self.screen.blit(text, (10, self.size[1]-20))

	def start(self):
		self.running = True
		self.fps = 0
		fps_time_counter = time.time()
		fps_counter = 0

		while self.running:
			fps_counter += 1
			if time.time()-fps_time_counter >= 0.5:
				fps_time_counter = time.time()
				self.fps = fps_counter*2
				fps_counter = 0

			self.frame += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.movement()
			self.draw()

			if not self.frame%self.tickspeed:
				self.env.next_frame()

			pygame.display.update()
			self.clock.tick(self.rate)

game = Game()
game.start()