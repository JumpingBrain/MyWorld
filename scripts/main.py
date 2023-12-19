import pygame
import sys
from pygame.locals import *
from math import floor

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

		pygame.mouse.set_visible(False)

	@property
	def mpos(self):
		return pygame.mouse.get_pos()

	def updates(self):
		self.dt = self.clock.tick(data.fpscap) * .001 * data.dt_fps
		self.ticks += 1
		self.time += 1 * self.dt

		self.camera[0] += (((self.player.rect.centerx - self.camera[0]) - (data.dissiz[0] / 2)) / 20) * self.dt
		self.camera[1] += (((self.player.rect.centery - self.camera[1]) - (data.dissiz[1] / 2)) / 20) * self.dt
		self.int_camera[0] = floor(self.camera[0])
		self.int_camera[1] = floor(self.camera[1])

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
						self.player.movement = 'jumping'

		self.player.update()

	def refresh(self):
		self.display.fill((135, 206, 245))
		self.map.render()

		self.player.render()
		self.player.render_stats()

		#render mouse cursor
		mouse_change = pygame.mouse.get_rel() #so the cursor sticks to the mouse
		self.display.blit(data.images['ui']['cursor'][0], ((self.mpos[0] / data.ratio) + (mouse_change[0] / 10), (self.mpos[1] / data.ratio) + (mouse_change[1] / 10)))

		self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))

		pygame.display.flip()

	def run(self):
		while 1:
			self.updates()

			self.refresh()

if __name__ == '__main__':
	main = Main()
	main.run()