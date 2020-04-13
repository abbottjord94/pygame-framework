import time
import pygame
import sys
from game_object import GameObject
from wall import Wall
from toiletpaper import ToiletPaper
from virus import Virus
from player import Player
#GameObject definitions will need to be imported here

#GameManager class
#This is the first object instantiated in any Game, and can be used to spawn in other initial GameObjects, and perform an action
#once per clock tick if desired
class GameManager(GameObject):


	_map = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
		[1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
		[1,0,0,1,0,0,1,1,1,1,1,1,0,1,0,1],
		[1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
		[1,0,0,1,0,0,1,1,1,1,1,0,0,1,0,1],
		[1,0,0,1,0,0,1,3,3,3,1,0,0,1,0,1],
		[1,0,0,1,0,0,1,5,5,5,1,0,0,1,0,1],
		[1,0,0,1,0,0,1,5,5,5,1,0,0,1,0,1],
		[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
		[1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
		[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
		[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

	def start(self):
		#spawn initial GameObjects here like so:
		print(self._map)
		for i in range(0,len(self._map)):
			for j in range(0,len(self._map[i])):
				if self._map[i][j] == 1:
					self._game.instantiate(Wall(self._game,"Wall","wall.png",j*50, i*50))
				if self._map[i][j] == 0:
					self._game.instantiate(ToiletPaper(self._game,"ToiletPaper","toiletpaper.png",j*50,i*50))
				if self._map[i][j] == 3:
					self._game.instantiate(Virus(self._game,"Virus", "virus.png",j*50,i*50))
				if self._map[i][j] == 4:
					self._game.instantiate(Player(self._game,"Player","player.png",j*50,i*50))
	def update(self):
		#If you want the GameManager to do things on every frame, this is where you would put the code
		_virus = self._game.getGameObjectByName("Virus")
		_tp = self._game.getGameObjectByName("ToiletPaper")
		if _virus == None and _tp == None:
			sys.exit()
