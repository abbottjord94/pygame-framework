import pygame
from game_object import GameObject

class PlayerPaddle2(GameObject):

	def start(self):
		self._speed = [0,0]
	def update(self):
		self._bounds = self._bounds.move(self._speed)

		kd = None
		ku = None
		kd_event = self._game.findEvent(pygame.KEYDOWN)
		if not kd_event == None:
			kd = kd_event.__dict__.get('key')

		ku_event = self._game.findEvent(pygame.KEYUP)
		if not ku_event == None:
			ku = ku_event.__dict__.get('key')

		if kd == pygame.K_o:
			self._speed = [0,-5]
		if kd == pygame.K_l:
			self._speed = [0,5]

		if ku == pygame.K_o or ku == pygame.K_l:
			self._speed = [0,0]

		if(self._speed[1] == -5 and self._bounds.top < 0):
			self._speed = [0,0]
		if(self._speed[1] == 5 and self._bounds.bottom > self._game._size[1]):
			self._speed = [0,0]

	def collision(self,other_obj):
		pass
