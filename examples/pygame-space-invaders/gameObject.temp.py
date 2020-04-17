import pygame
from game_object import GameObject

class NameThisObjectHere(GameObject):

	#Start Function, runs once upon initialization of the object
	def start(self):
		pass

	#Update function, runs once every clock tick
	def update(self):
		pass

	#Collision function, called when this object collides with another object	
	def collision(self,other_obj):
		pass
