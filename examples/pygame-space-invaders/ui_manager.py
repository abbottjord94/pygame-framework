import pygame
from game_object import GameObject
from button import Button
from resume_button import ResumeButton
from quit_button import QuitButton

class UIManager(GameObject):

	drawMenu = False
	buttons = []
	lastmousePos = (0,0)
	
	#Start Function, runs once upon initialization of the object
	def start(self):
		self.buttons.append(ResumeButton(self._game,self._game._size[0]/2,200,"Resume",(0,0,0),(255,255,255)))
		self.buttons.append(QuitButton(self._game,self._game._size[0]/2,250,"Quit  ",(0,0,0),(255,255,255)))

		for button in self.buttons:
			button.start()

	#Update function, runs once every clock tick
	def update(self):
		if(self.drawMenu):

			mouseMoveEvent = self._game.findEvent(pygame.MOUSEMOTION)
			mouseDownEvent = self._game.findEvent(pygame.MOUSEBUTTONDOWN)
			for button in self.buttons:
				if not mouseMoveEvent == None:
					self.lastmousePos = mouseMoveEvent.__dict__.get('pos')
					
				elif not mouseDownEvent == None:
					self.lastmousePos = mouseDownEvent.__dict__.get('pos')
					if button.button_rect.collidepoint(self.lastmousePos):
						button.clicked()

				if button.button_rect.collidepoint(self.lastmousePos):
					button.draw_invert()
				else:
					button.draw()


