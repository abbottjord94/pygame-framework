import time
import pygame
from game_object import GameObject
from player_paddle_1 import PlayerPaddle1
from player_paddle_2 import PlayerPaddle2
from ball import Ball
#GameObject definitions will need to be imported here

#GameManager class
#This is the first object instantiated in any Game, and can be used to spawn in other initial GameObjects, and perform an action
#once per clock tick if desired
class GameManager(GameObject):

	_player1 = None
	_player2 = None
	_ball = None

	_player1_score = 0
	_player2_score = 0

	_playing = False
	_font = None
	def start(self):
		#spawn initial GameObjects here like so:
		self._player1 = self._game.instantiate(PlayerPaddle1(self._game,"Player1","paddle.png",0,225))
		self._player2 = self._game.instantiate(PlayerPaddle2(self._game,"Player2","paddle.png",750,225))
		self._ball = self._game.instantiate(Ball(self._game,"Ball","ball.png",388,288))
		self.reset_game()
		pygame.font.init()
		self._font = pygame.font.SysFont('Comic Sans MS', 30)
	def update(self):
		#If you want the GameManager to do things on every frame, this is where you would put the code
		p1_score = self._font.render(str(self._player1_score),False,(255,255,255))
		p2_score = self._font.render(str(self._player2_score),False,(255,255,255))

		self._game.screen.blit(p1_score,(0,0))
		self._game.screen.blit(p2_score,(750,0))

		if self._playing:
			if self._ball._bounds.top < 0 or self._ball._bounds.bottom > self._game._size[1]:
				self._ball._speed[1] *= -1

			if self._ball._bounds.colliderect(self._player1._bounds) or self._ball._bounds.colliderect(self._player2._bounds):
				self._ball._speed[0] *= -1

			if self._ball._bounds.left < 0:
				self._ball._speed[0] *= -1
				self._player2_score += 1
				print(self._player1_score, self._player2_score)
				self.reset_game()

			if self._ball._bounds.right > self._game._size[0]:
				self._ball._speed[0] *= -1
				self._player1_score += 1
				print(self._player1_score, self._player2_score)
				self.reset_game()

	def reset_game(self):
		self._playing = False
		self._player1._bounds.topleft = (0,225)
		self._player2._bounds.topleft = (750,225)
		self._ball._bounds.topleft = (388,288)

		time.sleep(3)
		self._playing = True
