import pygame

from constantes import *
import Dino
import physics


def playGame (screen):

	# Create the animated object
	diplo = Dino.Dino("Sprites/diplo.png", "Sprites/diplo_bent.png")
	cactus = Dino.Cactus("Sprites/cactus.png")
	bird = Dino.Bird("Sprites/oiseau.png")

	# Load background
	bg = pygame.image.load("Sprites/bg2.jpg")
	pos_bg = pygame.Rect(0, 0, bg.get_width(), bg.get_height())
	bg_part = pygame.Rect(0, bg.get_height()-WINDOW_HEIGHT, bg.get_width(), WINDOW_HEIGHT)

	# Set a timer
	timer = pygame.time.Clock()

	continueGame = True
	
	while continueGame:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			return False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if diplo.state == Dino.WALKING:
					diplo.state = Dino.JUMPING
			elif event.key == pygame.K_DOWN:
				diplo.bend()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				diplo.stand_up()

		timer.tick(40)

		# Refresh the screen
		diplo.next_move()
		cactus.move()
		bird.move()

		# Scrolling of the background
		pos_bg.left -= 1
		if pos_bg.left < -bg.get_width():
			pos_bg.left = 0
		screen.blit(bg, pos_bg, area=bg_part)
		pos_bg.left += bg.get_width()
		screen.blit(bg, pos_bg, area=bg_part)
		pos_bg.left -= bg.get_width()

		screen.blit(cactus.sprite, cactus.pos)
		screen.blit(diplo.sprite, diplo.pos)
		screen.blit(bird.sprite, bird.pos)
	
		if physics.gotCollision (diplo.hitbox, cactus.hitbox) or physics.gotCollision (diplo.hitbox_neck, bird.hitbox):
			continueProg = game_over(screen)
			if not continueProg:
				return False
			continueGame = False

		pygame.display.flip()

	return True



def game_over (screen):

	font = pygame.font.Font(pygame.font.get_default_font(), 175)
	game_over = font.render("GAME OVER", 0, (0, 0, 0))

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

