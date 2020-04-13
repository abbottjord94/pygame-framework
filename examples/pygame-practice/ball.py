#Demo Ball Object
#This demonstrates how simple GameObjects work and how Game variables can be accessed by GameObjects
import pygame
from game_object import GameObject

class Ball(GameObject):

	#Start Function, runs once upon initialization of the object
	def start(self):

		#Setting the speed of the ball initially here
		self._speed = [5,5]

	#Update function, runs once every clock tick
	def update(self):
		#This moves the ball based on its speed
		self._bounds = self._bounds.move(self._speed)
		pygame.draw.rect(self._game.screen,(255,255,255),self._bounds,1)

		#This causes the ball to bounce once it hits the edges of the window
		if self._bounds.left < 0 or self._bounds.right > self._game._size[0]:
			self._speed[0] = -(self._speed[0])
		if self._bounds.top < 0 or self._bounds.bottom > self._game._size[1]:
			self._speed[1] = -(self._speed[1])

		#If a key is pressed, the ball will stop moving
		#Once it is released, the ball will start moving again
		if(self._game.findEvent(pygame.KEYDOWN)):
			self._speed=[0,0]
		if(self._game.findEvent(pygame.KEYUP)):
			self._speed=[5,5]
