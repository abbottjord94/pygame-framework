import os
import json
import pygame
import sys
from game_object import GameObject

#import other game objects classes here (EDITABLE SECTION)
($IMPORT_LIST)


#Scene Manager class

class SceneManager(GameObject):

	_current_scene = ""
	_background_image = None
	_background_bounds = None
	_game = None
	
	#Game Object types (EDITABLE SECTION)
	
	($OBJECT_TYPE_DICT)
	#_object_types = {}
	
	#Constructor
	def __init__(self, game):
		self._game = game
		self.start()
	
	#Load Scene function
	def load_scene(self, scene = "none.json"):
		try:
			_file = os.path.join(os.path.join(os.path.dirname(__file__), "scenes"), scene)
			
			scene_file = open(_file, "r")
			_scene_obj = json.loads(scene_file.read())
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
			
			self._image = self._background_image
			self._bounds = self._background_bounds
						
			#Spawn in the objects from the scene file
			for obj in _scene_obj["objects"]:
				new_obj = self._object_types[obj["type"]] (self._game, obj["obj_name"], obj["image"], obj["x"], obj["y"], obj["custom_properties"])
				self._game.instantiate(new_obj)
				
		except:
			#Some kind of error handling should go here for when the scene can't load
			print(sys.exc_info())
	
	#Returns the current scene name
	def get_current_scene(self):
		return _current_scene
		
	#Use this to load the first scene
	def start(self):
		self.load_scene(($FIRST_SCENE_NAME))
		
	#Use this if you want the SceneManager to perform an action on every clock tick
	def update(self):
		pass