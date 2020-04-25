import pygame
from game_object import GameObject

class Boss(GameObject):

	speed = [2,0]
	gameManager = None
	soundManager = None
	health = 100
	inversion = 1

	#Start Function, runs once upon initialization of the object
	def start(self):
		self.soundManager = self._game.getGameObjectByName("SoundManager")
	#Update function, runs once every clock tick
	def update(self):
		self.gameManager = self._game.getGameObjectByName("GameManager")
		if not self.gameManager == None:
			if self.gameManager.playing:
				self.speed = [2*self.inversion,0]
				if self._bounds.left < 0:
					self.inversion = 1
					self.speed = [2,0]
					self._bounds.y += 50
				if self._bounds.right > self._game._size[0]:
					self.inversion = -1
					self.speed = [2*self.inversion,0]
					self._bounds.y += 50
			else:
				self.speed = [0,0]

		self._bounds = self._bounds.move(self.speed)

	def collision(self,other_obj):
		if other_obj.getName() == "Bullet":
			self.health -= 20
			if not self.gameManager == None:
				self.gameManager.score += 1
			#self.soundmanager.play_sound("explosion.wav")
			self._game.remove(other_obj)
			if(self.health <= 0):
				self._game.remove(self)

		if other_obj.getName() == "Player":
			if not self.gameManager == None:
				self.gameManager.gameOver = True
				self.gameManager.playing = False
