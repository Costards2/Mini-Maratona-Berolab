import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.powerup_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.utils.text_utils import draw_message_component

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.high_score = 0
        self.death_count = 0
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()

    def execute(self):
        self.playing = True
        while self.playing:
            if not self.run():
                self.show_menu()
        
        pygame.quit()

    def run(self):
        # Game loop
        self.playing = True
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.game_speed = 20
        self.score = 0
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
        return False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_DOWN:
                    self.player.duck(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.duck(False)

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.powerup_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 1
        
        if self.score > self.high_score:
            self.high_score = self.score

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.x_pos_bg -= self.game_speed
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0

    def draw_score(self):
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        self.screen.blit(score_text, (850, 30))
        self.screen.blit(high_score_text, (800, 60))

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            draw_message_component("Press any key to start", self.screen)
        else:
            draw_message_component("Press any key to restart", self.screen)
            draw_message_component(f"Your Score: {self.score}", self.screen, pos_y_center=SCREEN_HEIGHT//2 + 50)
            draw_message_component(f"High Score: {self.high_score}", self.screen, pos_y_center=SCREEN_HEIGHT//2 + 100)
            draw_message_component(f"Death count: {self.death_count}", self.screen, pos_y_center=SCREEN_HEIGHT//2 + 150)
        
        pygame.display.update()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    waiting = False