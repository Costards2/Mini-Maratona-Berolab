import pygame
import random

class PowerUp:
    def __init__(self, image, powerup_type):
        self.image = image
        self.type = powerup_type
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = random.randint(200, 300)
        self.speed = 10

    def update(self, game_speed, powerups):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            powerups.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)