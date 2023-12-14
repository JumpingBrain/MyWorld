import pygame

from data import data


class Player:
	def __init__(self, Main):
		self.main = Main

		self.rect = pygame.FRect(data.spawn[0], data.spawn[1], 4, 8)

		self.images = {}
		for key in data.images['player']:
			images = data.images['player'][key]
			self.images[f'{key} 1'] = [image for image in images] #right (1)
			self.images[f'{key} -1'] = [pygame.transform.flip(image, True, False) for image in images] #left (-1)

		self.dir = 1
		self.mov_dir = 0
		self.curr_image_frame = 0
		self.mov_speed = 1
		self.movement = 'idle'

		self.y_momentum = 0
		self.falling_speed = .2
		self.jump_cnt = 0

	def reset_ani(self, new_ani):
		if new_ani != self.movement:
			self.curr_image_frame = 0

	def render(self):
		if self.curr_image_frame >= len(self.images[f'{self.movement} {self.dir}']):
			self.curr_image_frame = 0
		self.main.display.blit(self.images[f'{self.movement} {self.dir}'][int(self.curr_image_frame)], (self.rect.x - self.main.int_camera[0], self.rect.y - self.main.int_camera[1]))

	def collisions(self, rect_list):
		hits = []
		for d in rect_list:
			rect = d[0]
			if rect.colliderect(self.rect):
				hits.append(d)
		return hits

	def update(self):
		keys = pygame.key.get_pressed()

		self.mov_dir = keys[pygame.K_d] - keys[pygame.K_a]
		if self.mov_dir != 0:
			self.dir = self.mov_dir
			self.reset_ani('running')
			self.movement = 'running'
		else:
			self.reset_ani('idle')
			self.movement = 'idle'


		#do animation counting
		if self.movement == 'running':
			self.curr_image_frame += data.running_ani_speed * self.main.dt
		elif self.movement == 'idle':
			self.curr_image_frame += data.idle_ani_speed * self.main.dt

		map_rects = self.main.map.map_rects

		self.rect.x += self.mov_dir * self.mov_speed * self.main.dt
		hits = self.collisions(map_rects)
		for d in hits:
			rect = d[0]
			if self.mov_dir > 0:
				self.rect.right = rect.left
			elif self.mov_dir < 0:
				self.rect.left = rect.right

		self.y_momentum += self.falling_speed * self.main.dt
		if self.y_momentum >= 6:
			self.y_momentum = 6

		self.rect.y += self.y_momentum * self.main.dt
		hits = self.collisions(map_rects)
		for d in hits:
			rect = d[0]
			if self.y_momentum > 0:
				self.rect.bottom = rect.top
				self.y_momentum = 0
				self.jump_cnt = 0
			elif self.y_momentum < 0:
				self.rect.top = rect.bottom
				self.y_momentum = 0