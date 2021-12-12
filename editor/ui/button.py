import pygame

class Button():

	text = ""
	x = 0
	y = 0
	back_color = None
	text_color = None
	game = None
	button_rect = pygame.Rect(0,0,0,0)

	def __init__(self,game,x,y,text,back_color,text_color):
		self.game = game		
		self.x = x
		self.y = y
		self.text = text
		self.back_color = back_color
		self.text_color = text_color

		self.button_rect = pygame.Rect(int(self.x) - 40*(len(self.text)/2),int(self.y),240,36)
		self.start()

	#Credit to Robert Airth for parts of this function(github.com/rja45)

	def draw(self):
		font = pygame.font.Font(pygame.font.match_font('arial'), 32)
		text_surface = font.render(self.text, True, self.text_color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (int(self.x), int(self.y))
		pygame.draw.rect(self.game.screen, self.back_color, self.button_rect)
		self.game.screen.blit(text_surface, text_rect)

	def draw_invert(self):
		font = pygame.font.Font(pygame.font.match_font('arial'), 32)
		text_surface = font.render(self.text, True, self.back_color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (int(self.x), int(self.y))
		pygame.draw.rect(self.game.screen, self.text_color, self.button_rect)
		self.game.screen.blit(text_surface, text_rect)

	def start(self):
		pass

	def clicked(self):
		pass
