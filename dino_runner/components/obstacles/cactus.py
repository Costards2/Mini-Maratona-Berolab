import random
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS
from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    CACTUS_TYPES = [
        (LARGE_CACTUS, 300),  
        (SMALL_CACTUS, 325),
    ]

    def __init__(self):
        images, y_pos = random.choice(self.CACTUS_TYPES)
        image = random.choice(images)  
        super().__init__(image)  
        self.rect.y = y_pos