from random import randrange

import pygame

from constantes import *
from game import playGame


if __name__ == "__main__":
	pygame.display.init()
	pygame.font.init()

	# Set the screen
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.HWSURFACE | pygame.DOUBLEBUF)

	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	title = font.render("JURASSIC CACTI", 0, (80, 50, 180))

	# Load background
	bg = pygame.image.load("Sprites/bg2.jpg")
	pos_bg = pygame.Rect(0, 0, bg.get_width(), bg.get_height())
	bg_part = pygame.Rect(0, bg.get_height()-WINDOW_HEIGHT, bg.get_width(), WINDOW_HEIGHT)


	continueProg = True
	continueGame = True

	while continueProg:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			continueProg = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			continueProg = playGame (screen) 

		screen.blit(bg, pos_bg, area=bg_part)
		screen.blit(title, ((screen.get_width()-title.get_width())/2, (screen.get_height()-title.get_height())/2))
		pygame.display.flip()


	pygame.font.quit()
	pygame.display.quit()