import os
import pygame

#GameObject class
#Basic structure for all objects in every game. Runs a start function upon initialization, and an update function every clock tick

class GameObject():

	_x=0
	_y=0
	_name=""
	_bounds=None
	_image=None
	_active=True
	_custom_properties={}

	#Initilization function, where the position is assigned, the image is loaded(or a default, invisible 1x1 pixel by default),
	#and can be moved to another location
	def __init__(self,game,name="GameObject",image="unknown.png",x=0,y=0, custom_properties={}):

		self._name = name
		self._x=x
		self._y=y
		self._game = game
		self._custom_properties = custom_properties

		#Tries to load the specified image here
		#TO DO: Do some error checking here to make sure that the try-catch block actually works if a non-default argument is given that cannot be found
		try:
			self._image=pygame.image.load(image)
			self._bounds=self._image.get_rect()
		except:
			self._image=pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "assets"),"unknown.png"))
			self._bounds=self._image.get_rect()

		self._bounds = self._bounds.move(x,y)

		#Call to start function
		self.start()

	#Returns the name of the GameObject
	def getName(self):
		return self._name

	#Returns the position of the GameObjects
	def getPos(self):
		return (self._x, self._y)

	#Template start function
	def start(self):
		pass

	#Template update function
	def update(self):
		pass

	#Template collision handling function
	def collision(self,other_obj):
		pass
		
	#Move function
	def move(self,x,y):
		self._x = x
		self._y = y
		self._bounds = self._bounds.move(x,y)

	#Set Active function
	def setActive(self, active):
		_active = active