import pygame
from game_object import GameObject

class Bullet(GameObject):
	
	speed = [0,-5]
	timer = 0

	#Start Function, runs once upon initialization of the object
	def start(self):
		pass

	#Update function, runs once every clock tick
	def update(self):
		self._bounds = self._bounds.move(self.speed)

		if(self.timer < 600):
			self.timer += 1
		else:
			self._game.remove(self)
