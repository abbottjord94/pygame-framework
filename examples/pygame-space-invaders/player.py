import pygame
from game_object import GameObject
from bullet import Bullet

class Player(GameObject):

	speed = [0,0]
	soundManager = None
	canFire = True
	fireTimer = 0

	#Start Function, runs once upon initialization of the object
	def start(self):
		self.soundManager = self._game.getGameObjectByName("SoundManager")

	#Update function, runs once every clock tick
	def update(self):
		kd = self._game.findEvent(pygame.KEYDOWN)
		ku = self._game.findEvent(pygame.KEYUP)
		key = None
		if not self.canFire:
			if self.fireTimer < 60:
				self.fireTimer += 1
			else:
				self.canFire = True
				self.fireTimer = 0
		
		if not kd == None:
			key = kd.__dict__.get('key')
			if key == pygame.K_a:
				if self._bounds.left > 0:
					self.speed = [-5,0]
				else:
					self.speed = [0,0]
			if key == pygame.K_d:
				if self._bounds.right < self._game._size[0]:
					self.speed = [5,0]
				else:
					self.speed = [0,0]
				
			if key == pygame.K_SPACE:
				if self.canFire:
					self.canFire = False
					#self.soundManager.play_sound("laser.wav")
					self._game.instantiate(Bullet(self._game,"Bullet","bullet.png",self._bounds.x + 10,self._bounds.y - 20))

		if not ku == None:
			key = ku.__dict__.get('key')
			if key == pygame.K_a:
				self.speed = [0,0]
			if key == pygame.K_d:
				self.speed = [0,0]	

		self._bounds = self._bounds.move(self.speed)
