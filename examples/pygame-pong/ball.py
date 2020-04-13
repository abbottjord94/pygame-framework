import pygame
from game_object import GameObject

class Ball(GameObject):

	_speed = [5,5]

	def start(self):
		pass

	def update(self):
		self._bounds = self._bounds.move(self._speed)

	def collision(self,other_obj):
		pass
