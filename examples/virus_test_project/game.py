import os
import sys
import json
import pygame
import threading
from game_object import GameObject
from scene_manager import SceneManager

#Game Class
#This will encapsulate all of the GameObjects and global game data, as well as game settings, and includes the generalized game loop
class Game():

	_settings = {}
	_gameObjects = []
	_size = (0,0)
	_io_queue = []
	_threads = []

	#Upon initialization, the Game will try to load a settings file
	def __init__(self):
		self.loadSettings()

	#Loading game settings like player speed, key mapping, screen size, etc
	def loadSettings(self,file="settings.json"):

		_file = os.path.join(os.path.dirname(__file__),file)
		with open(_file) as json_file:
			self._settings = json.load(json_file)
			json_file.close()

	#Adds a GameObject to the Game
	def instantiate(self,obj):
		self._gameObjects.insert(-len(self._gameObjects), obj)

	#Removes a GameObject from the Game
	def remove(self,obj):
		self._gameObjects.remove(obj)

	#Looks for a GameObject in the current game by it's name, returns None if it can't be found
	def getGameObjectByName(self,obj_name):
		for g in self._gameObjects:
			if(g.getName() == obj_name):
				return g
		return None

	#Handles incoming I/O events by placing them into a queue that GameObjects can access
	#Events are are removed from the queue once per clock tick
	def handleEvents(self,event):

		#Handling the QUIT event
		if(event.type == pygame.QUIT):
			sys.exit()

		#Handling the key up/down events
		if(event.type == pygame.KEYDOWN):
			self._io_queue.append(event)
		if(event.type == pygame.KEYUP):
			self._io_queue.append(event)

		#Handling mouse events
		if(event.type == pygame.MOUSEMOTION):
			self._io_queue.append(event)
		if(event.type == pygame.MOUSEBUTTONUP):
			self._io_queue.append(event)
		if(event.type == pygame.MOUSEBUTTONDOWN):
			self._io_queue.append(event)

	#Find an event in the queue by type, returns True if found, False if not found
	def findEvent(self, event_type):
		for event in self._io_queue:
			if(event.type == event_type): return event
		return None

	#Run the Game with the loaded settings
	#Some things here are for testing only
	def run(self):

		_gameSettings = self._settings.get("game")
		print(_gameSettings)
		self._size = (_gameSettings.get("window_x"), _gameSettings.get("window_y"))
		pygame.init()
		self.screen = pygame.display.set_mode(self._size)
		pygame.display.set_caption(_gameSettings.get("title"))

		self.instantiate(SceneManager(self))

		#Game Loop starts here
		#We'll try to generalize this to handle each GameObject individually
		#This way, we can use this as a framework for different kinds of games

		running = True
		if not _gameSettings.get("max_framerate"):
			framerate = 30
		else:
			framerate = _gameSettings.get("max_framerate")
		clock = pygame.time.Clock()
		while running:
			self.screen.fill((0,0,0))

			#Handle keyboard and mouse events here
			for event in pygame.event.get():
				self.handleEvents(event)

			#Run the update function on all GameObjects
			for g in self._gameObjects:
				if(g._active):
					self._threads.append(threading.Thread(target=g.update).run())
					if not g._image == None:
						self.screen.blit(g._image,g._bounds)
						
				for k in self._gameObjects:
					if not k==g and k._active and g._bounds.colliderect(k._bounds):
						g.collision(k)

			pygame.display.update()
			self._io_queue.clear()
			clock.tick(framerate)