from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD[0])
        self.animation_images = BIRD
        self.rect.y = 250
        self.step_index = 0
        self.animation_speed = 5
        self.vertical_movement = 0
        self.vertical_speed = 0.8
        self.max_vertical = 25
        self.moving_up = True

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        
        if self.moving_up:
            self.vertical_movement -= self.vertical_speed
            if self.vertical_movement <= -self.max_vertical:
                self.moving_up = False
        else:
            self.vertical_movement += self.vertical_speed
            if self.vertical_movement >= self.max_vertical:
                self.moving_up = True
        
        self.rect.y = 250 + self.vertical_movement
        
        self.step_index += 1
        if self.step_index >= len(self.animation_images) * self.animation_speed:
            self.step_index = 0
        
        self.image = self.animation_images[self.step_index // self.animation_speed]
        super().update(game_speed, obstacles)

    def draw(self, screen):
        screen.blit(self.image, self.rect)