import pygame
import sys
from game_object import GameObject

class Player(GameObject):

	_speed = [0,0]
	_collidingleft = False
	_collidingright = False
	_collidingtop = False
	_collidingbottom = False
	_score = 0

	def start(self):
		pass

	def update(self):
		kd = self._game.findEvent(pygame.KEYDOWN)
		key = None
		if not kd == None:
			key = kd.__dict__.get('key')
			if key == pygame.K_w and not self._collidingtop:
				self._speed = [0,-5]
			if key == pygame.K_s and not self._collidingbottom:
				self._speed = [0,5]
			if key == pygame.K_a and not self._collidingleft:
				self._speed = [-5,0]
			if key == pygame.K_d and not self._collidingright:
				self._speed = [5,0]

		self._bounds = self._bounds.move(self._speed)
		self._collidingleft = False
		self._collidingright = False
		self._collidingtop = False
		self._collidingbottom = False

	def collision(self, other_obj):
		if other_obj.getName() == "Wall":
			if self._bounds.collidepoint(other_obj._bounds.midleft):
				if not self._collidingright:
					self._speed[0] = 0
					self._collidingright = True
			if self._bounds.collidepoint(other_obj._bounds.midright):
				if not self._collidingleft:
					self._speed[0] = 0
					self._collidingleft = True
			if self._bounds.collidepoint(other_obj._bounds.midtop):
				if not self._collidingbottom:
					self._speed[1] = 0
					self._collidingbottom = True
			if self._bounds.collidepoint(other_obj._bounds.midbottom):
				if not self._collidingtop:
					self._speed[1] = 0
					self._collidingtop = True

		if other_obj.getName() == "ToiletPaper":
			self._score = self._score + 1
			print(self._score)
			self._game.remove(other_obj)

		if other_obj.getName() == "Virus":
			sys.exit()
			#handle viruses
