from random import randrange

import pygame

from constantes import *
from game_elements import *
import physics



class Ennemy_gen:
	def __init__(self, lap):
		self.lap = lap
		self.frame_counter = 0
		self.n_ennemies = 0

	def new(self):
		self.frame_counter += 1
		if self.frame_counter >= self.lap:
			self.frame_counter = 0
			random_number = randrange(2)
			if random_number == 0:
				self.n_ennemies += 1
				return Cactus()
			else:
				self.n_ennemies += 1
				return Bird()
		else:
			return None

	def increase_frequency(self):
		self.lap -= 10





def playGame (screen):

	# Score
	score = 0

	# Font
	font = pygame.font.Font(pygame.font.get_default_font(), 80)


	# Create the animated object
	diplo = Dino()
	ennemies = list()
	ennemy_gen = Ennemy_gen(100)

	# Load background
	bg = pygame.image.load("Sprites/bg2.jpg")
	pos_bg = pygame.Rect(0, 0, bg.get_width(), bg.get_height())
	bg_part = pygame.Rect(0, bg.get_height()-WINDOW_HEIGHT, bg.get_width(), WINDOW_HEIGHT)

	# Set a timer
	timer = pygame.time.Clock()

	# Game loop
	continueGame = True
	while continueGame:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			return False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if diplo.state == WALKING:
					diplo.state = JUMPING
			elif event.key == pygame.K_DOWN:
				diplo.bend()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				diplo.stand_up()

		timer.tick(60)

		# Call the ennemy generator
		ennemy = ennemy_gen.new()
		if ennemy != None:
			ennemies.append(ennemy)

		# Refresh the screen

		# Scrolling of the background
		pos_bg.left -= 1
		if pos_bg.left < -bg.get_width():
			pos_bg.left = 0
		screen.blit(bg, pos_bg, area=bg_part)
		pos_bg.left += bg.get_width()
		screen.blit(bg, pos_bg, area=bg_part)
		pos_bg.left -= bg.get_width()

		# Move the animated object
		diplo.next_move()
		screen.blit(diplo.sprite, diplo.pos)

		for e in ennemies:
			e.move()
			screen.blit(e.sprite, e.pos)

		# Eliminate dead ennemies
		i = 0
		while i < len(ennemies):
			if not ennemies[i].is_alive():
				del ennemies[i]
				score += 10
			else:
				i += 1

		# print score
		txt_score = font.render("SCORE : "+str(score), True, (0, 0, 0))
		screen.blit(txt_score, (20, 20))

		# Check for collisions
		col = False
		for e in ennemies:
			if type(e) == Bird:
				col = physics.gotCollision (diplo.hitbox_neck, e.hitbox)
			elif type(e) == Cactus:
				col = physics.gotCollision (diplo.hitbox, e.hitbox)
			if col:
				continueProg = game_over(screen)
				if not continueProg:
					return False
				continueGame = False
				break

		# increases the difficulty
		if ennemy_gen.n_ennemies >= 10:
			ennemy_gen.n_ennemies = 0
			ennemy_gen.increase_frequency()

		pygame.display.flip()

	return True





def game_over (screen):

	font = pygame.font.Font(pygame.font.get_default_font(), 175)
	game_over = font.render("GAME OVER", True, (0, 0, 0))

	continueGameOver = True

	screen.blit(game_over, ((screen.get_width()-game_over.get_width())/2, (screen.get_height()-game_over.get_height())/2))
	pygame.display.flip()

	while continueGameOver:
		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			return False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			continueGameOver = False

	return True

