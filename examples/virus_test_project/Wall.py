import pygame
from game_object import GameObject

class Wall(GameObject):

	#Start Function, runs once upon initialization of the object
	def start(self):
		self.setName("Wall")

	#Update function, runs once every clock tick
	def update(self):
		pass