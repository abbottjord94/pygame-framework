import pygame
import os
from pygame import mixer
from game_object import GameObject


class SoundManager(GameObject):

	#Start Function, runs once upon initialization of the object
	def start(self):
		pass

	#Update function, runs once every clock tick
	def update(self):
		pass

	def play_sound(self,file):
		sound = mixer.Sound(os.path.join(os.path.dirname(__file__)+'/assets',file))
		sound.play()

	def play_music(self,file):
		mixer.music.load(os.path.join(os.path.dirname(__file__)+'/assets',file))
		mixer.music.play(-1)
