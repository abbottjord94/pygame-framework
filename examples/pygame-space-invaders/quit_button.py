import pygame
import sys
from button import Button

class QuitButton(Button):

	def clicked(self):
		pygame.quit()
		sys.exit()

