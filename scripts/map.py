import pygame
from data import data

from math import ceil


RECT_EXCLUSIONS = [
	'tree',
	'grass_end'
]

def one_surf(map_data, sects):
	map_width = max([[int(j) for j in i.split()][0] for i in map_data])
	map_height = max([[int(j) for j in i.split()][1] for i in map_data])
	map_corner = [min([[int(j) for j in i.split()][0] for i in map_data]), min([[int(j) for j in i.split()][1] for i in map_data])]
	map_image = pygame.Surface((map_width, map_height)).convert()
	map_image.set_colorkey((0, 0, 0, 0))
	sect_sizes = []
	for i in range(sects):
		sect_sizes.append(((12 + (map_width / sects)) - ((12 + (map_width / sects)) % 12)) - 12)
	x_sects = [[pygame.Surface((sect_sizes[i], map_height)).convert(), map_corner[0] + int((i * (map_width // sects)) - ((i * (map_width // sects)) % 12))] for i in range(sects)]
	for key in map_data:
		pos = [int(i) for i in key.split()]
		for id, d in enumerate(x_sects):
			surf = d[0]
			surf.set_colorkey((0, 0, 0, 0))
			x_pos = d[1]
			if pos[0] >= x_pos and pos[0] < x_pos + sect_sizes[id]:
				x_sects[id][0].blit(data.images['maps'][map_data[key][0]][int(map_data[key][1])], (pos[0] - x_pos, pos[1] - map_corner[1]))
				break
	return x_sects, map_corner

def get_map_rects(map_data):
	rects = []
	for key in map_data:
		do = True
		for exclusions in RECT_EXCLUSIONS:
			if exclusions in map_data[key][0]:
				do = False
		if do:
			image_key = map_data[key][0]
			image_id = map_data[key][1]
			image = data.images['maps'][image_key][image_id]
			pos = [int(i) for i in key.split()]
			if image_key == 'grass':
				if image_id != 4: #these images are rects that can never be touched by the player so no point processing them init. saves fps.
					rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
					rects.append([rect, image_key])
			else:
				rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
				rects.append([rect, image_key])

	return rects


class Map:
	def __init__(self, Main):
		self.main = Main

		#load map
		self.map_data = data.raw_map_data['fightingmap']
		self.map_images, self.map_render_pos = one_surf(self.map_data, 3)
		self.map_rects = get_map_rects(self.map_data)

	def render(self):
		for d in self.map_images:
			image = d[0]
			x_pos = d[1]
			self.main.display.blit(image, (x_pos - self.main.int_camera[0], self.map_render_pos[1] - self.main.int_camera[1]))
		#self.main.display.blit(self.map_images[0], (self.map_render_pos[0] - self.main.int_camera[0], self.map_render_pos[1] - self.main.int_camera[1]))