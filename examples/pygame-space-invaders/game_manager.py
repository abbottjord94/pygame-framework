import pygame
from game_object import GameObject
from background import Background
from sound_manager import SoundManager
from ui_manager import UIManager
from player import Player
from enemy import Enemy
from boss import Boss
#GameObject definitions will need to be imported here

#GameManager class
#This is the first object instantiated in any Game, and can be used to spawn in other initial GameObjects, and perform an action
#once per clock tick if desired
class GameManager(GameObject):

	soundManager = None
	uiManager = None
	player = None
	waveCount = 0
	score = 0
	playing = True
	gameOver = False

	def start(self):
		#spawn initial GameObjects here like so:
		self._game.instantiate(Background(self._game,"Background","background.png",0,0))
		self._game.instantiate(SoundManager(self._game,"SoundManager","unknown.png",-1,-1))
		self._game.instantiate(UIManager(self._game,"UIManager","unknown.png",-1,-1))
		self.soundManager = self._game.getGameObjectByName("SoundManager")
		self.uiManager = self._game.getGameObjectByName("UIManager")
		
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
		kd = self._game.findEvent(pygame.KEYDOWN)
		if not kd == None:
			key = kd.__dict__.get('key')
			if key == pygame.K_ESCAPE:
				if self.playing:
					self.uiManager.drawMenu = True
					self.playing = False
				else:
					self.uiManager.drawMenu = False
					self.playing = True

		if self.playing:
			scoreRender = self.scoreFont.render("Score: " + str(self.score), True, (255,255,255))
			waveRender = self.scoreFont.render("Wave: " + str(self.waveCount+1), True, (255,255,255))
			self._game.screen.blit(scoreRender,(0,0))
			self._game.screen.blit(waveRender,(0,16))

			if self._game.getGameObjectByName("Enemy") == None and self._game.getGameObjectByName("Boss") == None:
				self.waveCount += 1
				if((self.waveCount + 1) %  2 == 0):
					self._game.instantiate(Boss(self._game,"Boss","boss.png",self._game._size[0]/2, 0))
				else:
					for i in range(0,9):
						self._game.instantiate(Enemy(self._game,"Enemy","enemy.png",80*i,50))

		else:
			if self.gameOver:
				gameOverRender = self.gameOverFont.render("Game Over", True, (255,255,255))
				self._game.screen.blit(gameOverRender,((self._game._size[0]/2)-144,40))
