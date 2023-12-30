import pygame
import os
from random import choice

from data import data

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.mixer.set_num_channels(64)


class SoundClass:
	def __init__(self, sounds, vol):
		self.sounds = sounds
		[i.set_volume(vol) for i in self.sounds]
		self.sound_timer = 0
		self.sound_length = 0
		self.tmp_vol = 0
		self.playing = False
		self.curr_sound = None

	def fadeout(self):
		try: self.curr_sound.fadeout(1000)
		except Exception as e: print(e)
		self.reset()

	def play(self, dt, curr_fps, play_back_speed):
		dt_fps = data.dt_fps
		if self.sound_timer < .001:
			self.curr_sound = choice(self.sounds)
			self.curr_sound.play()
			self.sound_length = self.curr_sound.get_length()
			self.playing = True

		self.sound_timer += dt

		if dt_fps <= 0:
			dt_fps += .1
		if self.sound_timer >= (dt_fps * ((dt_fps / curr_fps) / play_back_speed) * self.sound_length): #((dt_fps / curr_fps) / 2) this is so that at 30fps is plays at the same speed as 180fps or whatever
			self.sound_timer = 0
			self.sound_length = 0

	def reset(self):
		self.sound_timer = 0
		self.sound_length = 0
		self.playing = False
		self.curr_sound = None

class SFX:
	def __init__(self):
		self.sounds = {}

		for foldername in os.listdir(data.sounddir + 'sfx/'):
			sounds = []
			for filename in os.listdir(data.sounddir + 'sfx/' + foldername + '/'):
				sounds.append(
					pygame.mixer.Sound(data.sounddir + 'sfx/' + foldername + '/' + filename)
					)
			vol = .25
			self.sounds[foldername] = SoundClass(sounds, vol)

sfx = SFX()