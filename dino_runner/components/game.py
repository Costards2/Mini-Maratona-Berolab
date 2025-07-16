import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.powerup_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_paused = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.high_score = 0
        self.death_count = 0
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()

        self.shield_hit_sound = pygame.mixer.Sound('dino_runner/assets/sound/812518__dinisnakamura__shield-block-01.wav')
        self.death_sound = pygame.mixer.Sound('dino_runner/assets/sound/363172__runningmind__pickups_shield_belt.wav')
        self.game_music = 'dino_runner/assets/sound/198896__bone666138__8-bit-circus-music.wav'
        
        self.shield_hit_sound.set_volume(0.5)
        self.death_sound.set_volume(0.7)

    def execute(self):
        running = True
        while running:
            if not self.handle_events():
                running = False
                break
                
            if self.playing:  
                self.run_game_loop()
            else:
                self.show_game_over_screen()

            
            pygame.display.update()
            self.clock.tick(FPS)
        
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.playing:
                    self.reset_game()
                    self.playing = True
        return True

    def run_game_loop(self):
        self.update()
        self.draw()

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
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.draw_score()

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

    def show_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 36)
        
        texts = [
            ("GAME OVER", font_large),
            (f"Score: {self.score}", font_small),
            (f"High Score: {self.high_score}", font_small),
            ("Press SPACE to restart", font_small)
        ]
        
        for i, (text, font) in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, 
                           (SCREEN_WIDTH//2 - text_surface.get_width()//2, 
                            SCREEN_HEIGHT//2 - 100 + i * 40))

    def reset_game(self):
        self.player.reset()
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.score = 0
        self.game_speed = 20
        self.game_paused = False
        self.x_pos_bg = 0

        pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.play(-1)  # -1 faz a música repetir
        pygame.mixer.music.set_volume(0.3)  # Volume mais baixo que efeitos