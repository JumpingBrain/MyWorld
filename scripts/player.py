import pygame

from data import data


class Player:
	def __init__(self, Main):
		self.main = Main

		self.rect = pygame.FRect(data.spawn[0], data.spawn[1], 7, 11)

		self.images = {}
		for key in data.images['player']:
			images = data.images['player'][key]
			self.images[f'{key} 1'] = [image for image in images] #right (1)
			self.images[f'{key} -1'] = [pygame.transform.flip(image, True, False) for image in images] #left (-1)

		self.dir = 1
		self.mov_dir = 0
		self.curr_image_frame = 0
		self.mov_speed = 1.5
		self.movement = 'idle'
		self.hitground = False

		self.y_momentum = 0
		self.falling_speed = .2
		self.jump_cnt = 0

		#stats
		#HEALTH
		self.health = 100
		self.health_bar_length = 75
		self.regen_speed = .2
		#SHIELD
		self.shield = 100
		self.shield_bar_length = 25
		#LEVELING
		self.level = 0
		self.xp = 5
		self.xp_bar_length = 14

	@property
	def pos(self):
		return [self.rect.centerx, self.rect.centery]
	

	def reset_ani(self, new_ani):
		if new_ani != self.movement:
			self.curr_image_frame = 0

	def xp_needed(self):
		if self.level < 10:
			return (self.level + 1) * 4
		elif self.level > 9 and self.level < 20:
			return (self.level + 1) * 2
		elif self.level > 19 and self.level < 30:
			return (self.level + 1) * 1.5
		else:
			return 1*(10**6)

	def render_stats(self):
		#HEALTH
		width = self.health_bar_length * (self.health / 100)
		x_pos = data.dissiz[0] - width
		padding = 2
		pygame.draw.rect(self.main.display, (196, 68, 74), (x_pos - padding, padding, width, 7))
		self.main.display.blit(data.images['ui']['healthbar_border'][0], (x_pos - padding - 1, padding - 1))

		#SHIEDL
		width = self.shield_bar_length * (self.shield / 100)
		x_pos = data.dissiz[0] - width
		padding = 9 + 3
		pygame.draw.rect(self.main.display, (97, 186, 255), (x_pos - 2, padding, width, 4))
		self.main.display.blit(data.images['ui']['shieldbar_border'][0], (x_pos - 2 - 1, padding - 1))

		#LEVEL
		self.main.display.blit(data.images['ui']['level_border'][0], (2, 2))
		font = data.fonts['mainfont' + '16']
		level_surf = font.render(str(int(self.level)), False, (255, 255, 235))
		if self.level > 10: self.main.display.blit(level_surf, (3, 3))
		else: self.main.display.blit(level_surf, (3 + 4, 3))
		#####################-XP
		xp_needed = self.xp_needed()
		width = self.xp_bar_length * (self.xp / xp_needed)
		x_pos = 4
		padding = 2
		pygame.draw.rect(self.main.display, (118, 255, 112), (x_pos, 22, width, 4))
		self.main.display.blit(data.images['ui']['xpbar_border'][0], (x_pos - 1, 22 - 1))
		########-resetting xp and leveling up is done here
		if self.xp >= xp_needed:
			self.level += 1 
			self.xp = 0

	def render(self):
		if self.curr_image_frame >= len(self.images[f'{self.movement} {self.dir}']):
			self.curr_image_frame = 0
			if self.hitground: self.hitground = False
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
			if not self.hitground:
				self.reset_ani('running')
			self.movement = 'running'
		else:
			if not self.hitground:
				self.reset_ani('idle')
			self.movement = 'idle'

		if self.jump_cnt > 0:
			self.movement = 'jumping'

		if self.hitground:
			self.movement = 'hitground'

		#print(self.hitground)


		#do animation counting
		if self.movement == 'running':
			self.curr_image_frame += data.running_ani_speed * self.main.dt
		elif self.movement == 'idle':
			self.curr_image_frame += data.idle_ani_speed * self.main.dt
		elif self.movement == 'hitground':
			#print(self.curr_image_frame)
			if self.mov_dir == 0: self.curr_image_frame += data.hitground_ani_speed * self.main.dt
			else: self.curr_image_frame += data.hitground_ani_speed * 2 * self.main.dt

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
				if self.y_momentum > 1:
					self.reset_ani('hitground')
					self.hitground = True
				self.rect.bottom = rect.top
				self.y_momentum = 0
				self.jump_cnt = 0
			elif self.y_momentum < 0:
				self.rect.top = rect.bottom
				self.y_momentum = 0