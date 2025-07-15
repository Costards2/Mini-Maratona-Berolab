import random
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.next_obstacle_distance = 0
        self.min_distance = 500
        self.max_distance = 1000
        self.spawn_weights = [0.6, 0.4]  # 60% cactus, 40% bird
    
    def update(self, game):
        # Spawn new obstacles
        if len(self.obstacles) == 0 or game.score >= self.next_obstacle_distance:
            self._spawn_obstacle(game)
            self.next_obstacle_distance = game.score + random.randint(
                self.min_distance, 
                self.max_distance
            )
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(game.game_speed, self.obstacles)
            self._handle_collision(game, obstacle)

    def _spawn_obstacle(self, game):
        obstacle_class = random.choices([Cactus, Bird], weights=self.spawn_weights)[0]
        self.obstacles.append(obstacle_class())
        
        # Increase difficulty gradually
        if game.score > 1000:
            self.min_distance = max(200, self.min_distance - 30)
            self.max_distance = max(500, self.max_distance - 30)
            self.spawn_weights[1] = min(0.5, self.spawn_weights[1] + 0.05)

    def _handle_collision(self, game, obstacle):
        """Handle collision between player and obstacle"""
        if game.player.dino_rect.colliderect(obstacle.rect):
            if not game.player.check_invincibility():
                game.playing = False
                game.death_count += 1
                game.time.delay(500)  
            else:
                self.obstacles.remove(obstacle)
                game.player.powerup_time -= 20  

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset(self):
        self.obstacles = []
        self.next_obstacle_distance = 0
        self.min_distance = 500
        self.max_distance = 1000