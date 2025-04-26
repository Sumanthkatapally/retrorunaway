import pygame
import sys
import os
import random
from player import Player
from level import Level
from constants import *
from sound_manager import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Runway")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.sound_manager = SoundManager()
        self.current_level = 0
        self.level = Level(LEVELS[self.current_level])
        self.player = Player(100, SCREEN_HEIGHT - 250)  # Raised player start even higher
        self.camera = Camera()
        self.camera.set_level_width(SCREEN_WIDTH * 2) # set the level width
        self.score = 0
        self.game_state = "playing"  # Ensure it starts as playing
        self.sound_manager.play_music(self.level.music)
        try:
            self.bg_image = pygame.image.load(os.path.join(ASSETS_DIR, "Images", "background.png")).convert()
            self.bg_rect = self.bg_image.get_rect()
        except FileNotFoundError:
            print("Background image not found!")
            self.bg_image = None
            self.bg_rect = None
        self.collision_delay = 2000 # Delay 2 seconds

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: # is it K_UP or K_SPACE?
                    self.check_collectibles()
                    self.player.jump() # should be here!
                if event.key == pygame.K_LSHIFT:
                    self.player.activate_disco()
                if event.key == pygame.K_r and self.game_state != "playing":
                    self.__init__()

    def check_collectibles(self):
        for collectible in self.level.collectibles:
            if pygame.sprite.collide_rect(self.player, collectible):
                if collectible.item_type == "Disco-Ball":
                    self.player.disco_count += 1
                else:
                    self.player.add_outfit_piece(collectible.item_type)
                    self.score += 1000
                collectible.collected = True
                self.sound_manager.play_sound("collect")

    def update(self):
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += 5
            if keys[pygame.K_DOWN]:
                self.player.crouch(True)
            else:
                self.player.crouch(False)

            self.player.update(self.level.platforms)
            self.player.rect.x = max(0, min(self.player.rect.x, SCREEN_WIDTH * 2 - self.player.rect.width))

            if(pygame.time.get_ticks() > self.collision_delay): # 2 second delay to allow bouncer placement
              for enemy in self.level.enemies:
                enemy.update()
                if enemy.check_vision(self.player) and not self.player.disco_active:  # Added disco check
                    self.sound_manager.play_sound("hit")
                    self.game_state = "game_over"
            self.check_level_completion()
            self.camera.update(self.player)

    def check_level_completion(self):
        if len([c for c in self.level.collectibles if not c.collected and c.item_type != "Disco-Ball"]) == 0:
            self.current_level += 1
            if self.current_level < len(LEVELS):
                self.sound_manager.play_sound("victory.mp3")
                self.level = Level(LEVELS[self.current_level])
                self.player.rect.x = 100
                self.player.rect.y = SCREEN_HEIGHT - 250  # Reset player y
                self.sound_manager.play_music(self.level.music)
                self.collision_delay = pygame.time.get_ticks() + 2000# Check for initial collision after level load
                for enemy in self.level.enemies:
                    if enemy.check_vision(self.player) and not self.player.disco_active:
                        self.game_state = "game_over"
                        break
            else:
                self.game_state = "victory"
                self.sound_manager.play_music("victory_theme.mp3")

    def draw(self):
        if self.bg_image:
            for x in range(0, SCREEN_WIDTH, self.bg_rect.width):
                for y in range(0, SCREEN_HEIGHT, self.bg_rect.height):
                    self.screen.blit(self.bg_image, (x, y))
        else:
            self.screen.fill((0, 0, 0))

        for platform in self.level.platforms:
            self.screen.blit(platform.image, (platform.rect.x - self.camera.offset.x, platform.rect.y - self.camera.offset.y))
    
        for hiding_spot in self.level.hiding_spots:
            self.screen.blit(hiding_spot.image, (hiding_spot.rect.x - self.camera.offset.x, hiding_spot.rect.y - self.camera.offset.y))
        
        for collectible in self.level.collectibles:
            collectible.draw(self.screen, self.camera)
        
        for enemy in self.level.enemies:
            enemy.draw_vision_cone(self.screen, self.camera)
            enemy.draw(self.screen, self.camera)
        
        self.player.draw(self.screen, self.camera)
        self.draw_hud()
        
        if self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()
        
        pygame.display.flip()

    def draw_hud(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, RETRO_YELLOW)
        self.screen.blit(score_text, (10, 10))
        
        # Outfit progress
        for i, item in enumerate(OUTFIT_ORDER):
            color = DISCO_BLUE if item in self.player.outfit else NEON_PINK
            pygame.draw.rect(self.screen, color, (10 + i * 40, 50, 30, 30), 0 if item in self.player.outfit else 2)
        
        # Disco balls
        for i in range(self.player.disco_count):
            pygame.draw.circle(self.screen, RETRO_YELLOW, (SCREEN_WIDTH - 30 - i * 40, 30), 15)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render("GAME OVER! Press R to Restart", True, NEON_PINK)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render("GROOVY! YOU'RE DISCO ROYALTY!", True, RETRO_YELLOW)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        score_text = self.font.render(f"Final Score: {self.score}", True, NEON_PINK)
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 + 20))

class Camera:
    def __init__(self):
        self.offset = pygame.math.Vector2(0, 0)

    def update(self, player):
        # Horizontal follow (centered)
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.x = target_x
        self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH)) # Changed level_width for screen_width

    def set_level_width(self, level_width):
        self.level_width = level_width

def main():
    game = Game()
    while True:
        game.handle_events()
        game.update()
        game.draw()
        game.clock.tick(60)

if __name__ == "__main__":
    main()
