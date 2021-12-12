import os
import json
import pygame
from game_object import GameObject

#import other game objects classes here (EDITABLE SECTION)

#Scene Manager class

class SceneManager(GameObject):

	_current_scene = ""
	_background_image = None
	_background_bounds = None
	_game = None
	
	#Game Object types (EDITABLE SECTION)
	
	_object_types = {
		
	}
	
	#Constructor
	def __init__(self, game):
		self._game = game
	
	#Load Scene function
	def load_scene(self, scene = "none.json"):
		try:
			_file = os.path.join(os.path.dirname(__file__), scene)
			
			with open(_file) as scene_file:
				_scene_obj = json.load(_file)
				scene_file.close()
			
			#Remove the previous scene's objects
			for o in self._game._gameObjects:
				self._game.remove(o)
			
			#Get the scene name
			self._current_scene = _scene_obj["scene_name"]
			
			#Load the background image
			self._background_image = pygame.image.load(_scene_obj["background"])
			self._background_bounds = self._background_image.get_rect()
			self._background_bounds = self._background_bounds.move(0,0)
			
			#Spawn in the objects from the scene file
			for obj in scene_obj["objects"]:
				self._game.instantiate(_self._object_types[obj["type"]] (self._game, obj["obj_name"], obj["image"], obj["x"], obj["y"], obj["custom_properties"]))
				
		except:
			#Some kind of error handling should go here for when the scene can't load
			pass
	
	#Returns the current scene name
	def get_current_scene(self):
		return _current_scene
		
	#Use this to load the first scene
	def start(self):
		self.load_scene("scene_name.json")
		
	#Use this if you want the SceneManager to perform an action on every clock tick
	def update(self):
		pass