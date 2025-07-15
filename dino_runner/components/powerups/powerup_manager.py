import random
from dino_runner.components.powerups.shield import Shield

class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.next_powerup_time = random.randint(200, 300) 
        self.duration = 200  # 5 seconds at 40 FPS

    def update(self, game):
        if game.score >= self.next_powerup_time and not self.powerups:
            self.powerups.append(Shield())
            self.next_powerup_time = game.score + random.randint(200, 300) 

        # Update existing powerups
        for powerup in self.powerups[:]:  
            powerup.update(game.game_speed, self.powerups)
            
            if game.player.dino_rect.colliderect(powerup.rect):
                game.player.activate_powerup(powerup.type, self.duration)
                self.powerups.remove(powerup)

    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)

    def reset(self):
        self.powerups = []
        self.next_powerup_time = random.randint(200, 300)