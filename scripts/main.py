import pygame
import sys
from pygame.locals import *

pygame.init()

from data import data
from map import Map
from player import Player


class Main:
	def __init__(self):
		self.window = pygame.display.set_mode(data.winsiz)
		self.display = pygame.Surface(data.dissiz)

		self.clock = pygame.time.Clock()
		self.dt = 0
		self.ticks = 0
		self.time = 0

		self.camera = [0, 0]
		self.int_camera = self.camera.copy()


		self.map = Map(self)
		self.player = Player(self)

	def updates(self):
		self.dt = self.clock.tick(data.fpscap) * .001 * data.dt_fps
		self.ticks += 1
		self.time += 1 * self.dt

		self.camera[0] += (((self.player.rect.centerx - self.camera[0]) - (data.dissiz[0] / 2)) / 20) * self.dt
		self.camera[1] += (((self.player.rect.centery - self.camera[1]) - (data.dissiz[1] / 2)) / 20) * self.dt
		self.int_camera[0] = int(self.camera[0])
		self.int_camera[1] = int(self.camera[1])

		if self.time >= data.dt_fps:
			self.time = 0
			pygame.display.set_caption(str(self.ticks))
			self.ticks = 0
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if self.player.jump_cnt < 2:
						self.player.y_momentum = -4
						self.player.jump_cnt += 1

		self.player.update()

	def refresh(self):
		self.display.fill((135, 206, 245))
		self.map.render()

		self.player.render()

		self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))

		pygame.display.flip()

	def run(self):
		while 1:
			self.updates()

			self.refresh()

if __name__ == '__main__':
	main = Main()
	main.run()