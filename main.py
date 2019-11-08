

#!/usr/bin/python3.6

from random import randrange

import pygame

from constantes import *
from game import playGame


if __name__ == "__main__":
	pygame.display.init()
	pygame.font.init()

	# Set the screen
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), \
										flags=pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

	font = pygame.font.Font(pygame.font.get_default_font(), 100)
	color = pygame.Color(randrange(255), randrange(255), randrange(255))
	title = font.render("JURASSIC CACTI", True, color)
	instruction = font.render("Press SPACE", True, color)

	# Load background
	bg = pygame.image.load("Sprites/bg2.jpg")
	pos_bg = pygame.Rect(0, 0, bg.get_width(), bg.get_height())
	bg_part = pygame.Rect(0, bg.get_height()-WINDOW_HEIGHT, bg.get_width(), WINDOW_HEIGHT)


	continueProg = True
	continueGame = True

	main_surface = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.HWSURFACE | pygame.DOUBLEBUF)
	main_surface.blit(bg, pos_bg, area=bg_part)
	main_surface.blit(title, ((main_surface.get_width()-title.get_width())/2, TITLE_Y))
	main_surface.blit(instruction, ((main_surface.get_width()-instruction.get_width())/2, INSTRUCTION_Y))

	while continueProg:
		screen.blit(main_surface, (0,0))
		pygame.display.flip()

		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			continueProg = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			continueProg = playGame (screen)
		elif event.type == pygame.VIDEORESIZE:
			main_surface = pygame.transform.smoothscale(main_surface, (event.w, event.h))




	pygame.font.quit()
	pygame.display.quit()
