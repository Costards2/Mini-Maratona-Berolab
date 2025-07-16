import pygame
from dino_runner.utils.constants import (
    RUNNING, JUMPING, DUCKING,
    RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD,
    DEFAULT_TYPE, SHIELD_TYPE
)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    POWERUP_DURATION = 200  # 5 seconds at 40 FPS

    def __init__(self):
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.dino_jump = False
        self.dino_duck = False
        self.has_powerup = False
        self.powerup_time = 0

    def update(self, user_input):
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck(True)
        
        if (user_input[pygame.K_UP] or user_input[pygame.K_w] or user_input[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_jump = True
        elif (user_input[pygame.K_DOWN] or user_input[pygame.K_s]) and not self.dino_jump:
            self.dino_duck = True
        elif not self.dino_jump:
            self.run()
        
        if self.step_index >= 10:
            self.step_index = 0
        
        if self.has_powerup:
            self.powerup_time -= 1
            if self.powerup_time <= 0:
                self.deactivate_powerup()

    def run(self):
        self.image = self.run_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        if self.step_index // 5 >= len(self.run_img[self.type]):
            self.step_index = 0
        self.step_index += 1
        self.dino_duck = False

    def jump(self):
        self.image = self.jump_img[self.type]
        if not self.dino_jump:
            self.jump_vel = self.JUMP_VEL
            self.dino_jump = True
        
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        
        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self, is_ducking):
        if is_ducking:
            self.image = self.duck_img[self.type][self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            if self.step_index // 5 >= len(self.run_img[self.type]):
                self.step_index = 0
            self.dino_duck = True
        else:
            self.dino_duck = False
            self.dino_rect.y = self.Y_POS
            self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def activate_powerup(self, powerup_type, duration=200):
        self.type = powerup_type
        self.has_powerup = True
        self.powerup_time = duration
        if powerup_type == SHIELD_TYPE:
            self.image = RUNNING_SHIELD[0]

    def deactivate_powerup(self):
        self.has_powerup = False
        self.type = DEFAULT_TYPE
        self.image = RUNNING[0]

    def check_invincibility(self):
        return self.has_powerup and self.type == SHIELD_TYPE

    def reset(self):
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.dino_jump = False
        self.dino_duck = False
        self.has_powerup = False
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL