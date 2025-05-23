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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Retro Runway")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.sound_manager = SoundManager()
        self.current_level = 0
        self.level = Level(LEVELS[self.current_level])
        self.player = Player(100, SCREEN_HEIGHT - 250)
        self.camera = Camera()
        self.camera.set_level_width(SCREEN_WIDTH * 2)
        self.score = 0
        self.game_state = "playing"
        # Play level music (strip .mp3)
        self.sound_manager.play_music(self.level.music.replace('.mp3',''))

        # Load background image
        try:
            self.bg_image = pygame.image.load(
                os.path.join(ASSETS_DIR, "Images", "background.png")
            ).convert()
            self.bg_rect = self.bg_image.get_rect()
        except FileNotFoundError:
            self.bg_image = None
            self.bg_rect = None

        # Load win and lose screens
        self.win_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "Images", "win_screen.png")
        ).convert()
        self.win_image = pygame.transform.scale(self.win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.lose_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "Images", "lost_screen.png")
        ).convert()
        self.lose_image = pygame.transform.scale(self.lose_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Delay bouncer activation
        self.collision_delay = pygame.time.get_ticks() + 2000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.check_collectibles()
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_LSHIFT:
                    self.player.activate_disco()
                elif event.key == pygame.K_r and self.game_state != "playing":
                    # restart the game
                    self.__init__()

    def check_collectibles(self):
        for c in self.level.collectibles:
            if pygame.sprite.collide_rect(self.player, c):
                if c.item_type == "Disco-Ball":
                    self.player.disco_count += 1
                else:
                    self.player.add_outfit_piece(c.item_type)
                self.score += 1000
                c.collected = True
                self.sound_manager.play_sound("collect")

    def update(self):
        if self.game_state != "playing":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.player.crouch(True)
        else:
            self.player.crouch(False)

        self.player.update(self.level.platforms)
        self.player.rect.x = max(0, min(self.player.rect.x, SCREEN_WIDTH * 2 - self.player.rect.width))

        # 1) Check for level completion before any bouncer can tag you
        self.check_level_completion()
        if self.game_state != "playing":
            return

        # 2) Enemy collisions (only if still playing)
        if pygame.time.get_ticks() > self.collision_delay:
            for enemy in self.level.enemies:
                enemy.update()
                hiding = (
                    self.player.crouching
                    and pygame.sprite.spritecollideany(self.player, self.level.hiding_spots)
                )
                if enemy.check_vision(self.player) and not self.player.disco_active and not hiding:
                    self.sound_manager.play_sound("hit")
                    self.game_state = "game_over"
                    return

        # 3) Update camera last
        self.camera.update(self.player)

    def check_level_completion(self):
        remaining = [
            c for c in self.level.collectibles
            if not c.collected and c.item_type != "Disco-Ball"
        ]
        if not remaining:
            self.current_level += 1
            if self.current_level < len(LEVELS):
                self.sound_manager.play_sound("victory")
                self.level = Level(LEVELS[self.current_level])
                self.player.rect.x = 100
                self.player.rect.y = SCREEN_HEIGHT - 250
                self.sound_manager.play_music(self.level.music.replace('.mp3',''))
                self.collision_delay = pygame.time.get_ticks() + 2000
            else:
                # no more levels → victory!
                self.game_state = "victory"
                self.sound_manager.play_music("victory_theme")

    def draw(self):
        # Win / lose screens override normal level draw
        if self.game_state == "game_over":
            self.screen.blit(self.lose_image, (0, 0))
            pygame.display.flip()
            return
        if self.game_state == "victory":
            self.screen.blit(self.win_image, (0, 0))
            pygame.display.flip()
            return

        # Normal level rendering
        if self.bg_image:
            for x in range(0, SCREEN_WIDTH, self.bg_rect.width):
                for y in range(0, SCREEN_HEIGHT, self.bg_rect.height):
                    self.screen.blit(self.bg_image, (x, y))
        else:
            self.screen.fill(BLACK)

        for p in self.level.platforms:
            self.screen.blit(p.image, (
                p.rect.x - self.camera.offset.x,
                p.rect.y - self.camera.offset.y
            ))
        for h in self.level.hiding_spots:
            self.screen.blit(h.image, (
                h.rect.x - self.camera.offset.x,
                h.rect.y - self.camera.offset.y
            ))
        for c in self.level.collectibles:
            c.draw(self.screen, self.camera)
        for e in self.level.enemies:
            e.draw_vision_cone(self.screen, self.camera)
            e.draw(self.screen, self.camera)

        self.player.draw(self.screen, self.camera)
        self.draw_hud()
        pygame.display.flip()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, RETRO_YELLOW)
        self.screen.blit(score_text, (10, 10))
        for i, item in enumerate(OUTFIT_ORDER):
            color = DISCO_BLUE if item in self.player.outfit else NEON_PINK
            pygame.draw.rect(
                self.screen, color,
                (10 + i*40, 50, 30, 30),
                0 if item in self.player.outfit else 2
            )
        for i in range(self.player.disco_count):
            pygame.draw.circle(
                self.screen, RETRO_YELLOW,
                (SCREEN_WIDTH - 30 - i*40, 30),
                15
            )

class Camera:
    def __init__(self):
        self.offset = pygame.math.Vector2(0, 0)

    def update(self, player):
        target_x = player.rect.centerx - SCREEN_WIDTH//2
        self.offset.x = max(0, min(target_x, SCREEN_WIDTH*2 - SCREEN_WIDTH))

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
