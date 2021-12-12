import pygame 
import random
from game_object import GameObject

class Virus(GameObject):

	_speed = [0,0]
	_direction = 1

	def start(self):
		self.setName("Virus")

	def update(self):
		rand = random.randint(1,50)
		if rand == 42:
			if self._direction == 4:
				self._direction = 1
			else:
				self._direction = self._direction+1

		if self._direction == 1:
			self._speed = [5,0]
		if self._direction == 2:
			self._speed = [0,5]
		if self._direction == 3:
			self._speed = [-5,0]
		if self._direction == 4:
			self._speed = [0,-5]

		self._bounds = self._bounds.move(self._speed)

		if self._bounds.top < 0 or self._bounds.left < 0 or self._bounds.bottom > 600 or self._bounds.right > 800:
			self._game.remove(self)


	def collision(self, other_obj):
		if other_obj.getName() == "Wall":
			if other_obj._bounds.collidepoint(self._bounds.midtop):
				self._direction = 1
			if other_obj._bounds.collidepoint(self._bounds.midleft):
				self._direction = 2
			if other_obj._bounds.collidepoint(self._bounds.midright):
				self._direction = 3
			if other_obj._bounds.collidepoint(self._bounds.midbottom):
				self._direction = 4
