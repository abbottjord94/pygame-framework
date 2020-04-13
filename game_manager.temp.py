import pygame
from game_object import GameObject

#GameObject definitions will need to be imported here

#GameManager class
#This is the first object instantiated in any Game, and can be used to spawn in other initial GameObjects, and perform an action
#once per clock tick if desired
class GameManager(GameObject):

	def start(self):
		#spawn initial GameObjects here like so:
		pass

	def update(self):
		#If you want the GameManager to do things on every frame, this is where you would put the code
		pass
