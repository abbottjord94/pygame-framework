import pygame
from game_object import GameObject

class Enemy(GameObject):

	speed = [3,0]
	waveCount = 0
	gameManager = None
	soundManager = None

	#Start Function, runs once upon initialization of the object
	def start(self):
		self.soundManager = self._game.getGameObjectByName("SoundManager")
	#Update function, runs once every clock tick
	def update(self):
		self.gameManager = self._game.getGameObjectByName("GameManager")
		if not self.gameManager == None:
			self.waveCount = self.gameManager.waveCount
			if self.gameManager.playing:
				if self._bounds.left < 0:
					self.speed = [3 + self.waveCount,0]
					self._bounds.y += 50
				if self._bounds.right > self._game._size[0]:
					self.speed = [-3 - self.waveCount,0]
					self._bounds.y += 50
			else:
				self.speed = [0,0]

		self._bounds = self._bounds.move(self.speed)

	def collision(self,other_obj):
		if other_obj.getName() == "Bullet":
			if not self.gameManager == None:
				self.gameManager.score += 1
			#self.soundmanager.play_sound("explosion.wav")
			self._game.remove(other_obj)
			self._game.remove(self)

		if other_obj.getName() == "Player":
			if not self.gameManager == None:
				self.gameManager.playing = False
