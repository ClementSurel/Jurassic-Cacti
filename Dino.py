import pygame

from constantes import *

class Animated_object:
	def __init__(self, sprite_file, position=None):
		self.sprite = pygame.image.load(sprite_file)
		self.pos = pygame.Rect(0, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
	



class Cactus (Animated_object):
	def __init__(self, sprite_file):
		Animated_object.__init__(self, sprite_file)
		self.pos.left = WINDOW_WIDTH
		self.hitbox = pygame.Rect(self.pos.left, self.pos.top, self.sprite.get_width(), self.sprite.get_height())

	def move(self):
		self.pos.left -= 10
		if self.pos.left < -self.sprite.get_width():
			self.pos.left = WINDOW_WIDTH + 2000
		self.hitbox.left = self.pos.left
		self.hitbox.top = self.pos.top+35




class Bird (Animated_object):
	def __init__(self, sprite_file):
		Animated_object.__init__(self, sprite_file)
		self.pos.left = WINDOW_WIDTH + 1000
		self.pos.top -= 180
		self.hitbox = pygame.Rect(self.pos.left, self.pos.top, self.sprite.get_width()-10, self.sprite.get_height())

	def move(self):
		self.pos.left -= 10
		if self.pos.left < -self.sprite.get_width():
			self.pos.left = WINDOW_WIDTH + 2000
		self.hitbox.left = self.pos.left
		self.hitbox.top = self.pos.top




class Dino (Animated_object):
	def __init__(self, sprite_file, sprite_bent_file):
		Animated_object.__init__(self, sprite_file)
		self.sprite_bent = pygame.image.load(sprite_bent_file)
		self.hitbox = pygame.Rect(self.pos.left+61, self.pos.top+75, 149, 156)
		self.hitbox_neck = pygame.Rect(self.pos.left+HITBOX_NECK_X, self.pos.top, self.sprite.get_width()-HITBOX_NECK_X, 150)
		self.state = WALKING

	def update_hitbox(self):
		if self.state != BENDING:
			self.hitbox.left = self.pos.left+61
			self.hitbox.top = self.pos.top+75
			self.hitbox.width = 149
			self.hitbox.height = 160
			self.hitbox_neck = pygame.Rect(self.pos.left+HITBOX_NECK_X, self.pos.top, self.sprite.get_width()-HITBOX_NECK_X, 150)


	def next_move(self):
		if self.state == WALKING:
			return
		elif self.state == JUMPING:
			self.jump()
		elif self.state == FALLING:
			self.fall()
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
			self.sprite, self.sprite_bent = self.sprite_bent, self.sprite
			self.pos = pygame.Rect(0, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
			self.hitbox = self.pos
			self.hitbox_neck = pygame.Rect(0, 0, 0, 0)

	def stand_up(self):
		if self.state == BENDING:
			self.state = WALKING
			self.sprite, self.sprite_bent = self.sprite_bent, self.sprite
			self.pos = pygame.Rect(0, GROUND-self.sprite.get_height(), self.sprite.get_width(), self.sprite.get_height())
			self.update_hitbox()