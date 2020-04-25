import pygame
from button import Button

class ResumeButton(Button):

	def start(self):
		pass

	def clicked(self):
		self.game.getGameObjectByName("UIManager").drawMenu = False
		self.game.getGameObjectByName("GameManager").playing = True
		

