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
			random_number = randrange(3)
			self.n_ennemies += 1
			if random_number == 0:
				return Cactus()
			elif random_number == 1:
				return Bird()
			else:
				return Trex()
		else:
			return None

	def increase_frequency(self):
		self.lap -= 10





def playGame (screen):

	first_cactus = False

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



	# GAME LOOP
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
			elif event.key == pygame.K_LEFT:
				diplo.attack()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				diplo.stand_up()

		timer.tick(60)

		# Call the ennemy generator
		ennemy = ennemy_gen.new()
		if ennemy != None:
			if type(ennemy) == Cactus and first_cactus == False:
				msg = ["You meet a cactus!", "Press UP arrow to jump over it"]
				#print_msg(screen, msg)
				first_cactus = True
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

		# print score
		txt_score = font.render("SCORE : "+str(score), True, (0, 0, 0))
		screen.blit(txt_score, (20, 20))

		# Blit the ennemies
		for e in ennemies:
			e.move()
			screen.blit(e.sprite, e.pos)

		# Check for collisions
		col = False
		for e in ennemies:
			if type(e) == Bird:
				col = physics.gotCollision (diplo.hitbox_neck, e.hitbox)
			elif type(e) == Cactus:
				col = physics.gotCollision (diplo.hitbox, e.hitbox)
			elif type(e) == Trex:
				col = physics.gotCollision(diplo.hitbox, e.hitbox)
				if col and diplo.state == ATTACKING:
					e.getHurt()
					col = False
			if col:
				msg = ["GAME OVER"]
				continueProg = print_msg(screen, msg)
				if not continueProg:
					return False
				continueGame = False
				break

		# Eliminate dead ennemies
		i = 0
		while i < len(ennemies):
			if not ennemies[i].is_alive():
				del ennemies[i]
				score += 10
			else:
				i += 1

		# increases the difficulty
		if ennemy_gen.n_ennemies >= 10:
			ennemy_gen.n_ennemies = 0
			ennemy_gen.increase_frequency()

		pygame.display.flip()

	return True




def print_msg (screen, msg):

	quitMsg = False

	font = pygame.font.Font(pygame.font.get_default_font(), 60)
	
	for i, m in enumerate(msg):
		txt = font.render(m, True, (0, 0, 0))
		txt_pos = ((screen.get_width()-txt.get_width())/2, (screen.get_height()-txt.get_height())/2+i*txt.get_height())
		screen.blit(txt, txt_pos)

	pygame.display.flip()

	while not quitMsg:
		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			return False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			quitMsg = True

	return True
