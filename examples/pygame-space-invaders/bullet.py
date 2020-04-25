import pygame
from game_object import GameObject

class Bullet(GameObject):
	
	speed = [0,-5]
	timer = 0
	gameManager = None

	#Start Function, runs once upon initialization of the object
	def start(self):
		self.gameManager = self._game.getGameObjectByName("GameManager")

	#Update function, runs once every clock tick
	def update(self):
		if self.gameManager.playing:
			self.speed = [0,-5]
			self._bounds = self._bounds.move(self.speed)
			if(self.timer < 600):
				self.timer += 1
			else:
				self._game.remove(self)
		else:
			self.speed = [0,0]
