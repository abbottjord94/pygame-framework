import pygame
from math import sin, cos, radians
from game_object import GameObject

class Ball(GameObject):

	_speed = [0,0]
	_deg_counter = 0

	def update(self):
		self._bounds = self._bounds.move(self._speed)
		self._speed[0] = 3*cos(radians(self._deg_counter))
		self._speed[1] = 3*sin(radians(self._deg_counter))
		self._deg_counter += 1
