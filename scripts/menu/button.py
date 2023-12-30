import pygame

from data import data

pygame.font.init()


class Button:
	def __init__(self, render_pos, border_name, text, text_colour, text_size):
		self.pos = render_pos
		self.text_size = text_size
		self.border_img = pygame.transform.scale(data.images['menu'][border_name][0], (self.text_size * (len(text) - 1), self.text_size + 6))

		font = pygame.font.Font(data.fontdir + 'mainfont.otf', self.text_size)
		self.button_text = font.render(text, False, text_colour)

	def render(self, surf):
		surf.blit(self.border_img, (self.pos[0] - 8, self.pos[1] - 3))
		surf.blit(self.button_text, (self.pos[0], self.pos[1]))