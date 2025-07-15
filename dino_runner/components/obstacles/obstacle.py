import pygame

class Obstacle:
    def __init__(self, images, obstacle_type=0):
        self.images = images if isinstance(images, list) else [images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 1100  
        self.type = obstacle_type
        self.animation_index = 0
        self.animation_count = 0
        self.animation_speed = 5  

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        self.animate()
        
        if self.rect.right < 0:  
            obstacles.remove(self)

    def animate(self):
        """Handle sprite animation if multiple frames exist"""
        if len(self.images) > 1:
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)