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
	for key in map_data:
		pos = [int(i) for i in key.split()]
		map_image.blit(data.images['maps'][map_data[key][0]][int(map_data[key][1])], (pos[0] - map_corner[0], pos[1] - map_corner[1]))

	image_width = ceil(map_width / sects)
	map_images = []
	for i in range(sects):
		surf = pygame.Surface((image_width, map_height)).convert()
		surf.blit(map_image, (0, 0), (i * image_width, 0, image_width, map_height))
		surf.set_colorkey((0, 0, 0, 0))
		map_images.append(surf)

	return map_images, map_corner, image_width

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
		self.map_images, self.map_render_pos, self.map_slice_width = one_surf(self.map_data, 10)
		self.map_rects = get_map_rects(self.map_data)

	def render(self):
		for id, map_slice in enumerate(self.map_images):
			pos = [self.map_render_pos[0] + (id * self.map_slice_width), self.map_render_pos[1]]
			if abs(self.main.player.pos[0] - pos[0]) < data.render_dis:
				self.main.display.blit(map_slice, (pos[0] - self.main.int_camera[0], pos[1] - self.main.int_camera[1]))
		#self.main.display.blit(self.map_images[0], (self.map_render_pos[0] - self.main.int_camera[0], self.map_render_pos[1] - self.main.int_camera[1]))