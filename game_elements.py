import pygame

from constantes import *

class Animated_object:

	def is_alive(self):
		if self.pos.left + self.pos.width < 0:
			return False
		else:
			return True



class Cactus (Animated_object):
	def __init__(self):
		self.sprite = pygame.image.load("Sprites/cactus.png")
		self.pos = pygame.Rect(WINDOW_WIDTH, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
		self.hitbox = pygame.Rect(self.pos.left, self.pos.top+20, self.sprite.get_width(), self.sprite.get_height())

	def move(self):
		self.pos.left -= 10
		self.hitbox.left = self.pos.left




class Bird (Animated_object):
	def __init__(self):
		self.sprite = pygame.image.load("Sprites/oiseau.png")
		self.pos = pygame.Rect(WINDOW_WIDTH, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
		self.pos.top -= BIRD_LEVEL
		self.hitbox = pygame.Rect(self.pos.left, self.pos.top, self.sprite.get_width()-10, self.sprite.get_height())

	def move(self):
		self.pos.left -= 10
		self.hitbox.left = self.pos.left



class Trex (Animated_object):
	def __init__(self):
		self.sprite = pygame.image.load("Sprites/trex.png")
		self.pos = pygame.Rect(WINDOW_WIDTH, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
		self.hitbox = pygame.Rect(self.pos.left, self.pos.top, self.sprite.get_width()-10, self.sprite.get_height())
		self.gotHurt = False
		self.state = WALKING

	def move(self):
		self.pos.left -= 10	
		self.hitbox.left = self.pos.left		

	def getHurt(self):
		self.state = IS_DYING
		self.hitbox = pygame.Rect(0, 0, 0, 0)
		self.sprite = pygame.transform.rotate(self.sprite, 90)
		#self.pos.top += 100


class Dino (Animated_object):

	def __init__(self):
		self.sprite = pygame.image.load("Sprites/diplo.png")
		self.pos = pygame.Rect(50, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
		self.sprite_walk = self.sprite
		self.sprite_bent = pygame.image.load("Sprites/diplo_bent.png")
		self.sprite_l = pygame.image.load("Sprites/diplo_l.png")
		self.sprite_bent_l = pygame.image.load("Sprites/diplo_bent_l.png")
		self.hitbox = pygame.Rect(self.pos.left+50, self.pos.top+75, 150, self.sprite.get_height()-75)
		self.hitbox_neck = pygame.Rect(self.pos.left+HITBOX_NECK_X, self.pos.top, self.sprite.get_width()-HITBOX_NECK_X, 150)
		self.state = WALKING
		self.frame_counter = 0
		self.attack_count = 0

	def update_hitbox(self):
		if self.state != BENDING:
			self.hitbox.left = self.pos.left+50
			self.hitbox.top = self.pos.top+75
			self.hitbox.width = 150
			self.hitbox.height = self.sprite.get_height()-75
			self.hitbox_neck = pygame.Rect(self.pos.left+HITBOX_NECK_X, self.pos.top, self.sprite.get_width()-HITBOX_NECK_X, 150)

	def next_move(self):
		# Update the attributs depending on the state
		if self.state == JUMPING:
			self.jump()
		elif self.state == FALLING:
			self.fall()
		elif self.state == ATTACKING:
			self.attack_count += 1
			if self.attack_count >= ATTACK_TIMING:
				self.sprite_walk = pygame.transform.flip(self.sprite_walk, True, False)
				self.sprite_l = pygame.transform.flip(self.sprite_l, True, False)
				self.state = WALKING
				self.update_hitbox()
				self.attack_count = 0
		# determine the new sprite
		self.frame_counter += 1
		if self.frame_counter >= 10:
			self.sprite_walk, self.sprite_l = self.sprite_l, self.sprite_walk
			self.sprite_bent, self.sprite_bent_l = self.sprite_bent_l, self.sprite_bent
			self.frame_counter = 0
			if self.state == WALKING or self.state == ATTACKING:
				self.sprite = self.sprite_walk
			elif self.state == BENDING:
				self.sprite  =self.sprite_bent
		self.update_hitbox()

	def jump(self):
		if self.state == JUMPING:
			if self.pos.y > MAX_JUMP:
				self.pos.y -= JUMP_SPEED
			else:
				self.state = FALLING

	def fall(self):
		if self.pos.y < GROUND-self.sprite.get_height():
			self.pos.y += FALL_SPEED
		else:
			self.pos.y = GROUND-self.sprite.get_height()
			self.state = WALKING

	def bend(self):
		if self.state == WALKING:
			self.state = BENDING
			if self.sprite == self.sprite_walk:
				self.sprite = self.sprite_bent
			else:
				self.sprite = self.sprite_bent_l
			self.pos = pygame.Rect(50, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
			self.hitbox = self.pos
			self.hitbox_neck = pygame.Rect(0, 0, 0, 0)

	def stand_up(self):
		if self.state == BENDING:
			self.state = WALKING
			if self.sprite == self.sprite_bent:
				self.sprite = self.sprite_walk
			else:
				self.sprite = self.sprite_walk_l
			self.pos = pygame.Rect(50, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
			self.update_hitbox()

	def attack(self):
		if self.state == WALKING:
			self.state = ATTACKING
			self.sprite_walk = pygame.transform.flip(self.sprite_walk, True, False)
			self.sprite_l = pygame.transform.flip(self.sprite_l, True, False)
			self.hitbox = pygame.Rect(self.pos.left, self.pos.top+75, self.sprite.get_width(), self.sprite.get_height()-75)
