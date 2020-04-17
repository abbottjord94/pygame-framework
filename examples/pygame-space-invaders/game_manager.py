import pygame
from game_object import GameObject
from background import Background
from sound_manager import SoundManager
from player import Player
from enemy import Enemy
#GameObject definitions will need to be imported here

#GameManager class
#This is the first object instantiated in any Game, and can be used to spawn in other initial GameObjects, and perform an action
#once per clock tick if desired
class GameManager(GameObject):

	soundManager = None
	player = None
	waveCount = 0
	score = 0
	playing = True

	def start(self):
		#spawn initial GameObjects here like so:
		self._game.instantiate(Background(self._game,"Background","background.png",0,0))
		self._game.instantiate(SoundManager(self._game,"SoundManager","unknown.png",-1,-1))
		self.soundManager = self._game.getGameObjectByName("SoundManager")
		
		#Music is here but I've disabled it for now		
		#self.soundManager.play_music("background.wav")

		self._game.instantiate(Player(self._game,"Player","player.png",100,500))
		self.player = self._game.getGameObjectByName("Player")

		for i in range(0,9):
			self._game.instantiate(Enemy(self._game,"Enemy","enemy.png",80*i,50))

		self.scoreFont = pygame.font.Font('freesansbold.ttf',16)
		self.gameOverFont = pygame.font.Font('freesansbold.ttf',64)
	def update(self):
		#If you want the GameManager to do things on every frame, this is where you would put the code
		if self.playing:
			scoreRender = self.scoreFont.render("Score: " + str(self.score), True, (255,255,255))
			waveRender = self.scoreFont.render("Wave: " + str(self.waveCount+1), True, (255,255,255))
			self._game.screen.blit(scoreRender,(0,0))
			self._game.screen.blit(waveRender,(0,16))

			if self._game.getGameObjectByName("Enemy") == None:
				self.waveCount += 1
				for i in range(0,9):
					self._game.instantiate(Enemy(self._game,"Enemy","enemy.png",80*i,50))

		else:
			gameOverRender = self.gameOverFont.render("Game Over", True, (255,255,255))
			self._game.screen.blit(gameOverRender,(320,378))
