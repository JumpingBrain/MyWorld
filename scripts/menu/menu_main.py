import pygame
import sys

from data import data
from menu.button import Button


class MenuMain:
	def __init__(self, Main):
		self.main = Main

		self.start_button = Button([50, 50], 'button_border1', 'START', (220, 220, 220), 16) # render_pos, border_name, text, text_colour, text_size

	def run(self):
		while 1:
			self.main.display.fill((0, 0, 0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.start_button.render(self.main.display)

			self.main.window.blit(
				pygame.transform.scale(self.main.display, data.winsiz), (0, 0)
				)

			pygame.display.flip()