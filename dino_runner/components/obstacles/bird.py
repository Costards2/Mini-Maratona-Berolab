from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD)  
        self.rect.y = 250
        self.vertical_speed = 0.8
        self.max_vertical = 25
        self.vertical_movement = 0
        self.moving_up = True
        self.animation_speed = 3 

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
        
        super().update(game_speed, obstacles)