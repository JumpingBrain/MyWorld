import socket
import pygame
import sys
from pygame.locals import *
from _thread import *
import threading

pygame.init()
pygame.font.init()

pygame.display.set_caption('Chat')

class Win:
	def __init__(self):
		self.window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
		self.clock = pygame.time.Clock()

		self.message = [""]
		self.font_size = 32
		self.render_pos = [3, self.window.get_height() - 3]
		self.font = pygame.font.SysFont('Futura', self.font_size)

		self.conversation = []
		self.ran = 0
		self.t1 = threading.Thread(target=self.get_messages)

	def render_text(self, text, pos, colour):
		surf = self.font.render(text, True, colour)
		self.window.blit(surf, pos)

	def get_messages(self):
		while 1:
			try:
				rev_message = n.recieve()

				if rev_message != "":
					formatted_message = [rev_message]
					while 1:
						width = self.font.size(formatted_message[-1])[0]
						diff = width / self.window.get_width()
						if diff < 1:
							break
						else:
							buf = formatted_message[-1]
							formatted_message[-1] = formatted_message[-1][:int(len(formatted_message[-1])/2)]
							formatted_message.append(buf[int(len(formatted_message[-1])/2):])
					self.conversation.extend(formatted_message)
			except:
				pass

	def run(self):
		while 1:
			self.render_pos[1] = self.window.get_height() - 3
			self.window.fill((0, 0, 0))

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == TEXTINPUT:
					self.message[-1] += event.text
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						self.message[-1] = self.message[-1][:-1] 
						if len(self.message[-1]) == 0:
							if len(self.message) > 1:
								self.message = self.message[:-1]
					if self.font.size(self.message[-1])[0] >= self.window.get_width() - self.font_size:
						if len(self.message) < 50:
							self.message.append("")
					if event.key == K_RETURN:
						n.send(''.join(self.message))
						self.conversation.extend(self.message)
						self.message = [""]

			for id, message in enumerate(self.conversation):
				if id % 2 == 0:
					colour = (0, 255, 0)
				else:
					colour = (200, 200, 200)
				self.render_text(f'-{message}', [3, (self.window.get_height()/2) - ((len(self.conversation) - id) * self.font_size)], colour)
			if len(self.conversation) > 10:
				del self.conversation[0]

			box_height = len(self.message) * self.font_size + 6
			pygame.draw.rect(self.window, (0, 0, 128), (0, self.window.get_height() - box_height + 3, self.window.get_width(), box_height))	
			
			for id, text in enumerate(self.message):
				self.render_text(text, [self.render_pos[0], self.render_pos[1] - ((len(self.message) - id) * self.font_size)], (220, 220, 220))

			pygame.display.flip()


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "192.168.1.144"
		self.port = 5555
		self.addr = (self.server, self.port)
		self.pos = self.connect()
		print(self.pos)

	def get_pos(self):
		return self.pos

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			pass

	def send(self, data):
		try:
			self.client.send(str.encode(data))
		except socket.error as e:
			print(e, 'goo goo gah gah')

	def recieve(self):
		try:
			return self.client.recv(2048).decode()
		except:
			pass

n = Network()
win = Win()
win.conversation.append(n.pos)

while 1:
	try:
		print(self.client.recv(2048).decode() + '<<<<<<<<<')
	except:
		pass

	start_new_thread(win.get_messages, ())
	win.run()
	#user_message = str(input(': '))
	#print('Recieved: ', n.send(user_message))